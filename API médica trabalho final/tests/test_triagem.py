"""
Testes unitários das regras de negócio do motor de triagem médica.
"""
from app.schemas import AnamneseEntrada
from app.services.triagem_service import analisar_anamnese, obter_estrutura_anamnese_padrao


def test_estrutura_anamnese_padrao():
    estrutura = obter_estrutura_anamnese_padrao()
    assert len(estrutura.sintomas_principais) > 0
    assert len(estrutura.sinais_alerta) > 0
    assert len(estrutura.tempos_evolucao) > 0
    assert len(estrutura.comorbidades_comuns) > 0


def test_caso_leve_sem_sinais_alerta():
    entrada = AnamneseEntrada(
        nome_paciente="João Leve",
        idade=28,
        sexo="Masculino",
        sintoma_principal="dor_garganta",
        sintomas_associados=["coriza"],
        tempo_evolucao="1_a_2_dias",
        intensidade_dor=2,
        sinais_alerta=[],
        comorbidades=["nenhuma"]
    )
    resultado = analisar_anamnese(entrada)
    assert resultado.nivel_risco == "LEVE"
    assert resultado.cor_risco == "verde"
    assert resultado.encaminhamento_urgencia.necessario is False
    assert any("João Leve" in o for o in resultado.orientacoes_personalizadas)


def test_caso_moderado_com_comorbidade_e_dor_media():
    entrada = AnamneseEntrada(
        nome_paciente="Maria Moderada",
        idade=55,
        sexo="Feminino",
        sintoma_principal="dor_abdominal",
        sintomas_associados=["perda_apetite"],
        tempo_evolucao="3_a_7_dias",
        intensidade_dor=6,
        sinais_alerta=[],
        comorbidades=["diabetes", "hipertensao"]
    )
    resultado = analisar_anamnese(entrada)
    assert resultado.nivel_risco == "MODERADO"
    assert resultado.cor_risco == "amarelo"
    assert resultado.encaminhamento_urgencia.necessario is False
    assert any("Diabetes" in o for o in resultado.orientacoes_personalizadas)
    assert any("Hipertensão" in o for o in resultado.orientacoes_personalizadas)


def test_caso_grave_com_dor_peito_irradiada():
    entrada = AnamneseEntrada(
        nome_paciente="Roberto Alerta",
        idade=50,
        sexo="Masculino",
        sintoma_principal="dor_peito",
        sintomas_associados=["sudorese", "palpitacoes"],
        tempo_evolucao="poucas_horas",
        intensidade_dor=9,
        sinais_alerta=["dor_peito_irradiada"],
        comorbidades=["cardiopatia"]
    )
    resultado = analisar_anamnese(entrada)
    assert resultado.nivel_risco == "GRAVE"
    assert resultado.cor_risco == "vermelho"
    assert resultado.encaminhamento_urgencia.necessario is True
    assert "google.com/maps" in resultado.encaminhamento_urgencia.link_mapa_proximo
    assert any("192" in tel["numero"] for tel in resultado.encaminhamento_urgencia.telefones_emergencia)


def test_personalizacao_para_idosos():
    entrada = AnamneseEntrada(
        nome_paciente="Dona Francisca",
        idade=72,
        sexo="Feminino",
        sintoma_principal="tosse",
        sintomas_associados=["dores_corpo"],
        tempo_evolucao="1_a_2_dias",
        intensidade_dor=3,
        sinais_alerta=[],
        comorbidades=[]
    )
    resultado = analisar_anamnese(entrada)
    assert any("idosos" in o.lower() for o in resultado.orientacoes_personalizadas)
