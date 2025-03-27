from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

ARQUIVO = "tarefas.txt"

class Tarefa(BaseModel):
    id: int
    nome: str
    estado: str = "pendente"

class AttTarefa(BaseModel):
    nome: Optional [str] = None
    estado: Optional [str] = None

def carregar_tarefas():
    tarefas = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as file:
            for line in file:
                tarefa_id_nome, estado = line.strip().split(" - ", 1)
                tarefa_id, nome = tarefa_id_nome.split(". ", 1)
                tarefas.append({
                    "id": int(tarefa_id),
                    "nome": nome,
                    "estado": estado
                })
    return tarefas

def salvar_tarefa(tarefa: Tarefa):
    with open(ARQUIVO, "a") as file:
        file.write(f"{tarefa.id}. {tarefa.nome} - {tarefa.estado}\n")

@app.get("/tarefas")
def listar_tarefas():
    tarefas = carregar_tarefas()
    if not tarefas:
        raise HTTPException(status_code = 404, detail = "Nenhuma tarefa encontrada.")
    return tarefas

@app.get("/tarefas/{id}")
def procurar_tarefa(id: int):
    tarefas = carregar_tarefas()
    tarefa = None
    for i in tarefas:
        if i["id"] == id:
            tarefa = i
            break
    
    if tarefa is None:
        raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")
    return tarefa

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    tarefas = carregar_tarefas()

    for i in tarefas:
        if i["id"] == tarefa.id:
            raise HTTPException(status_code = 400, detail = "ID já existe.")
    
    salvar_tarefa(tarefa)
    return {"mensagem": "Tarefa criada com sucesso!", "tarefa": tarefa}

@app.patch("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: AttTarefa):
    tarefas = carregar_tarefas()
    tarefa_escolhida = None

    for i in tarefas:
        if i["id"] == id:
            if tarefa.nome is not None:
                i["nome"] = tarefa.nome
            if tarefa.estado is not None:
                i["estado"] = tarefa.estado
            tarefa_escolhida = i
            break
    
    if tarefa_escolhida is None:
        raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")
    
    with open(ARQUIVO, "w") as file:
        for i in tarefas:
            file.write(f"{i['id']}. {i['nome']} - {i['estado']}\n")

    return {"mensagem": "Tarefa atualizada com sucesso!", "tarefa": tarefa_escolhida}

@app.delete("/tarefas/{id}")
def deletar(id: int):
    tarefas = carregar_tarefas()
    tarefa_escolhida = None

    for i in tarefas:
        if i["id"] == id:
            tarefa_escolhida = i
            break

    if tarefa_escolhida is None:
            raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")
        
    tarefas.remove(tarefa_escolhida)

    with open(ARQUIVO, "w") as file:
        for i in tarefas:
            file.write(f"{i['id']}. {i['nome']} - {i['estado']}\n")
    
    return {"mensagem": "Tarefa deletada com sucesso!", "tarefas": tarefas}