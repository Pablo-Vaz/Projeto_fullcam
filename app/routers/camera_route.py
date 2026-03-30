from datetime import datetime
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from app.database.postgre import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.camera_model import Camera
from app.schemas.camera_schema import CameraAttStatus, CameraResponse, CameraResposta, CameraCriarAtt
from app.services.publisher_rabbit import PublisherRabbitMq
from app.services.security import get_user



router = APIRouter(tags=["CRUD ROUTE"])


@router.get('/cameras', response_model=list[CameraResposta])
async def listar_cameras(db: AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    action = select(Camera)
    result = await db.execute(action)
    cameras = result.scalars().all()
    if not cameras:
        raise HTTPException(status_code=404, detail="Nenhuma câmera encontrada")
    return cameras


@router.get('/cameras{camera_id}', response_model=CameraResposta)
async def listar_camera(camera_id: int, db: AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    action = select(Camera).where(Camera.id == camera_id)
    result = await db.execute(action)
    camera = result.scalar_one_or_none()
    if not camera:
        raise HTTPException(status_code=404, detail='Câmera não encontrada')
    return camera


@router.post('/cameras', response_model=CameraResponse, status_code=201)
async def criar_camera(camera: CameraCriarAtt, db: AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    new_cam = Camera(
        nome = camera.nome,
        localizacao = camera.localizacao
    )
    db.add(new_cam)
    try:
        await db.commit()
        await db.refresh(new_cam)
    except Exception:
        await db.rollback()
        raise HTTPException (status_code=500, detail="Erro ao criar câmera")
    logs = {
        "id": new_cam.id,
        "dataehora": datetime.now().isoformat(),
        "action": "Criação",
        "description": f"Câmera '{new_cam.nome}' criada com sucesso"
    }
    rabbit_crud= PublisherRabbitMq('crud_exchange','crud_queue','fanout','crud')
    rabbit_crud.init_conn()
    rabbit_crud.publish(logs)
    return logs


@router.put('/cameras/{camera_id}', response_model=CameraResponse)
async def atualizar_camera(camera_id: int,dados: CameraCriarAtt, db: AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail='Camera não encontrada')
    camera.nome = dados.nome
    camera.localizacao = dados.localizacao
    try:
        await db.commit()
        await db.refresh(camera)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar")
    
    logs = {
        "id": camera.id,
        "dataehora": datetime.now().isoformat(),
        "action":"Atualização",
        "description":f"A câmera '{camera.nome}' foi atualizada com sucesso"
    }
    rabbit_crud= PublisherRabbitMq('crud_exchange','crud_queue','fanout','crud')
    rabbit_crud.init_conn()
    rabbit_crud.publish(logs)
    return logs

@router.patch('/cameras/{camera_id}', response_model=CameraResponse)
async def atualizar_status(camera_id: int, mudar: CameraAttStatus, db: AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail='Camera não encontrada')
    camera.status = mudar.status
    
    try:
        await db.commit()
        await db.refresh(camera)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar")
    
    logs = {
        "id": camera.id,
        "dataehora": datetime.now().isoformat(),
        "action":"Atualização status",
        "description":f"Status alterado para '{camera.status}'"
    }
    rabbit_crud= PublisherRabbitMq('crud_exchange','crud_queue','fanout','crud')
    rabbit_crud.init_conn()
    rabbit_crud.publish(logs)
    return logs


@router.delete('/cameras/{camera_id}',response_model=CameraResponse)
async def deletar_camera(camera_id: int, db:AsyncSession = Depends(get_db), user: str = Depends(get_user)):
    delete_cam = await db.get(Camera, camera_id)
    if not delete_cam:
        raise HTTPException(status_code=404, detail='Camera não encontrada')
    
    await db.delete(delete_cam)
    await db.commit()
    logs = {
        "id": delete_cam.id,
        "dataehora": datetime.now().isoformat(),
        "action": "Exclusão",
        "description": f"Camera '{delete_cam.nome}' deletada com sucesso"
    }
    rabbit_crud= PublisherRabbitMq('crud_exchange','crud_queue','fanout','crud')
    rabbit_crud.init_conn()
    rabbit_crud.publish(logs)
    return logs

    

