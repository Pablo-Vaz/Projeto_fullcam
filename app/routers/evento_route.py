import re
from fastapi import APIRouter,HTTPException
from app.schemas.camera_schema import EventoDetectarPessoa, EventoLeituraPlaca
from app.services.publisher_evento import publicar

router = APIRouter()


@router.post('/eventos/placa', status_code=201)
async def criar_evento_leitura_de_placa(evento_placa: EventoLeituraPlaca):
    placa = str(evento_placa.placa.replace("-", "").strip().upper())
    
    padrao_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')
    padrao_mercosul = re.compile(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$')

    eventos = evento_placa.model_dump_json(ensure_ascii=False)

    if not padrao_antigo.match(placa) or padrao_mercosul.match(placa):
        raise HTTPException(status_code=404, detail='Placa incorreta')
    
    publicar(eventos)
    return "Enviado para a fila"

@router.post('/eventos/detectar_pessoa', status_code=201)
async def criar_evento_detectar_pessoa(evento_pessoa: EventoDetectarPessoa):
    evento = evento_pessoa.model_dump_json(ensure_ascii=False)
    try:
        publicar(evento)
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao publicar evento")
    return "sucesso"
    

    