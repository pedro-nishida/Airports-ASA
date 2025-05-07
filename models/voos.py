from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey, Float
from .database import Base

class Voos(Base):
    __tablename__ = 'voos'

    id = Column(Integer, primary_key=True, nullable=False)
    aeroporto_origem = Column(String(3), ForeignKey('aeroportos.sigla'), nullable=False)
    aeroporto_destino = Column(String(3), ForeignKey('aeroportos.sigla'), nullable=False)
    data = Column(String(10), nullable=False)
    assentos_disponiveis = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    id_aviao = Column(Integer, ForeignKey('avioes.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    def __str__(self): 
        return f"Aeroporto de Origem: {self.aeroporto_origem}, Aeroporto de Destino: {self.aeroporto_destino}, Assentos Disponíveis: {self.assentos_disponiveis}, Data: {self.data}, Preço: {self.preco:.2f}, ID do Avião: {self.id_aviao}"