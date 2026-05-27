from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.postgre import get_db
from app.models.camera_model import Camera
from app.schemas.camera_schema import (
    CameraAttAll,
    CameraAttStatus,
    CameraBase,
    CameraCreate,
)


async def select_all_cams(db: AsyncSession):
    query = select(Camera)
    result = await db.execute(query)

    return result.scalars().all()


async def select_cam_by_id(db: AsyncSession, camera_id: int):
    query = select(Camera).where(Camera.id == camera_id)
    result = await db.execute(query)

    return result.scalar_one_or_none()


async def select_cam_by_name(db: AsyncSession, camera_name: str):
    query = select(Camera).where(Camera.nome == camera_name)
    result = await db.execute(query)

    return result.scalar_one_or_none()


async def create_cam(camera_info: CameraCreate, db: AsyncSession):
    camera = Camera(nome=camera_info.nome, localizacao=camera_info.localizacao)
    db.add(camera)
    await db.commit()
    await db.refresh(camera)

    return camera


async def update_cam_status_repository(
    camera: CameraBase, camera_status: CameraAttStatus, db: AsyncSession
):
    camera.status = camera_status.status
    await db.commit()
    await db.refresh(camera)

    return camera


async def update_cam_service_repository(
    camera: CameraBase, camera_info: CameraAttAll, db: AsyncSession
):
    camera.nome = camera_info.nome
    camera.localizacao = camera_info.localizacao
    await db.commit()
    await db.refresh(camera)

    return camera


async def delete_cam(camera: Camera, db: AsyncSession):

    await db.delete(camera)
    await db.commit()

    return camera
