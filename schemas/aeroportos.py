from pydantic import BaseModel

class Aeroporto(BaseModel):
    nome: str
    endereco: str
    sigla: str
