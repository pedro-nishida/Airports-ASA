
from sqlalchemy import Column, Integer, String, DateTime,Boolean
from models.database import Base
import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)

class TokenTable(Base):
    __tablename__ = "token"
    id_usuario = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    data_de_criacao = Column(DateTime, default=datetime.datetime.now)