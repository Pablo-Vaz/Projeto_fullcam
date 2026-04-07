from datetime import datetime
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.database.postgre import get_db
from app.models.camera_model import Camera
from app.schemas.camera_schema import (
    CamResponseLog,
    CameraAttAll,
    CameraAttStatus,
    CameraCriar,
    CamResponseGet,
)
from app.services.publisher_rabbit import PublisherRabbitMq, get_crud
from app.services.security import get_user


router = APIRouter()


@router.get("/cameras", response_model=list[CamResponseGet])
async def listar_cameras(
    db: AsyncSession = Depends(get_db), user: str = Depends(get_user)
) -> list[CamResponseGet]:
    action = select(Camera)
    result = await db.execute(action)
    cameras = result.scalars().all()
    if not cameras:
        raise HTTPException(status_code=404, detail="Nenhuma câmera encontrada")
    return cameras


@router.get("/cameras{camera_id}", response_model=CamResponseGet)
async def listar_camera(
    camera_id: int, db: AsyncSession = Depends(get_db), user: str = Depends(get_user)
) -> CamResponseGet:
    action = select(Camera).where(Camera.id == camera_id)
    result = await db.execute(action)
    camera = result.scalar_one_or_none()
    if not camera:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    return camera


@router.post("/cameras", response_model=CamResponseLog, status_code=201)
async def criar_camera(
    camera: CameraCriar,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_user),
    publisher: PublisherRabbitMq = Depends(get_crud),
) -> CamResponseLog:
    new_cam = Camera(nome=camera.nome, localizacao=camera.localizacao)

    query = select(Camera).where(Camera.nome == new_cam.nome)
    result = await db.execute(query)
    camera_exist = result.scalar_one_or_none()

    if camera_exist:
        raise HTTPException(status_code=409, detail="Câmera ja existe")

    try:
        db.add(new_cam)
        await db.commit()
        await db.refresh(new_cam)
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


@router.put("/cameras/{camera_id}", response_model=CamResponseLog)
async def atualizar_camera(
    camera_id: int,
    dados: CameraAttAll,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_user),
    publisher: PublisherRabbitMq = Depends(get_crud),
) -> CamResponseLog:
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera não encontrada")
    camera.nome = dados.nome
    camera.localizacao = dados.localizacao

    try:
        await db.commit()
        await db.refresh(camera)
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


@router.patch("/cameras/{camera_id}", response_model=CamResponseLog)
async def atualizar_status(
    camera_id: int,
    mudar: CameraAttStatus,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_user),
    publisher: PublisherRabbitMq = Depends(get_crud),
) -> CamResponseLog:
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera não encontrada")
    camera.status = mudar.status

    try:
        await db.commit()
        await db.refresh(camera)
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


@router.delete("/cameras/{camera_id}", response_model=CamResponseLog)
async def deletar_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_user),
    publisher: PublisherRabbitMq = Depends(get_crud),
) -> CamResponseLog:
    delete_cam = await db.get(Camera, camera_id)
    if not delete_cam:
        raise HTTPException(status_code=404, detail="Camera não encontrada")

    await db.delete(delete_cam)
    await db.commit()
    logs = {
        "id": camera_id,
        "dataehora": datetime.now().isoformat(),
        "action": "Exclusão",
        "description": f"Camera '{delete_cam.nome}' deletada com sucesso",
    }
    publisher.publish(json.dumps(logs))
    return logs
