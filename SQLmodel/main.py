from fastapi import  HTTPException, FastAPI
from sqlmodel import Session, select
from db import create_db_and_tables
from routers import equipes

app = FastAPI()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get('/')
def home():
    return {'msg':'Bem-Vindo'}

app.include_router(equipes.router)