"""
Roteador para gerenciamento de contas de usuários, autenticação e cookies.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth import (
    gerar_hash_senha,
    verificar_senha,
    criar_token_sessao,
    obter_usuario_atual,
)
from app.config import NOME_COOKIE_SESSAO, SEGUNDOS_EXPIRACAO_COOKIE
from app.database import obter_banco_dados
from app.models import Usuario
from app.schemas import UsuarioCadastro, UsuarioLogin, UsuarioResposta

roteador_auth = APIRouter(prefix="/api/auth", tags=["Autenticação"])


@roteador_auth.post("/cadastro", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    dados: UsuarioCadastro,
    resposta: Response,
    db: Session = Depends(obter_banco_dados)
):
    """
    Cadastra um novo usuário no sistema e define o cookie de sessão com segurança.
    """
    email_normalizado = dados.email.lower().strip()
    usuario_existente = db.query(Usuario).filter(Usuario.email == email_normalizado).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma conta cadastrada com este endereço de e-mail."
        )

    novo_usuario = Usuario(
        nome=dados.nome.strip(),
        email=email_normalizado,
        senha_hash=gerar_hash_senha(dados.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Criação automática do cookie de sessão seguro
    token = criar_token_sessao(novo_usuario.id)
    resposta.set_cookie(
        key=NOME_COOKIE_SESSAO,
        value=token,
        max_age=SEGUNDOS_EXPIRACAO_COOKIE,
        httponly=True,
        samesite="lax",
        secure=False  # Em ambiente de desenvolvimento local sem HTTPS
    )

    return novo_usuario


@roteador_auth.post("/login", response_model=UsuarioResposta)
def realizar_login(
    dados: UsuarioLogin,
    resposta: Response,
    db: Session = Depends(obter_banco_dados)
):
    """
    Realiza a autenticação do usuário e emite o cookie de sessão HttpOnly (RF08).
    """
    email_normalizado = dados.email.lower().strip()
    usuario = db.query(Usuario).filter(Usuario.email == email_normalizado).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    token = criar_token_sessao(usuario.id)
    resposta.set_cookie(
        key=NOME_COOKIE_SESSAO,
        value=token,
        max_age=SEGUNDOS_EXPIRACAO_COOKIE,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return usuario


@roteador_auth.post("/logout")
def realizar_logout(resposta: Response):
    """
    Encerra a sessão do usuário removendo o cookie HttpOnly.
    """
    resposta.delete_cookie(
        key=NOME_COOKIE_SESSAO,
        httponly=True,
        samesite="lax"
    )
    return {"mensagem": "Logout realizado com sucesso."}


@roteador_auth.get("/perfil", response_model=UsuarioResposta)
def obter_perfil_atual(usuario_atual: Usuario = Depends(obter_usuario_atual)):
    """
    Retorna os dados do usuário autenticado no momento.
    """
    return usuario_atual
