import os
from app.repository.new_member import NewMemberRepository
from app.security import create_access_token
from app.service.evolution import EvolutionService

FRONTEND_URL = os.getenv("FRONTEND_URL")


class NewMemberService:
    def __init__(self):
        self.repository = NewMemberRepository()
        self.evolution = EvolutionService()

    def generate_token(self, celular: str):
        token = create_access_token(data={"sub": celular})
        self.repository.save(token, celular)
        message = f"Olá! Para continuar o seu cadastro, clique no link a seguir: {FRONTEND_URL}/membros/novo?token={token}"
        self.evolution.send_message(celular, message)
        return token

    def update_new_member(self, celular: str, data):
        update_data = data.dict(exclude_unset=True)
        update_data["celular"] = celular
        self.repository.update(celular, update_data)

    def get_by_celular(self, celular: str):
        return self.repository.get_by_celular(celular)


