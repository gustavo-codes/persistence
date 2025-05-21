from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlmodel import Session, select
from db import get_session
from models import *

router = APIRouter(prefix='/projetos', tags=['Projetos'])

@router.post('',response_model=Projeto)
def criar_projeto(projeto:Projeto, session:Session = Depends(get_session)):
    exists = session.get(Projeto,projeto.id)

    if exists:
        raise HTTPException(status_code=404,detail='Projeto com esse id já existe')

    equipe = session.get(Equipe,projeto.equipe_id)

    if not equipe:
        raise HTTPException(status_code=404,detail='Equipe com esse id não existe')
    
    session.add(projeto)
    session.commit()
    session.refresh(projeto)

    return projeto


@router.get('',response_model=List[Projeto])
def listar_projetos(session:Session = Depends(get_session)):
    return session.exec(select(Projeto)).all()

@router.get('/{projeto_id}',response_model=Projeto)
def buscar_projeto(projeto_id:int,session:Session = Depends(get_session)):
    projeto = session.get(Projeto,projeto_id)

    if not projeto:
        raise HTTPException(status_code=404,detail='Projeto com esse id não existe')
    
    return projeto

@router.put('/{projeto_id}',response_model=Projeto)
def atualizar_projeto(projeto_id:int, projeto:Projeto,session:Session = Depends(get_session)):
    projeto_atual = session.get(Projeto,projeto_id)

    if not projeto_atual:
        raise HTTPException(status_code=404,detail='Projeto com esse id não existe')
    
    projeto_data = projeto.model_dump()

    for key, val in projeto_data.items():
        setattr(projeto_atual,key,val)

    session.add(projeto_atual)
    session.commit()
    session.refresh(projeto_atual)

    return projeto_atual

@router.delete('/{projeto_id}')
def deletar_projeto(projeto_id:int,session:Session = Depends(get_session)):
    projeto = session.get(Projeto,projeto_id)

    if not projeto:
        raise HTTPException(status_code=404,detail='Projeto com esse id não existe')
    
    session.delete(projeto)
    session.commit()

    return {'msg':f'Projeto {projeto_id} deletado'}