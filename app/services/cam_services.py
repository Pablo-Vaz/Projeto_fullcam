from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.database.postgre import get_db
from app.models.camera_model import Camera
from app.schemas.camera_schema import CameraAttStatus, CameraBase, CameraCreate, CameraAttAll
from app.database.repository import (
    select_cam_by_name,
    create_cam,
    select_all_cams,
    select_cam_by_id,
    update_cam_service_repository,
    update_cam_status_repository,
    delete_cam,
)

from fastapi import HTTPException
from datetime import datetime
import json

from app.services.publish_refac import PublisherRabbitMq


async def get_all_cams(db: AsyncSession):
    cameras = await select_all_cams(db)

    if not cameras:
        raise HTTPException(status_code=404, detail="Nenhuma câmera encontrada")
    return cameras


async def get_one_cam(camera_id: int, db: AsyncSession):
    camera = await select_cam_by_id(db, camera_id)

    if not camera:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    return camera


async def create_cam_service(
    camera_info: CameraCreate, db: AsyncSession, publisher: PublisherRabbitMq
):
    camera = await select_cam_by_name(db, camera_info.nome)

    if camera:
        raise HTTPException(status_code=409, detail="Câmera ja existe")

    try:
        new_cam = await create_cam(camera_info, db)

    except Exception:
        await db.rollback()

        raise HTTPException(status_code=500, detail="Erro ao criar câmera")

    logs = {
        "id": new_cam.id,
        "dataehora": datetime.now().isoformat(),
        "action": "Criação",
        "description": f"Câmera '{new_cam.nome}' criada com sucesso",
    }

    publisher.publish(json.dumps(logs))

    return logs


async def update_cam_service(
    camera_id: int,
    camera_info: CameraAttAll,
    db: AsyncSession,
    publisher: PublisherRabbitMq,
):
    camera = await select_cam_by_id(db, camera_id)

    if not camera:
        raise HTTPException(status_code=404, detail="Camera não encontrada")

    
    try:
        camera = await update_cam_service_repository(camera, camera_info, db)

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar")

    logs = {
        "id": camera_id,
        "dataehora": datetime.now().isoformat(),
        "action": "Atualização",
        "description": f"A câmera '{camera.nome}' foi atualizada com sucesso",
    }
    publisher.publish(json.dumps(logs))

    return logs


async def update_cam_status(
    camera_id: int,
    camera_status: CameraAttStatus,
    db: AsyncSession,
    publisher: PublisherRabbitMq,
):
    camera = await select_cam_by_id(db, camera_id)

    if not camera:
        raise HTTPException(status_code=404, detail="Camera não encontrada")

    try:
        camera = await update_cam_status_repository(camera, camera_status, db)

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar")

    logs = {
        "id": camera_id,
        "dataehora": datetime.now().isoformat(),
        "action": "Atualização status",
        "description": f"Status alterado para '{camera.status}'",
    }
    publisher.publish(json.dumps(logs))

    return logs


async def delete_cam_from_db(
    camera_id: int, 
    db: AsyncSession, 
    publisher: PublisherRabbitMq
):
    try:
        camera = await select_cam_by_id(db, camera_id)
        camera = await delete_cam(camera, db)

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao excluir")
    
    logs = {
        "id": camera_id,
        "dataehora": datetime.now().isoformat(),
        "action": "Exclusão",
        "description": f"Camera '{camera.nome}' deletada com sucesso",
    }
    publisher.publish(json.dumps(logs))
    return logs
