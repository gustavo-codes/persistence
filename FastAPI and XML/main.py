from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path
from xml.etree import ElementTree as ET

class Livro(BaseModel):
    id:int
    titulo:str
    autor:str
    ano:int
    genero:str

app = FastAPI()

#Lê o XML e retorna uma lista de Livros
def readXml():
    livros = []
    tree = ET.parse('livros.xml')
    root = tree.getroot()
    
    for elem in root.findall('livro'):
        livro = Livro(
            id = int(elem.find('id').text),
            titulo = elem.find('titulo').text,
            autor = elem.find('autor').text,
            ano = int(elem.find('ano').text),
            genero = elem.find('genero').text
        )
        livros.append(livro)
    return livros

#Lê uma lista de Livros e escreve no arquivo XML
def writeXml(livros):
    root = ET.Element('livros')

    for livro in livros:

        livroElement = ET.SubElement(root,'livro')
        ET.SubElement(livroElement,'id').text = str(livro.id)
        ET.SubElement(livroElement,'titulo').text = livro.titulo
        ET.SubElement(livroElement,'autor').text = livro.autor
        ET.SubElement(livroElement,'ano').text = str(livro.ano)
        ET.SubElement(livroElement,'genero').text = livro.genero

        tree = ET.ElementTree(root)
        tree.write('livros.xml')

@app.get('/livros/',response_model=List[Livro])
def getLivros():
    return readXml()

@app.post('/livros/', response_model=Livro)
def addLivro(livro:Livro):
    livros = readXml()
    
    if any(l.id == livro.id for l in livros):
       raise HTTPException(status_code=400,detail='Livro já existe')
    
    livros.append(livro)
    writeXml(livros)
    return livro

@app.get('/livros/{livroId}',response_model=Livro)
def getLivro(livroId:int):
    livros = readXml()
    
    if not any(l.id == livroId for l in livros):
       raise HTTPException(status_code=400,detail='Livro não encontrado')

    for livro in livros:
        if livro.id == livroId:
            return livro