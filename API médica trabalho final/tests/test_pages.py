"""
Testes de renderização das páginas HTML da interface web.
"""
def test_pagina_inicial(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "Triagem Médica e Anamnese Digital" in resposta.text


def test_pagina_anamnese(cliente):
    resposta = cliente.get("/anamnese")
    assert resposta.status_code == 200
    assert "Anamnese Geral e Triagem de Sintomas" in resposta.text


def test_pagina_resultado(cliente):
    resposta = cliente.get("/resultado")
    assert resposta.status_code == 200
    assert "Resultado da Triagem Clínica" in resposta.text


def test_pagina_historico(cliente):
    resposta = cliente.get("/historico")
    assert resposta.status_code == 200
    assert "Minhas Anamneses e Triagens" in resposta.text
