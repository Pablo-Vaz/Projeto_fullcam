from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()

username = "pablo"
passwords = "teste"


async def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != username or credentials.password != passwords:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return credentials.username
