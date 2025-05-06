from fastapi import FastAPI
from typing import Optional
from routers.aeroportos import router as router_aeroportos
from routers.avioes import router as router_avioes
from routers.voos import router as router_voos
from routers.reservas import router as router_reserva
from models.usuarios import Usuario,TokenTable
from models.database import Base, engine, SessionLocal
import schemas.usuarios as schemas
import models.usuarios as models
import jwt
from datetime import datetime 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.auth_bearer import JWTBearer
from functools import wraps
from app.utils import criar_access_token,criar_refresh_token,verificar_senha,get_senha_hashed,verifica_token_expirado


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 dias
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # manter em segredo
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
app=FastAPI()

@app.get('/usuarios')
def get( dependencies=Depends(JWTBearer()),session: Session = Depends(get_session)):
    usuario = session.query(models.Usuario).all()
    return usuario

@app.put('/mudar-senha')
def mudar_senha(request: schemas.MudarSenha, db: Session = Depends(get_session)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == request.email).first()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado")
    
    if not verificar_senha(request.senha_antiga, usuario.senha):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha antiga incorreta")
    
    senha_encriptada = get_senha_hashed(request.senha_nova)
    usuario.senha = senha_encriptada
    db.commit()
    
    return {"message": "Senha mudada com sucesso"}

@app.get('/verifica_token')
def verifica_token(dependencies=Depends(JWTBearer())):
    if verifica_token_expirado(dependencies,JWT_SECRET_KEY,ALGORITHM):
        return {"message":"Token expirado"}
    return {"message":"Token válido"}

@app.post('/login' ,response_model=schemas.TokenSchema)
def login(request: schemas.RequestDetails, db: Session = Depends(get_session)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto")
    hashed_pass = usuario.senha
    if not verificar_senha(request.senha, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )
    
    access = criar_access_token(usuario.id)
    refresh = criar_refresh_token(usuario.id)

    token_db = models.TokenTable(id_usuario=usuario.id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }

@app.post("/registrar_usuario")
def registrar_usuario(usuario: schemas.CriarUsuario, session: Session = Depends(get_session)):
    existing_usuario = session.query(models.Usuario).filter_by(email=usuario.email).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    senha_encriptada = get_senha_hashed(usuario.senha)

    novo_usuario = models.Usuario(nome=usuario.nome, email=usuario.email, senha=senha_encriptada )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return {"message":"Usuário criado com sucesso"}

@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token=dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    id_usuario = payload['sub']
    token_record = db.query(models.TokenTable).all()
    info=[]
    for record in token_record :
        print("record",record)
        if (datetime.utcnow() - record.data_de_criacao).days >1:
            info.append(record.id_usuario)
    if info:
        existing_token = db.query(models.TokenTable).where(TokenTable.id_usuario.in_(info)).delete()
        db.commit()
        
    existing_token = db.query(models.TokenTable).filter(models.TokenTable.id_usuario == id_usuario, models.TokenTable.access_token==token).first()
    if existing_token:
        existing_token.status=False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message":"Logout executado com sucesso"}

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
    
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        id_usuario = payload['sub']
        data= kwargs['session'].query(models.TokenTable).filter_by(id_usuario=id_usuario,access_token=kwargs['dependencies'],status=True).first()
        if data:
            return func(kwargs['dependencies'],kwargs['session'])
        
        else:
            return {'msg': "Token bloqueado"}
        
    return wrapper


Base.metadata.create_all(bind=engine)

app.include_router(router_aeroportos)
app.include_router(router_avioes)
app.include_router(router_voos)
app.include_router(router_reserva)
