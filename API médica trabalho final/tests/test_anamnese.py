"""
Testes de integração das rotas de anamnese, histórico e tempo de resposta.
"""
import time
from fastapi.testclient import TestClient
from app.main import app


def test_obter_anamnese_padrao(cliente):
    resposta = cliente.get("/api/anamnese/padrao")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert "sintomas_principais" in dados
    assert "sinais_alerta" in dados
    assert len(dados["sintomas_principais"]) > 0


def test_fluxo_submissao_e_historico(cliente):
    # 1. Cadastrar usuário
    resposta_cad = cliente.post(
        "/api/auth/cadastro",
        json={
            "nome": "Ana Paula",
            "email": "ana@exemplo.com",
            "senha": "senhaSegura123"
        }
    )
    assert resposta_cad.status_code == 201

    # 2. Submeter Anamnese com medição de tempo (< 5 segundos - RNF01)
    tempo_inicio = time.time()
    resposta_triagem = cliente.post(
        "/api/anamnese/analisar",
        json={
            "nome_paciente": "Ana Paula",
            "idade": 30,
            "sexo": "Feminino",
            "sintoma_principal": "febre",
            "sintomas_associados": ["dores_corpo"],
            "tempo_evolucao": "1_a_2_dias",
            "intensidade_dor": 4,
            "sinais_alerta": [],
            "comorbidades": ["nenhuma"],
            "medicamentos": "",
            "alergias": ""
        }
    )
    duracao = time.time() - tempo_inicio

    # Verifica tempo de resposta do RNF01
    assert duracao < 5.0, f"Tempo de resposta excedeu 5 segundos: {duracao}s"
    assert resposta_triagem.status_code == 200

    dados_triagem = resposta_triagem.json()
    assert dados_triagem["id"] is not None
    assert dados_triagem["nivel_risco"] == "LEVE"

    # 3. Consultar Histórico
    resposta_historico = cliente.get("/api/anamnese/historico")
    assert resposta_historico.status_code == 200
    itens_historico = resposta_historico.json()
    assert len(itens_historico) >= 1
    assert itens_historico[0]["nome_paciente"] == "Ana Paula"

    # 4. Obter Detalhes da Anamnese
    anamnese_id = dados_triagem["id"]
    resposta_detalhes = cliente.get(f"/api/anamnese/{anamnese_id}")
    assert resposta_detalhes.status_code == 200
    detalhes = resposta_detalhes.json()
    assert detalhes["id"] == anamnese_id
    assert detalhes["sintoma_principal"] == "febre"


def test_seguranca_isolamento_outro_usuario():
    # Cadastra segundo usuário em um novo cliente
    with TestClient(app) as cliente_outro:
        resposta_cad = cliente_outro.post(
            "/api/auth/cadastro",
            json={
                "nome": "Outro Usuário",
                "email": "outro@exemplo.com",
                "senha": "senhaSegura123"
            }
        )
        assert resposta_cad.status_code == 201

        # Tenta acessar a anamnese ID 1 da Ana Paula (RNF07)
        resposta_acesso_indevido = cliente_outro.get("/api/anamnese/1")
        assert resposta_acesso_indevido.status_code == 404
