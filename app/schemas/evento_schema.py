from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, HttpUrl


class EventoLeituraPlaca(BaseModel):
    dataehora: datetime
    placa: str
    model_config = ConfigDict(from_attributes=True)


class EventoBase(BaseModel):
    camera_id: int
    event_type: str
    timestamp: datetime


class BoundingBox(BaseModel):
    top: int
    left: int
    width: int
    height: int


class EventoDetectarPessoa(EventoBase):
    confidence: float
    roi_name: str
    bounding_box: BoundingBox
    model_config = ConfigDict(from_attributes=True)


class EventoDetectarMovimento(EventoBase):
    status: str
    target_type: str
    snapshot_url: HttpUrl
    area_detected: List
