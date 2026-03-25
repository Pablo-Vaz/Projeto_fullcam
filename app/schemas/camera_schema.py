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

class EventoLeituraPlaca(BaseModel):
    dataehora: datetime
    placa: str
    model_config = ConfigDict(from_attributes=True)


class BoundingBox(BaseModel):
    top: int
    left: int
    width: int
    height: int

class EventoDetectarPessoa(BaseModel):
    camera_id: int
    event_type: str
    timestamp: datetime
    confidence: float
    roi_name: str
    bounding_box: BoundingBox
    model_config = ConfigDict(from_attributes=True)


class EventoDetectarMovimento(BaseModel):
    event: str
    camera_id: int
    timestamp: datetime
    status: str
    target_type: str
    snapshot_url: HttpUrl
    area_detected: list 



