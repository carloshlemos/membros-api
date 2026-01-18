from datetime import datetime
from typing import Optional
from uuid import uuid4
from zoneinfo import ZoneInfo

from bson import ObjectId
from pydantic import BaseModel, Field, validator


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
    nascimento: Optional[datetime] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None
    pais: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    nome_conjuge: Optional[str] = None
    data_casamento: Optional[datetime] = None
    rg: Optional[str] = None
    batismo_data: Optional[datetime] = None
    batismo_pastor: Optional[str] = None
    batismo_igreja: Optional[str] = None
    profissao_fe_data: Optional[datetime] = None
    profissao_fe_pastor: Optional[str] = None
    profissao_fe_igreja: Optional[str] = None

    # campos criados automaticamente — NÃO vem do frontend
    dados_atualizados: Optional[bool] = None
    ultima_atualizacao: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True # Changed from allow_population_by_field_name



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
    nascimento: Optional[datetime] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None
    pais: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    nome_conjuge: Optional[str] = None
    data_casamento: Optional[datetime] = None
    rg: Optional[str] = None
    batismo_data: Optional[datetime] = None
    batismo_pastor: Optional[str] = None
    batismo_igreja: Optional[str] = None
    profissao_fe_data: Optional[datetime] = None
    profissao_fe_pastor: Optional[str] = None
    profissao_fe_igreja: Optional[str] = None

    dados_atualizados: Optional[bool] = None
    ultima_atualizacao: Optional[datetime] = None

    @validator("nascimento", "data_casamento", "batismo_data", "profissao_fe_data", pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class MembrosResponse(BaseModel):
    total: int
    membros: list[Membro]


class MembroTokenRequest(BaseModel):
    celular: str


class NewMemberTokenRequest(BaseModel):
    celular: str


class NewMember(BaseModel):
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
    nascimento: Optional[datetime] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None
    pais: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    nome_conjuge: Optional[str] = None
    data_casamento: Optional[datetime] = None
    rg: Optional[str] = None
    batismo_data: Optional[datetime] = None
    batismo_pastor: Optional[str] = None
    batismo_igreja: Optional[str] = None
    profissao_fe_data: Optional[datetime] = None
    profissao_fe_pastor: Optional[str] = None
    profissao_fe_igreja: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True # Changed from allow_population_by_field_name


class UpdateNewMember(BaseModel):
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
    nascimento: Optional[datetime] = None
    naturalidade: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    profissao: Optional[str] = None
    tipo_membro: Optional[str] = None
    oficio: Optional[str] = None
    pais: Optional[str] = None
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    nome_conjuge: Optional[str] = None
    data_casamento: Optional[datetime] = None
    rg: Optional[str] = None
    batismo_data: Optional[datetime] = None
    batismo_pastor: Optional[str] = None
    batismo_igreja: Optional[str] = None
    profissao_fe_data: Optional[datetime] = None
    profissao_fe_pastor: Optional[str] = None
    profissao_fe_igreja: Optional[str] = None

    @validator("nascimento", "data_casamento", "batismo_data", "profissao_fe_data", pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
