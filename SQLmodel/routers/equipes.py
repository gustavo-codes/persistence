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

@router.get('',response_model=List[Equipe])
def listar_equipes(session:Session = Depends(get_session)):
    return session.exec(select(Equipe)).all()

@router.get('/{equipe_id}',response_model=Equipe)
def buscar_equipe(equipe_id:int, session:Session = Depends(get_session)):
    equipe = session.get(Equipe,equipe_id)

    if not equipe:
        raise HTTPException(status_code=404, detail='Equipe não encotrada')
    return equipe

@router.put('/{equipe_id}',response_model=Equipe)
def atualizar_equipe(equipe_id:int, equipe:Equipe ,session:Session = Depends(get_session)):
    equipe_atual = session.get(Equipe,equipe_id)

    if not equipe_atual:
        raise HTTPException(status_code=404, detail='Equipe não encotrada')
    
    equipe_data = equipe.model_dump(exclude_unset=True)
    for key, value in equipe_data.items():
        setattr(equipe_atual,key,value)

    session.add(equipe_atual)
    session.commit()
    session.refresh(equipe_atual)

    return equipe_atual

@router.delete('/{equipe_id}')
def excluir_equipe(equipe_id:int, session:Session = Depends(get_session)):
    
    