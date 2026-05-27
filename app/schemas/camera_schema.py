from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.camera_model import StatusCamera


class CameraBase(BaseModel):
    nome: str
    localizacao: str
    status: StatusCamera


class CameraCreate(BaseModel):
    nome: str
    localizacao: str


class CameraAttAll(BaseModel):
    nome: str
    localizacao: str


class CameraAttStatus(BaseModel):
    status: StatusCamera


class CamResponseGet(CameraBase):
    id: int
    status: StatusCamera
    model_config = ConfigDict(from_attributes=True)


class CamResponseLog(BaseModel):
    id: int
    dataehora: datetime
    action: str
    description: str
