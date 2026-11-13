"""
Serviço de persistência e consulta de anamneses no banco de dados.
"""
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Anamnese
from app.schemas import AnamneseEntrada, TriagemResultado


def salvar_anamnese(
    db: Session,
    usuario_id: int,
    dados: AnamneseEntrada,
    resultado: TriagemResultado
) -> Anamnese:
    """
    Persiste as respostas da anamnese e o resultado da triagem no banco de dados (RF01, RF11).
    """
    nova_anamnese = Anamnese(
        usuario_id=usuario_id,
        nome_paciente=dados.nome_paciente,
        idade=dados.idade,
        sexo=dados.sexo,
        sintoma_principal=dados.sintoma_principal,
        sintomas_associados=json.dumps(dados.sintomas_associados, ensure_ascii=False),
        tempo_evolucao=dados.tempo_evolucao,
        intensidade_dor=dados.intensidade_dor,
        sinais_alerta=json.dumps(dados.sinais_alerta, ensure_ascii=False),
        comorbidades=json.dumps(dados.comorbidades, ensure_ascii=False),
        medicamentos=dados.medicamentos or "",
        alergias=dados.alergias or "",
        nivel_risco=resultado.nivel_risco,
        cor_risco=resultado.cor_risco,
        resumo_clinico=resultado.resumo_clinico,
        orientacoes_personalizadas=json.dumps(resultado.orientacoes_personalizadas, ensure_ascii=False),
        indicacao_urgencia=resultado.encaminhamento_urgencia.necessario,
    )
    db.add(nova_anamnese)
    db.commit()
    db.refresh(nova_anamnese)
    return nova_anamnese


def listar_anamneses_usuario(db: Session, usuario_id: int) -> List[Anamnese]:
    """
    Retorna o histórico de todas as anamneses registradas pelo usuário, da mais recente para a mais antiga (RF08).
    """
    return db.query(Anamnese).filter(
        Anamnese.usuario_id == usuario_id
    ).order_by(Anamnese.criado_em.desc()).all()


def obter_anamnese_por_id(db: Session, anamnese_id: int, usuario_id: int) -> Optional[Anamnese]:
    """
    Retorna uma anamnese específica garantindo que pertence ao usuário logado (RNF07).
    """
    return db.query(Anamnese).filter(
        Anamnese.id == anamnese_id,
        Anamnese.usuario_id == usuario_id
    ).first()
