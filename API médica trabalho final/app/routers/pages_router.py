"""
Roteador para renderização das páginas HTML da interface web.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import os

from app.auth import obter_usuario_opcional
from app.config import CAMINHO_BASE
from app.models import Usuario

roteador_paginas = APIRouter(include_in_schema=False)

caminho_templates = os.path.join(CAMINHO_BASE, "templates")
templates = Jinja2Templates(directory=caminho_templates)


@roteador_paginas.get("/")
def pagina_inicial(request: Request, usuario: Usuario = Depends(obter_usuario_opcional)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"usuario": usuario}
    )


@roteador_paginas.get("/anamnese")
def pagina_anamnese(request: Request, usuario: Usuario = Depends(obter_usuario_opcional)):
    return templates.TemplateResponse(
        request=request,
        name="anamnese.html",
        context={"usuario": usuario}
    )


@roteador_paginas.get("/resultado")
def pagina_resultado(request: Request, usuario: Usuario = Depends(obter_usuario_opcional)):
    return templates.TemplateResponse(
        request=request,
        name="resultado.html",
        context={"usuario": usuario}
    )


@roteador_paginas.get("/historico")
def pagina_historico(request: Request, usuario: Usuario = Depends(obter_usuario_opcional)):
    return templates.TemplateResponse(
        request=request,
        name="historico.html",
        context={"usuario": usuario}
    )
