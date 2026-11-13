"""
Ponto de entrada da aplicação FastAPI para Triagem e Anamnese Médica.
"""
import time
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import CAMINHO_BASE
from app.database import engine, Base
from app.routers.auth_router import roteador_auth
from app.routers.anamnese_router import roteador_anamnese
from app.routers.pages_router import roteador_paginas

# Criação das tabelas no banco de dados SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Anamnese Médica e Triagem Clínica",
    description="API para recepção de anamnese simplificada, classificação de risco de triagem e orientações personalizadas.",
    version="1.0.0"
)

# Middleware para monitorar o tempo de resposta (RNF01: resposta em menos de 5 segundos)
@app.middleware("http")
async def monitorar_tempo_resposta(request: Request, call_next):
    inicio = time.time()
    resposta = await call_next(request)
    duracao = time.time() - inicio
    resposta.headers["X-Tempo-Processamento-Segundos"] = f"{duracao:.4f}"
    return resposta

# Montagem de arquivos estáticos (CSS, JS)
caminho_estaticos = os.path.join(CAMINHO_BASE, "static")
os.makedirs(caminho_estaticos, exist_ok=True)
app.mount("/static", StaticFiles(directory=caminho_estaticos), name="static")

# Inclusão dos roteadores
app.include_router(roteador_auth)
app.include_router(roteador_anamnese)
app.include_router(roteador_paginas)
