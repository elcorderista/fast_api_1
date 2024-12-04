import os
from dotenv import load_dotenv
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from starlette import status

from settings.config import Settings
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, Depends

settings = Settings()
load_dotenv()
key_secret = settings.jwt_secret_key
algorithm = settings.jwt_algorithm

def createToken(data: dict):
    token = encode(
        payload=data,
        key=key_secret,
        algorithm=algorithm
    )
    return token

def validateToken(token: str) -> dict:
    data: dict = decode(token, key=key_secret, algorithms=algorithm)
    return data

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        token = auth.credentials
        print(token)
        try:
            payload = decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
            print(payload)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

def get_current_user(payload: dict = Depends(BearerJWT())):
    print(payload)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or payload is missing"
        )

    if not payload.get('email') or not payload.get('id'):
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    return payload
