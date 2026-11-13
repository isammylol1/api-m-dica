"""
Motor de Triagem Clínica e Análise de Anamnese Simplificada.
"""
from typing import Dict, Any, List
from app.schemas import (
    EstruturaAnamnesePadrao,
    OpcaoItem,
    AnamneseEntrada,
    TriagemResultado,
    EncaminhamentoUrgencia,
)


def obter_estrutura_anamnese_padrao() -> EstruturaAnamnesePadrao:
    """
    Retorna a anamnese padrão que se repete para todas as pessoas (RF05).
    """
    return EstruturaAnamnesePadrao(
        titulo="Anamnese Clínica Geral e Triagem",
        descricao="Formulário estruturado padronizado para avaliação inicial de sintomas e orientações de triagem.",
        sintomas_principais=[
            OpcaoItem(id="dor_cabeca", rotulo="Dor de cabeça (Cefaleia)"),
            OpcaoItem(id="febre", rotulo="Febre ou calafrios"),
            OpcaoItem(id="dor_peito", rotulo="Dor ou aperto no peito / tórax"),
            OpcaoItem(id="falta_ar", rotulo="Falta de ar ou cansaço respiratório"),
            OpcaoItem(id="dor_abdominal", rotulo="Dor na barriga / abdômen"),
            OpcaoItem(id="tosse", rotulo="Tosse persistente"),
            OpcaoItem(id="diarreia_vomito", rotulo="Náusea, vômitos ou diarreia"),
            OpcaoItem(id="tontura_fraqueza", rotulo="Tontura, vertigem ou fraqueza"),
            OpcaoItem(id="dor_garganta", rotulo="Dor de garganta"),
            OpcaoItem(id="dor_lombar", rotulo="Dor nas costas ou lombar"),
            OpcaoItem(id="outro", rotulo="Outro sintoma não listado"),
        ],
        sintomas_associados=[
            OpcaoItem(id="coriza", rotulo="Coriza ou congestão nasal"),
            OpcaoItem(id="perda_apetite", rotulo="Perda de apetite"),
            OpcaoItem(id="sudorese", rotulo="Suor frio ou excessivo"),
            OpcaoItem(id="sensibilidade_luz", rotulo="Sensibilidade à luz (fotofobia)"),
            OpcaoItem(id="palpitacoes", rotulo="Coração acelerado / palpitações"),
            OpcaoItem(id="dores_corpo", rotulo="Dores musculares pelo corpo"),
            OpcaoItem(id="visao_turva", rotulo="Visão embaçada ou manchas"),
            OpcaoItem(id="inchaco_pernas", rotulo="Inchaço nas pernas ou tornozelos"),
        ],
        tempos_evolucao=[
            OpcaoItem(id="poucas_horas", rotulo="Começou há poucas horas (início súbito)"),
            OpcaoItem(id="1_a_2_dias", rotulo="Entre 1 e 2 dias"),
            OpcaoItem(id="3_a_7_dias", rotulo="Entre 3 e 7 dias"),
            OpcaoItem(id="mais_1_semana", rotulo="Há mais de 1 semana"),
            OpcaoItem(id="mais_1_mes", rotulo="Há mais de 1 mês (crônico)"),
        ],
        sinais_alerta=[
            OpcaoItem(
                id="dor_peito_irradiada",
                rotulo="Dor forte no peito irradiando para braço esquerdo, costas ou mandíbula",
                descricao="Possível sinal de evento cardiovascular agudo"
            ),
            OpcaoItem(
                id="falta_ar_grave",
                rotulo="Falta de ar intensa, lábios arroxeados ou incapacidade de completar frases",
                descricao="Comprometimento respiratório agudo"
            ),
            OpcaoItem(
                id="confusao_desmaio",
                rotulo="Desmaio recente, perda de consciência ou confusão mental súbita",
                descricao="Sinal neurológico de alta prioridade"
            ),
            OpcaoItem(
                id="paralisia_fala",
                rotulo="Fraqueza súbita em um lado do rosto/corpo ou fala enrolada/incompreensível",
                descricao="Possível sinal de Acidente Vascular Cerebral (AVC)"
            ),
            OpcaoItem(
                id="sangramento_grave",
                rotulo="Sangramento volumoso ativo, vômito com sangue ou fezes escuras tipo borra",
                descricao="Hemorragia aguda"
            ),
            OpcaoItem(
                id="febre_convulsao_rigidez",
                rotulo="Febre alta associada a convulsão, manchas escuras na pele ou rigidez na nuca",
                descricao="Sinal de infecção grave do sistema nervoso"
            ),
        ],
        comorbidades_comuns=[
            OpcaoItem(id="hipertensao", rotulo="Hipertensão arterial (Pressão alta)"),
            OpcaoItem(id="diabetes", rotulo="Diabetes Mellitus"),
            OpcaoItem(id="cardiopatia", rotulo="Doença cardíaca ou infarto prévio"),
            OpcaoItem(id="asma_dpoc", rotulo="Asma, bronquite ou DPOC"),
            OpcaoItem(id="doenca_renal", rotulo="Doença renal crônica"),
            OpcaoItem(id="imunossuprimido", rotulo="Imunossupressão ou tratamento oncológico"),
            OpcaoItem(id="nenhuma", rotulo="Nenhuma doença crônica conhecida"),
        ]
    )


def analisar_anamnese(dados: AnamneseEntrada) -> TriagemResultado:
    """
    Executa a análise das informações e identifica sinais de alerta,
    classificando em LEVE, MODERADO ou GRAVE com orientações personalizadas.
    """
    # 1. Checagem de Sinais de Alerta Críticos (RF04)
    sinais_graves_selecionados = [
        s for s in dados.sinais_alerta
        if s in [
            "dor_peito_irradiada",
            "falta_ar_grave",
            "confusao_desmaio",
            "paralisia_fala",
            "sangramento_grave",
            "febre_convulsao_rigidez"
        ]
    ]

    # Critérios de Emergência / Gravidade (RF10)
    tem_sinal_alerta_grave = len(sinais_graves_selecionados) > 0
    dor_intensa_urgente = (dados.intensidade_dor >= 9) and (
        dados.sintoma_principal in ["dor_peito", "falta_ar", "dor_abdominal", "dor_cabeca"]
    )
    respiratorio_critico = dados.sintoma_principal == "falta_ar" and dados.tempo_evolucao == "poucas_horas"

    e_caso_grave = tem_sinal_alerta_grave or dor_intensa_urgente or respiratorio_critico

    # 2. Critérios de Risco Moderado
    comorbidades_risco = [
        c for c in dados.comorbidades
        if c in ["cardiopatia", "diabetes", "hipertensao", "asma_dpoc", "doenca_renal", "imunossuprimido"]
    ]
    dor_moderada = 5 <= dados.intensidade_dor <= 8
    evolucao_preocupante = dados.tempo_evolucao in ["3_a_7_dias", "mais_1_semana"] and dados.sintoma_principal in ["febre", "falta_ar", "tosse", "dor_abdominal"]
    idade_vulneravel = dados.idade >= 65 or dados.idade <= 2

    e_caso_moderado = (dor_moderada or bool(comorbidades_risco) or evolucao_preocupante or idade_vulneravel) and not e_caso_grave

    # 3. Definição do Nível e Resumo Clínico
    if e_caso_grave:
        nivel_risco = "GRAVE"
        cor_risco = "vermelho"
        titulo_risco = "Atenção Imediata - Alta Prioridade (Emergência)"
        indicacao_urgencia = True
        resumo_clinico = (
            f"Paciente {dados.nome_paciente}, {dados.idade} anos, apresenta queixa de '{dados.sintoma_principal}' "
            f"com intensidade de dor {dados.intensidade_dor}/10 e presença de sinais de alerta de risco à vida. "
            f"Requer avaliação médica emergencial imediata."
        )
    elif e_caso_moderado:
        nivel_risco = "MODERADO"
        cor_risco = "amarelo"
        titulo_risco = "Prioridade Moderada - Avaliação Médica Recomendada"
        indicacao_urgencia = False
        resumo_clinico = (
            f"Paciente {dados.nome_paciente}, {dados.idade} anos, relata '{dados.sintoma_principal}' "
            f"com evolução '{dados.tempo_evolucao}' e intensidade {dados.intensidade_dor}/10. "
            f"O quadro clínico e fatores associados recomendam consulta médica em serviço de saúde ou UBS."
        )
    else:
        nivel_risco = "LEVE"
        cor_risco = "verde"
        titulo_risco = "Baixo Risco - Cuidados Iniciais e Observação"
        indicacao_urgencia = False
        resumo_clinico = (
            f"Paciente {dados.nome_paciente}, {dados.idade} anos, com queixa de '{dados.sintoma_principal}' "
            f"de intensidade leve ({dados.intensidade_dor}/10), sem sinais de alarme no momento. "
            f"Quadro compatível com cuidados domiciliares de suporte e monitoramento de sintomas."
        )

    # 4. Geração de Orientações Personalizadas (RF09)
    orientacoes: List[str] = []
    sinais_monitoramento: List[str] = []

    # Saudação e contexto personalizado
    orientacoes.append(f"Olá, {dados.nome_paciente}. Analisamos as informações fornecidas na sua anamnese.")

    if e_caso_grave:
        orientacoes.append(
            "⚠️ ATENÇÃO: Devido aos sintomas e sinais de alarme relatados, você deve se dirigir imediatamente ao Pronto-Socorro, UPA ou hospital mais próximo."
        )
        orientacoes.append(
            "Não conduza veículos sozinho. Peça ajuda a um acompanhante ou acione o SAMU pelo número 192."
        )
        orientacoes.append(
            "Mantenha repouso absoluto, mantenha as vias aéreas livres e afrouxe roupas apertadas enquanto aguarda socorro."
        )
        sinais_monitoramento.extend([
            "Piora na respiração ou lábios azulados/arroxeados",
            "Sensação de desmaio iminente ou tontura forte",
            "Aumento súbito da dor torácica"
        ])
    elif e_caso_moderado:
        orientacoes.append(
            "Procure uma Unidade Básica de Saúde (UBS), AMA ou clínica médica para avaliação presencial nas próximas 12 a 24 horas."
        )
        orientacoes.append(
            "Evite a automedicação, especialmente o uso de anti-inflamatórios sem prescrição médica."
        )
        orientacoes.append(
            "Mantenha hidratação constante com água, água de coco ou soro caseiro, e repouso adequado."
        )
        sinais_monitoramento.extend([
            "Febre que atinja mais de 38,5°C ou que não responda a antitérmicos",
            "Aparecimento de falta de ar ou dor no peito",
            "Incapacidade de reter líquidos por vômitos frequentes",
            "Piora significativa da intensidade da dor"
        ])
    else:
        orientacoes.append(
            "Mantenha-se bem hidratado (mínimo de 2 litros de água ao longo do dia) e faça repouso."
        )
        orientacoes.append(
            "Alimente-se com refeições leves e de fácil digestão, evitando alimentos ultraprocessados ou gordurosos."
        )
        orientacoes.append(
            "Caso os sintomas não apresentem melhora em 48 a 72 horas, agende uma consulta médica de rotina."
        )
        sinais_monitoramento.extend([
            "Aparecimento de febre acima de 38°C",
            "Aumento da intensidade da dor para além do nível leve",
            "Surgimento de novos sintomas não relatados anteriormente"
        ])

    # Personalização por idade
    if dados.idade >= 65:
        orientacoes.append(
            "👵 Orientação específica para idosos: Por ter 65 anos ou mais, seu organismo pode apresentar desidratação ou infecções de forma atípica. Monitore a temperatura, pressão arterial e confira se há sonolência incomum."
        )
    elif dados.idade <= 12:
        orientacoes.append(
            "👶 Orientação pediátrica: Mantenha acompanhamento contínuo dos pais ou responsáveis, observando se a criança continua brincando, urinando normalmente e aceitando líquidos."
        )

    # Personalização por comorbidades
    for comorbidade in dados.comorbidades:
        if comorbidade == "diabetes":
            orientacoes.append(
                "🩸 Monitoramento de Diabetes: Verifique a glicemia capilar com maior frequência durante este período, pois quadros infecciosos ou de dor podem desregular os níveis de glicose."
            )
        elif comorbidade == "hipertensao":
            orientacoes.append(
                "❤️ Monitoramento de Hipertensão: Aferir a pressão arterial no repouso. Evite medicamentos vasoconstritores ou antigripais que possam elevar a pressão sem aval médico."
            )
        elif comorbidade == "asma_dpoc":
            orientacoes.append(
                "🫁 Atenção Respiratória: Tenha por perto suas medicações inalatórias de resgate conforme orientação do seu pneumologista e evite exposição a fumaça ou poeira."
            )
        elif comorbidade == "cardiopatia":
            orientacoes.append(
                "💓 Histórico Cardíaco: Qualquer alteração no ritmo cardíaco ou desconforto torácico deve ser motivo de atendimento médico presencial imediato."
            )

    # Encaminhamento de Urgência (RF10)
    encaminhamento = EncaminhamentoUrgencia(
        necessario=e_caso_grave,
        titulo="Encaminhamento de Urgência Médica" if e_caso_grave else "Acompanhamento Clínico",
        mensagem=(
            "Seu quadro possui indicativos de gravidade que exigem avaliação de emergência imediata em hospital ou pronto-atendimento."
            if e_caso_grave else
            "Não foram identificados sinais de emergência imediata. Siga as orientações e procure atendimento caso haja piora."
        ),
        telefones_emergencia=[
            {"nome": "SAMU (Serviço de Atendimento Móvel de Urgência)", "numero": "192"},
            {"nome": "Corpo de Bombeiros (Resgate)", "numero": "193"},
            {"nome": "Disque Saúde (SUS)", "numero": "136"}
        ],
        link_mapa_proximo=(
            "https://www.google.com/maps/search/pronto+socorro+hospital+upa+urgencia+mais+proximo"
            if e_caso_grave else None
        )
    )

    return TriagemResultado(
        nivel_risco=nivel_risco,
        cor_risco=cor_risco,
        titulo_risco=titulo_risco,
        resumo_clinico=resumo_clinico,
        orientacoes_personalizadas=orientacoes,
        sinais_monitoramento=sinais_monitoramento,
        encaminhamento_urgencia=encaminhamento
    )
