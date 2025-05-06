from pydantic import BaseModel
import datetime
class CriarUsuario(BaseModel):
    nome: str
    email: str
    senha: str

class RequestDetails(BaseModel):
    email:str
    senha:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class MudarSenha(BaseModel):
    email:str
    senha_antiga:str
    senha_nova:str

class TokenCreate(BaseModel):
    id_usuario:str
    access_token:str
    refresh_token:str
    status:bool
    data_de_criacao:datetime.datetime