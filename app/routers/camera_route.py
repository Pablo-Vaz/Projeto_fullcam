from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.database.postgre import get_db
from app.models.camera_model import Camera
from app.schemas.camera_schema import (
    CamResponseLog,
    CameraAttAll,
    CameraAttStatus,
    CameraBase,
    CameraCreate,
    CamResponseGet,
)
from app.services.cam_services import delete_cam_from_db, update_cam_service, create_cam_service, get_all_cams, get_one_cam, update_cam_status
from app.services.publish_refac import PublisherRabbitMq, get_crud
from app.services.security1 import get_user_atual

router = APIRouter(dependencies=[Depends(get_user_atual)])


@router.get("/cameras", response_model=list[CamResponseGet])
async def listar_cameras(db: AsyncSession = Depends(get_db)
) -> list[CamResponseGet]:

    return await get_all_cams(db)


@router.get("/cameras{camera_id}", response_model=CamResponseGet)
async def listar_camera(camera_id: int, db:AsyncSession = Depends(get_db)) -> CamResponseGet:
    
    return await get_one_cam(camera_id, db)


@router.post("/cameras", response_model=CamResponseLog, status_code=201)
async def criar_camera(
    camera_info: CameraCreate,
    db: AsyncSession = Depends(get_db),
    publisher: PublisherRabbitMq = Depends(get_crud),
):

    return await create_cam_service(camera_info, db, publisher)

    # new_cam = Camera(nome=camera.nome, localizacao=camera.localizacao)

    # query = select(Camera).where(Camera.nome == new_cam.nome)
    # result = await db.execute(query)
    # camera_exist = result.scalar_one_or_none()

    # if camera_exist:
    #     raise HTTPException(status_code=409, detail="Câmera ja existe")

    # try:
    #     db.add(new_cam)
    #     await db.commit()
    #     await db.refresh(new_cam)
    # except Exception:
    #     await db.rollback()
    #     raise HTTPException(status_code=500, detail="Erro ao criar câmera")
    # logs = {
    #     "id": new_cam.id,
    #     "dataehora": datetime.now().isoformat(),
    #     "action": "Criação",
    #     "description": f"Câmera '{new_cam.nome}' criada com sucesso",
    # }
    # publisher.publish(json.dumps(logs))
    # return logs


@router.put("/cameras/{camera_id}", response_model=CamResponseLog)
async def atualizar_camera(
    camera_id: int,
    camera: CameraAttAll,
    db: AsyncSession = Depends(get_db),
    publisher: PublisherRabbitMq = Depends(get_crud),
):
    
    return await update_cam_service(camera_id, camera, db, publisher)

    # camera = await db.get(Camera, camera_id)
    # if not camera:
    #     raise HTTPException(status_code=404, detail="Camera não encontrada")
    # camera.nome = dados.nome
    # camera.localizacao = dados.localizacao

    # try:
    #     await db.commit()
    #     await db.refresh(camera)
    # except Exception:
    #     await db.rollback()
    #     raise HTTPException(status_code=500, detail="Erro ao atualizar")

    # logs = {
    #     "id": camera_id,
    #     "dataehora": datetime.now().isoformat(),
    #     "action": "Atualização",
    #     "description": f"A câmera '{camera.nome}' foi atualizada com sucesso",
    # }
    # publisher.publish(json.dumps(logs))
    # return logs


@router.patch("/cameras/{camera_id}", response_model=CamResponseLog)
async def atualizar_status(
    camera_id: int,
    camera_status: CameraAttStatus,
    db: AsyncSession = Depends(get_db),
    publisher: PublisherRabbitMq = Depends(get_crud),
):
    return await update_cam_status(camera_id, camera_status, db, publisher)
    # camera = await db.get(Camera, camera_id)
    # if not camera:
    #     raise HTTPException(status_code=404, detail="Camera não encontrada")
    # camera.status = mudar.status

    # try:
    #     await db.commit()
    #     await db.refresh(camera)
    # except Exception:
    #     await db.rollback()
    #     raise HTTPException(status_code=500, detail="Erro ao atualizar")

    # logs = {
    #     "id": camera_id,
    #     "dataehora": datetime.now().isoformat(),
    #     "action": "Atualização status",
    #     "description": f"Status alterado para '{camera.status}'",
    # }
    # publisher.publish(json.dumps(logs))
    # return logs


@router.delete("/cameras/{camera_id}", response_model=CamResponseLog)
async def deletar_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db),
    publisher: PublisherRabbitMq = Depends(get_crud),
):
    return await delete_cam_from_db(camera_id, db, publisher)
    # delete_cam = await db.get(Camera, camera_id)
    # if not delete_cam:
    #     raise HTTPException(status_code=404, detail="Camera não encontrada")

    # await db.delete(delete_cam)
    # await db.commit()
    # logs = {
    #     "id": camera_id,
    #     "dataehora": datetime.now().isoformat(),
    #     "action": "Exclusão",
    #     "description": f"Camera '{delete_cam.nome}' deletada com sucesso",
    # }
    # publisher.publish(json.dumps(logs))
    # return logs
