"""
Esquemas Pydantic para validação de dados de entrada e saída da API.
"""
from typing import List, Optional
from datetime import datetime
import re
from pydantic import BaseModel, Field, field_validator, ConfigDict


# ==========================================
# Esquemas de Autenticação e Usuário
# ==========================================

PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UsuarioCadastro(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150, description="Nome completo do usuário")
    email: str = Field(..., description="Endereço de e-mail único")
    senha: str = Field(..., min_length=6, max_length=100, description="Senha de acesso")

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        valor_limpo = valor.strip().lower()
        if not PADRAO_EMAIL.match(valor_limpo):
            raise ValueError("Endereço de e-mail inválido.")
        return valor_limpo


class UsuarioLogin(BaseModel):
    email: str = Field(..., description="Endereço de e-mail cadastrado")
    senha: str = Field(..., description="Senha de acesso")

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        valor_limpo = valor.strip().lower()
        if not PADRAO_EMAIL.match(valor_limpo):
            raise ValueError("Endereço de e-mail inválido.")
        return valor_limpo



class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    criado_em: datetime


# ==========================================
# Esquemas da Anamnese Padrão (Estrutura)
# ==========================================

class OpcaoItem(BaseModel):
    id: str
    rotulo: str
    descricao: Optional[str] = None


class EstruturaAnamnesePadrao(BaseModel):
    titulo: str
    descricao: str
    sintomas_principais: List[OpcaoItem]
    sintomas_associados: List[OpcaoItem]
    tempos_evolucao: List[OpcaoItem]
    sinais_alerta: List[OpcaoItem]
    comorbidades_comuns: List[OpcaoItem]


# ==========================================
# Esquemas de Envio e Análise de Anamnese
# ==========================================

class AnamneseEntrada(BaseModel):
    nome_paciente: str = Field(..., min_length=2, max_length=150, description="Nome da pessoa avaliada")
    idade: int = Field(..., ge=0, le=130, description="Idade em anos")
    sexo: str = Field(..., description="Sexo biológico (Masculino, Feminino, Outro)")
    sintoma_principal: str = Field(..., min_length=2, max_length=200, description="Queixa ou sintoma principal")
    sintomas_associados: List[str] = Field(default=[], description="Lista de sintomas secundários")
    tempo_evolucao: str = Field(..., description="Tempo de início dos sintomas")
    intensidade_dor: int = Field(..., ge=0, le=10, description="Escala de dor de 0 a 10")
    sinais_alerta: List[str] = Field(default=[], description="Sinais de gravidade identificados")
    comorbidades: List[str] = Field(default=[], description="Histórico de doenças prévias")
    medicamentos: Optional[str] = Field(default="", max_length=300, description="Medicamentos em uso")
    alergias: Optional[str] = Field(default="", max_length=300, description="Alergias conhecidas")


class EncaminhamentoUrgencia(BaseModel):
    necessario: bool
    titulo: str
    mensagem: str
    telefones_emergencia: List[dict]
    link_mapa_proximo: Optional[str] = None


class TriagemResultado(BaseModel):
    id: Optional[int] = None
    nivel_risco: str  # LEVE, MODERADO, GRAVE
    cor_risco: str    # verde, amarelo, vermelho
    titulo_risco: str
    resumo_clinico: str
    orientacoes_personalizadas: List[str]
    sinais_monitoramento: List[str]
    encaminhamento_urgencia: EncaminhamentoUrgencia
    criado_em: Optional[datetime] = None


class AnamneseItemHistorico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_paciente: str
    idade: int
    sintoma_principal: str
    nivel_risco: str
    cor_risco: str
    indicacao_urgencia: bool
    criado_em: datetime
