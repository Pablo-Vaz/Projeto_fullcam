import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt





load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = 30


def criar_token_acesso(data: dict, time_diff: timedelta | None = None):
    encode = data.copy() #criando uma copia 

    if time_diff:
        expire = datetime.now(timezone.utc) + time_diff
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)


    encode.update({"exp": expire}) #adicionando a variavel de expiração na cópia

    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) #transformando para jwt
    return encoded_jwt


"""Injeção de dependencia"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") #apontando a rota do token


async def get_user_atual(token: str = Depends(oauth2_scheme)):
    try:
        valid_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = valid_token.get("sub")
        return username

    except JWTError:
        raise HTTPException (status_code=401, detail="Token inválido")
    