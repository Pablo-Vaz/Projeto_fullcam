from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass

class StatusCamera(enum.Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'

class Camera(Base):
    __tablename__= 'cameras'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True)
    localizacao = Column(String(50))
    status = Column(Enum(StatusCamera), default=StatusCamera.OFFLINE)



