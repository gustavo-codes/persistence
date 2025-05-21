from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlmodel import Session, select
from db import get_session
from models import *

router = APIRouter(prefix='/membros', tags=['Membros'])

@router.post('',response_model=Membro)
def criar_membro(membro:Membro, session:Session = Depends(get_session)):
    
    exists = session.get(Membro,membro.id)

    if exists:
        raise HTTPException(status_code=404,detail='Membro com esse id já existe')
    
    equipe = session.get(Equipe,membro.equipe_id )

    if not equipe:
        raise HTTPException(status_code=404,detail='Equipe não existe')
    
    session.add(membro)
    session.commit()
    session.refresh(membro)

    return membro

@router.get('',response_model=List[Membro])
def listar_membros(session:Session = Depends(get_session)):
    return session.exec(select(Membro)).all()

@router.get('/{membro_id}',response_model=Membro)
def buscar_membro(membro_id:int, session:Session = Depends(get_session)):
    membro = session.get(Membro,membro_id)

    if not membro:
        raise HTTPException(status_code=404,detail='Membro não existe')
    
    return membro

@router.put('/{membro_id}',response_model=Membro)
def atualizar_membro(membro_id:int,membro:Membro, session:Session = Depends(get_session)):
    membro_atual = session.get(Membro,membro_id)

    if not membro_atual:
        raise HTTPException(status_code=404,detail='Membro não existe')
    
    membro_data = membro.model_dump(exclude_unset=True)

    for key, val in membro_data.items():
        setattr(membro_atual,key,val)

    session.add(membro_atual)
    session.commit()
    session.refresh(membro_atual)

    return membro_atual

@router.delete('/{membro_id}')
def deletar_membro(membro_id:int,session:Session = Depends(get_session)):
    membro = session.get(Membro,membro_id)

    if not membro:
        raise HTTPException(status_code=404,detail='Membro não existe')
    
    session.delete(membro)
    session.commit()

    return {'msg':f'Membro {membro_id} deletado'}