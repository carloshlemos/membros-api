from datetime import datetime
from typing import Optional
from uuid import uuid4
from zoneinfo import ZoneInfo

from bson import ObjectId
from pydantic import BaseModel, Field

TZ = ZoneInfo("America/Sao_Paulo")


class Membro(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    nome: Optional[str] = None
    sexo: Optional[str] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    nascimento: Optional[str] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None

    # campos criados automaticamente — NÃO vem do frontend
    dados_atualizados: Optional[bool] = None
    ultima_atualizacao: Optional[datetime] = None

class UpdateMembro(BaseModel):
    nome: Optional[str] = None
    sexo: Optional[str] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    nascimento: Optional[str] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None

    dados_atualizados: Optional[bool] = None
    ultima_atualizacao: Optional[datetime] = None

class MembrosResponse(BaseModel):
    total: int
    membros: list[Membro]
