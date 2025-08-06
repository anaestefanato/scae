from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import resposta_chamado_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/aluno/chamado/respostas")
async def get_root(request: Request):
    resposta_chamado = resposta_chamado_repo.obter_por_pagina()
    response = templates.TemplateResponse("/resposta_chamado/resposta_chamado.html", {"request": request, "respostas": resposta_chamado})
    return response

@router.get("/aluno/chamado/respostas/{id_resposta_chamado}")
async def get(request: Request, id_resposta_chamado: int):
    resposta_chamado = resposta_chamado_repo.obter_por_id(id_resposta_chamado)
    response = templates.TemplateResponse("/resposta_chamado/resposta_chamado.html", {"request": request, "resposta": resposta_chamado})
    return response

@router.get("/aluno/chamado/respostas/atualizar/{id_resposta_chamado}")
async def get(request: Request, id_resposta_chamado: int):
    resposta_chamado = resposta_chamado_repo.atualizar(id_resposta_chamado)
    response = templates.TemplateResponse("/resposta_chamado/resposta_chamado.html", {"request": request, "resposta": resposta_chamado})
    return response