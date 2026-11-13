"""
Testes de autenticação, cadastro e cookies de sessão.
"""
def test_cadastro_usuario_com_sucesso(cliente):
    resposta = cliente.post(
        "/api/auth/cadastro",
        json={
            "nome": "Carlos Silva",
            "email": "carlos@exemplo.com",
            "senha": "senhaSegura123"
        }
    )
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["nome"] == "Carlos Silva"
    assert dados["email"] == "carlos@exemplo.com"
    assert "token_sessao" in resposta.cookies


def test_falha_ao_cadastrar_email_duplicado(cliente):
    resposta = cliente.post(
        "/api/auth/cadastro",
        json={
            "nome": "Carlos Duplicado",
            "email": "carlos@exemplo.com",
            "senha": "outraSenha123"
        }
    )
    assert resposta.status_code == 400
    assert "Já existe uma conta" in resposta.json()["detail"]


def test_login_com_credenciais_validas(cliente):
    resposta = cliente.post(
        "/api/auth/login",
        json={
            "email": "carlos@exemplo.com",
            "senha": "senhaSegura123"
        }
    )
    assert resposta.status_code == 200
    assert "token_sessao" in resposta.cookies


def test_login_com_senha_incorreta(cliente):
    resposta = cliente.post(
        "/api/auth/login",
        json={
            "email": "carlos@exemplo.com",
            "senha": "senhaErrada999"
        }
    )
    assert resposta.status_code == 401
    assert "incorretos" in resposta.json()["detail"]


def test_protecao_rota_perfil_sem_cookie():
    from fastapi.testclient import TestClient
    from app.main import app
    cliente_anonimo = TestClient(app)
    resposta = cliente_anonimo.get("/api/auth/perfil")
    assert resposta.status_code == 401


def test_logout_remove_cookie(cliente):
    resposta_login = cliente.post(
        "/api/auth/login",
        json={
            "email": "carlos@exemplo.com",
            "senha": "senhaSegura123"
        }
    )
    assert resposta_login.status_code == 200

    resposta_logout = cliente.post("/api/auth/logout")
    assert resposta_logout.status_code == 200
    assert "Logout realizado com sucesso" in resposta_logout.json()["mensagem"]
