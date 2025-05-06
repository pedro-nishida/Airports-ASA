import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 dias
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # manter em segredo
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_senha_hashed(password: str) -> str:
    return password_context.hash(password)


def verificar_senha(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def criar_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
        
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encoded_jwt

def verifica_token_expirado(token: str, secret_key: str, algorithm: str) -> bool:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.utcnow() > datetime.utcfromtimestamp(exp)
    except JWTError:
        return True

def criar_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt