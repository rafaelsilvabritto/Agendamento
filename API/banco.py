from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os

ARQUIVO = "tarefas.txt"

banco = create_engine("sqlite:///tarefas.banco")
Session = sessionmaker(bind = banco)
session = Session()

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    descricao = Column("descricao", String)
    estado = Column("estado", String)

    def __init__(self, descricao, estado):
        self.descricao = descricao
        self.estado = estado

class Login(Base):
    __tablename__ = "logins"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    usuario = Column("usuario", String, unique = True, nullable = False)
    senha = Column("senha", String, nullable = False)

    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha

Base.metadata.create_all(bind = banco)