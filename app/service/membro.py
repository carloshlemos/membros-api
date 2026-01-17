from datetime import datetime
from zoneinfo import ZoneInfo
import os
from app.repository.membro import MembroRepository
from app.security import create_access_token
from app.service.evolution import EvolutionService
from ..domain import schemas
from fastapi import HTTPException

TZ = ZoneInfo("America/Sao_Paulo")
FRONTEND_URL = os.getenv("FRONTEND_URL")
EVOLUTION_API_MESSAGE = os.getenv("EVOLUTION_API_MESSAGE")


class MembroService:
    def __init__(self):
        self.repository = MembroRepository()
        self.evolution = EvolutionService()

    def get_by_id(self, membro_id: str):
        return self.repository.find_by_id(membro_id)

    def generate_token(self, membro_id: str, celular: str):
        membro = self.get_by_id(membro_id)
        if not membro:
            raise HTTPException(status_code=404, detail="Membro not found")

        self.repository.update(membro_id, {"celular": celular})

        token = create_access_token(data={"sub": membro_id})
        message = f"{EVOLUTION_API_MESSAGE}: {FRONTEND_URL}/membros/me?token={token}"
        self.evolution.send_message(celular, message)
        return token

    def update_membro(self, membro_id: str, data: schemas.UpdateMembro):
        update_data = data.model_dump(exclude_unset=True)

        membro_atual = self.repository.find_by_id(membro_id)

        if not membro_atual:
            return None

        houve_mudanca = False

        # Verifica se algum campo foi alterado
        for campo, novo_valor in update_data.items():
            if membro_atual.get(campo) != novo_valor:
                houve_mudanca = True
                break

        if houve_mudanca:
            update_data["dados_atualizados"] = True
            update_data["ultima_atualizacao"] = datetime.now(TZ)

        return self.repository.update(membro_id, update_data)

    def get_all_membros(self, filters: dict, skip: int, limit: int, sort_by: str, sort_order: int):
        return self.repository.find_all(filters, skip, limit, sort_by, sort_order)
