from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Reservas(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True, nullable=False)
    nome_cliente = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False)
    id_voo = Column(Integer, ForeignKey('voos.id'), nullable=False)

    def __str__(self):
        return f"Nome do Cliente: {self.nome_cliente}, CPF: {self.cpf}, ID do Voo: {self.id_voo}"