import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.usuarios import TokenTable

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 dias
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # manter em segredo
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

def decodificar_JWT(jwtoken: str):
    try:
        # Decodificar e verificar o token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except InvalidTokenError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Schema de autorização inválido.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token ou token expirado inválido.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Código de autorização inválido.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodificar_JWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

jwt_bearer = JWTBearer()
