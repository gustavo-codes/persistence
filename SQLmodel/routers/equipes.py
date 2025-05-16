from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlmodel import Session, select
from db import get_session
from models import *

router = APIRouter(prefix='/equipes', tags=['Equipes'])

@router.post('',response_model=Equipe)
def criar_equipe(equipe:Equipe, session:Session = Depends(get_session))->Equipe:
    session.add(equipe)
    session.commit()
    session.refresh(equipe)
    return equipe
