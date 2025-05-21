from fastapi import  HTTPException, FastAPI
from sqlmodel import Session, select
from db import create_db_and_tables
from routers import equipes, membros, projetos, tarefas

app = FastAPI()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get('/')
def home():
    return {'msg':'Bem-Vindo'}

app.include_router(equipes.router)
app.include_router(membros.router)
app.include_router(projetos.router)
app.include_router(tarefas.router)