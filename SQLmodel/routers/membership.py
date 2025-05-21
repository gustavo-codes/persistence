from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import *

router = APIRouter(prefix="/membership", tags=["MemberShip"])


@router.get("", response_model=List[Membership])
def listar_participacao(session: Session = Depends(get_session)):
    return session.exec(select(Membership))

@router.get("/{participacao_id}", response_model=Membership)
def procurar_participacao_por_id(participacao_id:int, session : Session = Depends(get_session)):
    exist = session.get(Membership,participacao_id)
    
    if not exist:
        raise HTTPException(status_code=404,detail="ID não encontrado!")
    
    return exist


@router.post("", response_model=Membership)
def criar_participacao(
    participacao: Membership, session: Session = Depends(get_session)
):
    exist = session.get(Membership, participacao.id)  # Checa se id já existe no db
    if exist:
        raise HTTPException(
            status_code=404, detail="Participação com esse id já existe!"
        )

    exist_membro_id = session.get(Membro, participacao.membro_id)

    if not exist_membro_id:
        raise HTTPException(status_code=404, detail="Membro não encontrado!")

    exist_equipe_id = session.get(Equipe, participacao.equipe_id)

    if not exist_equipe_id:
        raise HTTPException(status_code=404, detail="Equipe não encontrada!")

    session.add(participacao)
    session.commit()
    session.refresh(participacao)

    return participacao

@router.put("/{participacao_id}", response_model=Membership)
def atualizar_participacao(participacao_id: int, participacao:Membership, session : Session = Depends(get_session)):
    participacao_atual = session.get(Membership,participacao_id)
    
    if not participacao_atual:
        raise HTTPException(status_code=404,detail="Participação com esse id não existe!")
    
    participacao_data = participacao.model_dump()
    
    for key, val in participacao_data.items():
        setattr(participacao_atual,key,val)
    session.add(participacao_atual)
    session.commit()
    session.refresh(participacao_atual)
    
    return participacao_atual


@router.delete("/{participacao_id}")
def apagar_participacao(participacao_id: int, session: Session = Depends(get_session)):
    participacao = session.get(Membership, participacao_id)

    if not participacao:
        raise HTTPException(status_code=404, detail="Participação não existe!")

    session.delete(participacao)
    session.commit()

    return {"msg": f" Participação de  id {participacao_id} apagada!"}
