from pydantic import BaseModel
from datetime import datetime

class Voo(BaseModel):
    aeroporto_origem: str
    aeroporto_destino: str
    assentos_disponiveis: int
    data: str
    preco: float
    id_aviao: int
    