"""
Roteador de Anamnese e Triagem Médica.
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import obter_usuario_atual
from app.database import obter_banco_dados
from app.models import Usuario
from app.schemas import (
    EstruturaAnamnesePadrao,
    AnamneseEntrada,
    TriagemResultado,
    AnamneseItemHistorico,
    EncaminhamentoUrgencia,
)
from app.services.triagem_service import (
    obter_estrutura_anamnese_padrao,
    analisar_anamnese,
)
from app.services.anamnese_service import (
    salvar_anamnese,
    listar_anamneses_usuario,
    obter_anamnese_por_id,
)

roteador_anamnese = APIRouter(prefix="/api/anamnese", tags=["Anamnese e Triagem"])


@roteador_anamnese.get("/padrao", response_model=EstruturaAnamnesePadrao)
def carregar_anamnese_padrao():
    """
    Retorna o modelo de anamnese padrão que se repete para todas as pessoas (RF05).
    """
    return obter_estrutura_anamnese_padrao()


@roteador_anamnese.post("/analisar", response_model=TriagemResultado)
def submeter_e_analisar_anamnese(
    dados: AnamneseEntrada,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(obter_banco_dados)
):
    """
    Cadastra as respostas, processa os sintomas e sinais de alerta,
    executa a análise clínica e salva os resultados no banco de dados
    (RF01, RF02, RF03, RF04, RF07, RF08, RF09, RF10, RF11).
    """
    resultado_triagem = analisar_anamnese(dados)
    registro_salvo = salvar_anamnese(db, usuario_atual.id, dados, resultado_triagem)
    resultado_triagem.id = registro_salvo.id
    resultado_triagem.criado_em = registro_salvo.criado_em

    return resultado_triagem


@roteador_anamnese.get("/historico", response_model=List[AnamneseItemHistorico])
def consultar_historico_anamneses(
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(obter_banco_dados)
):
    """
    Consulta o histórico de todas as anamneses registradas pelo usuário autenticado (RF08).
    """
    registros = listar_anamneses_usuario(db, usuario_atual.id)
    return registros


@roteador_anamnese.get("/{anamnese_id}")
def obter_detalhes_anamnese(
    anamnese_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(obter_banco_dados)
):
    """
    Recupera os detalhes completos e orientações de uma anamnese específica (RNF07).
    """
    registro = obter_anamnese_por_id(db, anamnese_id, usuario_atual.id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anamnese não encontrada ou você não tem permissão para acessá-la."
        )

    sintomas_associados = json.loads(registro.sintomas_associados or "[]")
    sinais_alerta = json.loads(registro.sinais_alerta or "[]")
    comorbidades = json.loads(registro.comorbidades or "[]")
    orientacoes = json.loads(registro.orientacoes_personalizadas or "[]")

    e_grave = registro.nivel_risco == "GRAVE"

    return {
        "id": registro.id,
        "nome_paciente": registro.nome_paciente,
        "idade": registro.idade,
        "sexo": registro.sexo,
        "sintoma_principal": registro.sintoma_principal,
        "sintomas_associados": sintomas_associados,
        "tempo_evolucao": registro.tempo_evolucao,
        "intensidade_dor": registro.intensidade_dor,
        "sinais_alerta": sinais_alerta,
        "comorbidades": comorbidades,
        "medicamentos": registro.medicamentos,
        "alergias": registro.alergias,
        "nivel_risco": registro.nivel_risco,
        "cor_risco": registro.cor_risco,
        "resumo_clinico": registro.resumo_clinico,
        "orientacoes_personalizadas": orientacoes,
        "indicacao_urgencia": registro.indicacao_urgencia,
        "criado_em": registro.criado_em,
        "encaminhamento_urgencia": {
            "necessario": e_grave,
            "titulo": "Encaminhamento de Urgência Médica" if e_grave else "Acompanhamento Clínico",
            "mensagem": (
                "Seu quadro possui indicativos de gravidade que exigem avaliação de emergência imediata em hospital ou pronto-atendimento."
                if e_grave else
                "Não foram identificados sinais de emergência imediata. Siga as orientações e procure atendimento caso haja piora."
            ),
            "telefones_emergencia": [
                {"nome": "SAMU (Serviço de Atendimento Móvel de Urgência)", "numero": "192"},
                {"nome": "Corpo de Bombeiros (Resgate)", "numero": "193"},
                {"nome": "Disque Saúde (SUS)", "numero": "136"}
            ],
            "link_mapa_proximo": (
                "https://www.google.com/maps/search/pronto+socorro+hospital+upa+urgencia+mais+proximo"
                if e_grave else None
            )
        }
    }
