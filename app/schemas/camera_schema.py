from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime
from app.models.camera_model import StatusCamera

class CameraCriarAtt(BaseModel):
    nome: str
    localizacao: str

class CameraAttStatus(BaseModel):
    status: StatusCamera

class CameraResposta(BaseModel):
    id: int
    nome: str
    localizacao: str
    status: str
    model_config = ConfigDict(from_attributes=True)

class CameraResponse(BaseModel):
    id: int
    dataehora: datetime
    action: str
    description: str