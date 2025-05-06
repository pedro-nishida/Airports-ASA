from pydantic import BaseModel
from datetime import datetime

class Voo(BaseModel):
    aeroporto_origem: int
    aeroporto_destino: int
    assentos_disponiveis: int
    data: str
    preco: float
    id_aviao: int
    