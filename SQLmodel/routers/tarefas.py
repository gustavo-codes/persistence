from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlmodel import Session, select
from db import get_session
from models import *

router = APIRouter(prefix='/tarefas', tags=['Tarefas'])



@router.post('',response_model=Tarefa)
def criar_tarefa(tarefa:Tarefa, session:Session = Depends(get_session)):
    exists = session.get(Tarefa,tarefa.id)

    if exists:
        raise HTTPException(status_code=404,detail='Tarefa com esse id já existe')

    projeto = session.get(Projeto,tarefa.projeto_id)

    if not projeto:
        raise HTTPException(status_code=404,detail='Projeto com esse id não existe')
    
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)

    return tarefa

@router.get('',response_model=List[Tarefa])
def listar_tarefas(session:Session = Depends(get_session)):
    return session.exec(select(Tarefa)).all()

@router.get('/{tarefa_id}',response_model=Tarefa)
def buscar_projeto(tarefa_id:int,session:Session = Depends(get_session)):
    tarefa = session.get(Tarefa,tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=404,detail='Tarefa com esse id não existe')
    
    return tarefa

@router.put('/{tarefa_id}',response_model=Tarefa)
def atualizar_tarefa(tarefa_id:int, tarefa:Tarefa,session:Session = Depends(get_session)):
    tarefa_atual = session.get(Tarefa,tarefa_id)

    if not tarefa_atual:
        raise HTTPException(status_code=404,detail='Tarefa com esse id não existe')
    
    tarefa_data = tarefa.model_dump()

    for key, val in tarefa_data.items():
        setattr(tarefa_atual,key,val)

    session.add(tarefa_atual)
    session.commit()
    session.refresh(tarefa_atual)

    return tarefa_atual

@router.delete('/{tarefa_id}')
def deletar_tarefa(tarefa_id:int,session:Session = Depends(get_session)):
    tarefa = session.get(Tarefa,tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=404,detail='Tarefa com esse id não existe')
    
    session.delete(tarefa)
    session.commit()

    return {'msg':f'Tarefa {tarefa_id} deletada'}