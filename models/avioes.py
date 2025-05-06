from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Avioes(Base):
    __tablename__ = 'avioes'
    id = Column(Integer, primary_key=True, nullable=False)
    modelo = Column(String(100), nullable=False)
    qtd_passageiros = Column(Integer, nullable=False)

    def __str__(self):
        return f"AVIÕES:\n\nModelo: {self.modelo}\nQuantidade de Passageiros: {self.qtd_passageiros}"