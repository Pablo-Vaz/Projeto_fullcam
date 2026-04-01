from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, HttpUrl


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
    area_detected: List
