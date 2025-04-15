from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from banco import Tarefa, session, Login
import bcrypt

app = FastAPI()

class TarefaAPI(BaseModel):
    descricao: str
    estado: str = "pendente"

class LoginAPI(BaseModel):
    usuario: str
    senha: str
class AttTarefa(BaseModel):
    descricao: Optional [str] = None
    estado: Optional [str] = None

class AttLogin(BaseModel):
    senha: str

@app.get("/tarefas")
def listar_tarefas():
    tarefas = session.query(Tarefa).all()
    if not tarefas:
        raise HTTPException(status_code = 404, detail = "Nenhuma tarefa encontrada.")
    
    lista = []
    for i in tarefas:
        dicionario = {
            "id": i.id,
            "descricao": i.descricao,
            "estado": i.estado
        }
        lista.append(dicionario)

    return lista

@app.get("/tarefas/{id}")
def procurar_tarefa(id: int):
    tarefa = session.query(Tarefa).filter(Tarefa.id == id).first()
    if not tarefa:
        raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")
    return {"id": tarefa.id, "descricao": tarefa.descricao, "estado": tarefa.estado}

@app.post("/tarefas")
def criar_tarefa(tarefa: TarefaAPI):
    nova_tarefa = Tarefa(descricao = tarefa.descricao, estado = tarefa.estado)
    session.add(nova_tarefa)
    session.commit()
    return {"mensagem": "Tarefa criada com sucesso!", "tarefa": {"id": nova_tarefa.id, "descricao": nova_tarefa.descricao, "estado": nova_tarefa.estado}}

@app.patch("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: AttTarefa):
    tarefa_escolhida = session.query(Tarefa).filter(Tarefa.id == id).first()
    if not tarefa_escolhida:
        raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")

    if tarefa.descricao is not None:
        tarefa_escolhida.descricao = tarefa.descricao
    if tarefa.estado is not None:
        tarefa_escolhida.estado =  tarefa.estado

    session.commit()
    return {"mensagem": "Tarefa atualizada com sucesso!", "tarefa": {"id": tarefa_escolhida.id, "descricao": tarefa_escolhida.descricao, "estado": tarefa_escolhida.estado}}

@app.delete("/tarefas/{id}")
def deletar(id: int):
    tarefa_escolhida = session.query(Tarefa).filter(Tarefa.id == id).first()
    if not tarefa_escolhida:
        raise HTTPException(status_code = 404, detail = "Tarefa não encontrada.")

    session.delete(tarefa_escolhida)
    session.commit()
    return {"mensagem": "Tarefa deletada com sucesso!"}

@app.get("/logins")
def listar_logins():
    logins = session.query(Login).all()
    
    if not logins:
        raise HTTPException(status_code = 404, detail = "Nenhum login encontrado.")
    
    lista_logins = []
    for i in logins:
        dicionario_logins = {
            "id": i.id,
            "usuario": i.usuario
        }
        lista_logins.append(dicionario_logins)

    return lista_logins

@app.get("/logins/{usuario}")
def buscar_login(usuario: str):
    login = session.query(Login).filter(Login.usuario == usuario).first()
    
    if not login:
        raise HTTPException(status_code = 404, detail = "Login não encontrado.")
    return {"id": login.id, "usuario": login.usuario}

@app.post("/logins")
def criar_login(login: LoginAPI):
    if session.query(Login).filter(Login.usuario == login.usuario).first():
        raise HTTPException(status_code = 400, detail = "Usuário já existe.")

    senha_bytes = login.senha.encode("utf-8")
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    novo_login = Login(usuario = login.usuario, senha = senha_hash.decode("utf-8"))
    session.add(novo_login)
    session.commit()
    return {"menssagem": "Login criado com sucesso!", "login": {"id": novo_login.id, "usuario": novo_login.usuario}}

@app.post("/login")
def autenticar(login: LoginAPI):
    usuario = session.query(Login).filter(Login.usuario == login.usuario).first()
    
    if not usuario:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado.")
    
    senha_bytes = login.senha.encode("utf-8")
    senha_banco_bytes = usuario.senha.encode("utf-8")

    if not bcrypt.checkpw(senha_bytes, senha_banco_bytes):
        raise HTTPException(status_code = 401, detail = "Usuário ou senha incorretos.")
    
    return {"mensagem": "Login bem-sucedido!"}

@app.patch("/logins/{usuario}")
def atualizar_login(usuario: str, att_login: AttLogin):
    login_escolhido = session.query(Login).filter(Login.usuario == usuario).first()

    if not login_escolhido:
        raise HTTPException(status_code = 404, detail = "Login não encontrado.")
    
    nova_senha_bytes = att_login.senha.enocode("utf-8")
    salt = bcrypt.gensalt()
    nova_senha_hash = bcrypt(nova_senha_bytes, salt)

    login_escolhido.senha = nova_senha_hash.decode("utf-8")
    session.commit()
    return {"mensagem": "Senha atualizada com sucesso!"}

@app.delete("/logins/{usuario}")
def deletar_login(usuario: str):
    login_escolhido = session.query(Login).filter(Login.usuario == usuario).first()

    if not login_escolhido:
        raise HTTPException(status_code = 404, detail = "Login não encontrado.")
    
    session.delete(login_escolhido)
    session.commit()
    return {"mensagem": "Login deletado com sucesso!"}