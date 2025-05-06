from pydantic import BaseModel
from datetime import datetime

class Reserva(BaseModel):
    nome_cliente: str
    cpf: str
    id_voo: int

