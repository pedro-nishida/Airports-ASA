from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Aeroportos(Base):
    __tablename__ = 'aeroportos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    endereco = Column(String(255), nullable=False)
    sigla = Column(String(3), nullable=False, unique=True)

    def __str__(self):
        return f"AEROPORTO:\n\nNome: {self.nome} ({self.sigla})\nEndereço: {self.endereco}"