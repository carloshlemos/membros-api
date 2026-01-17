from typing import Optional

from fastapi import APIRouter, Query, Request, HTTPException, Depends
from pymongo import ASCENDING, DESCENDING

from app.domain import schemas
from .. import security
from ..service.membro import MembroService

router = APIRouter(
    tags=['Membro']
)


@router.post("/membros/new/token")
def generate_new_member_token(data: schemas.NewMemberTokenRequest):
    token = MembroService().new_member_generate_token(data.celular)
    return {"access_token": token, "token_type": "bearer"}


@router.put("/membros/new", response_model=schemas.NewMember)
def update_new_member(
    data: schemas.UpdateNewMember,
    current_celular: str = Depends(security.get_current_new_member_celular)
):
    MembroService().update_new_member(current_celular, data)
    return MembroService().get_by_celular(current_celular)


@router.get("/membros/new/me", response_model=schemas.NewMember)
def get_current_new_member(current_celular: str = Depends(security.get_current_new_member_celular)):
    membro = MembroService().get_by_celular(current_celular)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    return membro


@router.post("/membros/{membro_id}/token")
def generate_token(membro_id: str, data: schemas.MembroTokenRequest):
    token = MembroService().generate_token(membro_id, data.celular)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/membros/me", response_model=schemas.Membro)
def get_current_member(current_member_id: str = Depends(security.get_current_member_id)):
    membro = MembroService().get_by_id(current_member_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    return membro


@router.put("/membros/me", response_model=schemas.Membro)
def update_current_member(
    data: schemas.UpdateMembro,
    current_member_id: str = Depends(security.get_current_member_id)
):
    updated_membro = MembroService().update_membro(current_member_id, data)
    if not updated_membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    return updated_membro

@router.get("/membros", response_model=schemas.MembrosResponse)
def get_membros(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query("nome"),
    sort_order: Optional[str] = Query("asc")
):
    query_params = dict(request.query_params)
    filters = {k: v for k, v in query_params.items() if k not in ["skip", "limit", "sort_by", "sort_order"]}
    
    order = DESCENDING if sort_order.lower() == "desc" else ASCENDING
    
    total, membros = MembroService().get_all_membros(filters, skip, limit, sort_by, order)
    
    return {"total": total, "membros": membros}