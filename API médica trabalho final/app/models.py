"""
Modelos ORM de banco de dados para Usuários e Anamneses.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


def horario_atual_utc():
    return datetime.now(timezone.utc)


class Usuario(Base):
    """
    Modelo de usuário cadastrado no sistema.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=horario_atual_utc, nullable=False)

    # Relacionamento com as anamneses registradas pelo usuário
    anamneses = relationship("Anamnese", back_populates="usuario", cascade="all, delete-orphan")


class Anamnese(Base):
    """
    Modelo para armazenamento das respostas da anamnese e do resultado da triagem.
    """
    __tablename__ = "anamneses"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)

    # Dados do paciente
    nome_paciente = Column(String(150), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String(20), nullable=False)

    # Sintomas e queixas
    sintoma_principal = Column(String(200), nullable=False)
    sintomas_associados = Column(Text, nullable=True)  # Armazenado em JSON (lista de sintomas)
    tempo_evolucao = Column(String(100), nullable=False)
    intensidade_dor = Column(Integer, nullable=False)  # Escala 0 a 10

    # Sinais de alerta e histórico clínico
    sinais_alerta = Column(Text, nullable=True)        # Armazenado em JSON (lista de red flags assinaladas)
    comorbidades = Column(Text, nullable=True)          # Armazenado em JSON (doenças crônicas)
    medicamentos = Column(String(300), nullable=True)
    alergias = Column(String(300), nullable=True)

    # Resultado da análise e triagem clínica
    nivel_risco = Column(String(50), nullable=False)    # LEVE, MODERADO, GRAVE
    cor_risco = Column(String(20), nullable=False)      # verde, amarelo, vermelho
    resumo_clinico = Column(Text, nullable=False)
    orientacoes_personalizadas = Column(Text, nullable=False)  # JSON com lista de orientações
    indicacao_urgencia = Column(Boolean, default=False, nullable=False)

    criado_em = Column(DateTime, default=horario_atual_utc, nullable=False)

    # Relacionamento
    usuario = relationship("Usuario", back_populates="anamneses")
