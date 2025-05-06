
from pydantic import BaseModel
from datetime import datetime

class Aviao(BaseModel):
    modelo: str
    qtd_passageiros: int
