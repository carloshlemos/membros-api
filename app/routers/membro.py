from typing import Optional
from fastapi import APIRouter, Query, Request, HTTPException, Depends
from app.domain import schemas
from ..service.membro import MembroService
from .. import security
from pymongo import ASCENDING, DESCENDING
from datetime import timedelta

router = APIRouter(
    tags=['Membro']
)

@router.post("/membros/new/token")
def generate_new_member_token():
    expires_delta = timedelta(hours=24)
    access_token = security.create_access_token(
        data={"sub": "new_member", "type": "new_member"},
        expires_delta=expires_delta
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/membros/{membro_id}/token")
def generate_token(membro_id: str):
    membro = MembroService().get_by_id(membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro not found")
    
    access_token = security.create_access_token(data={"sub": membro_id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/membros/me", response_model=schemas.Membro)
def get_current_member(current_member_id: str = Depends(security.get_current_member_id)):
    membro = MembroService().get_by_id(current_member_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro not found")
    return membro


@router.put("/membros/me", response_model=schemas.Membro)
def update_current_member(
    data: schemas.UpdateMembro,
    current_member_id: str = Depends(security.get_current_member_id)
):
    updated_membro = MembroService().update_membro(current_member_id, data)
    if not updated_membro:
        raise HTTPException(status_code=404, detail="Membro not found")
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