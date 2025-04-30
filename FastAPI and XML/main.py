from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path
from xml.etree import ElementTree as ET

class Livro(BaseModel):
    id:int
    titulo:str
    autor:str
    ano:int
    genero:str

pasta = Path('db')
pasta.mkdir(exist_ok=True)

LIVROS_XML = pasta / 'livros.xml'

if not LIVROS_XML.exists():
    root = ET.Element("livros")
    tree = ET.ElementTree(root)
    tree.write(LIVROS_XML)


app = FastAPI()

#Lê o XML e retorna uma lista de Livros
def readXml():
    livros = []
    tree = ET.parse(LIVROS_XML)
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
    tree.write(LIVROS_XML)


def update_livro(livro_id: int, livro:Livro):
    tree = ET.parse(LIVROS_XML)
    root = tree.getroot()
    
    for l in root.findall("livro"):
        print(int(l.find("id").text))
        if int(l.find("id").text) == livro_id:
            if livro.id != livro_id:
                livro.id = livro_id
            l.find("titulo").text = livro.titulo
            l.find("autor").text = livro.autor
            l.find("ano").text = str(livro.ano)
            l.find("genero").text = livro.genero
            tree.write(LIVROS_XML)
            return livro
    raise HTTPException(status_code=404,detail="ID não foi encontrado")
    


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
    
    for livro in livros:
        if livro.id == livroId:
            return livro
    raise HTTPException(status_code=400,detail='Livro não encontrado')

@app.put("/livros/{livro_id}", response_model=Livro)
def update_book_by_id(livro_id:int,book:Livro):
    return update_livro(livro_id,book)
    
    
@app.delete("/livros/{livro_id}")
def delete_book_by_id(livro_id:int):
    books = readXml()
    if not any(l.id == livro_id for l in books):
        raise HTTPException(status_code=404,detail="ID não existe")
    new_books = [book for book in books if book.id != livro_id]
    writeXml(new_books)
    return {"msg":f"Livro de id {livro_id} foi apagado."}
    