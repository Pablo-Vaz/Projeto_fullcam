from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.security1 import criar_token_acesso

router = APIRouter()

fake_user = {
    "username": "admin",
    "password": "123456"
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(
            status_code=401,
            detail="Nome ou senha incorretos")
    access_token = criar_token_acesso(
        data={"sub": form_data.username}
    )
    return {"access_token": access_token, "token_type":"bearer"}