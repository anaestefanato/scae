from fastapi import APIRouter, Request, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os
from datetime import datetime

from repo import usuario_repo, recebimento_repo
from util.auth_decorator import obter_usuario_logado, requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/recebimentos")
@requer_autenticacao(["aluno"])
async def get_recebimentos(request: Request, usuario_logado: dict = None):
    if not usuario_logado['completo']:
        return RedirectResponse("/aluno/perfil", status_code=303)
    
    aluno = usuario_repo.obter_usuario_por_matricula(usuario_logado['matricula'])
    recebimentos = recebimento_repo.obter_por_aluno(usuario_logado['id'])

    response = templates.TemplateResponse("/aluno/recebimentos.html", {
        "request": request, 
        "aluno": aluno,
        "recebimentos": recebimentos
    })
    return response


@router.post("/recebimentos/confirmar/{mes_referencia}/{ano_referencia}")
@requer_autenticacao(["aluno"])
async def post_confirmar_recebimento(
    request: Request,
    mes_referencia: str,
    ano_referencia: int,
    usuario_logado: dict = None,
    comprovante_transporte: Optional[UploadFile] = File(None),
    comprovante_moradia: Optional[UploadFile] = File(None)
):
    try:
        # Processar uploads de comprovantes
        path_transporte = None
        path_moradia = None
        
        upload_dir = "static/uploads/comprovantes"
        os.makedirs(upload_dir, exist_ok=True)
        
        if comprovante_transporte and comprovante_transporte.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transporte_{usuario_logado['id']}_{mes_referencia}_{ano_referencia}_{timestamp}_{comprovante_transporte.filename}"
            path_transporte = os.path.join(upload_dir, filename)
            with open(path_transporte, "wb") as f:
                content = await comprovante_transporte.read()
                f.write(content)
        
        if comprovante_moradia and comprovante_moradia.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"moradia_{usuario_logado['id']}_{mes_referencia}_{ano_referencia}_{timestamp}_{comprovante_moradia.filename}"
            path_moradia = os.path.join(upload_dir, filename)
            with open(path_moradia, "wb") as f:
                content = await comprovante_moradia.read()
                f.write(content)
        
        # Confirmar todos os recebimentos do mês
        sucesso = recebimento_repo.confirmar_recebimentos_mes(
            usuario_logado['id'],
            mes_referencia, 
            ano_referencia,
            path_transporte, 
            path_moradia
        )
        
        if sucesso:
            request.session['sucesso'] = "Recebimento confirmado com sucesso!"
        else:
            request.session['erro'] = "Erro ao confirmar recebimento"
        
        return RedirectResponse("/aluno/recebimentos", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        print(f"Erro ao confirmar recebimento: {e}")
        request.session['erro'] = f"Erro ao processar confirmação: {str(e)}"
        return RedirectResponse("/aluno/recebimentos", status_code=status.HTTP_303_SEE_OTHER)


