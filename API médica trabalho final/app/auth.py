"""
Módulo de segurança, criptografia de senhas e gerenciamento de sessões com cookies.
"""
import base64
import hashlib
import hmac
import json
import os
import time
from typing import Optional

from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.config import CHAVE_SECRETA, NOME_COOKIE_SESSAO, SEGUNDOS_EXPIRACAO_COOKIE
from app.database import obter_banco_dados
from app.models import Usuario


# ==========================================
# Criptografia e Verificação de Senhas
# ==========================================

def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash criptográfico seguro PBKDF2-HMAC-SHA256 com salt aleatório.
    Formato armazenado: salt$hash_hex
    """
    salt = os.urandom(16).hex()
    iteracoes = 100_000
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt.encode("utf-8"),
        iteracoes
    )
    return f"{salt}${hash_bytes.hex()}"


def verificar_senha(senha: str, senha_armazenada: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    try:
        partes = senha_armazenada.split("$")
        if len(partes) != 2:
            return False
        salt, hash_esperado = partes
        iteracoes = 100_000
        hash_calculado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt.encode("utf-8"),
            iteracoes
        ).hex()
        return hmac.compare_digest(hash_calculado, hash_esperado)
    except Exception:
        return False


# ==========================================
# Gerenciamento de Sessão via Cookies
# ==========================================

def criar_token_sessao(usuario_id: int) -> str:
    """
    Cria um token assinado contendo o ID do usuário e data de expiração.
    """
    expira_em = int(time.time()) + SEGUNDOS_EXPIRACAO_COOKIE
    payload = json.dumps({"sub": usuario_id, "exp": expira_em}, separators=(",", ":"))
    payload_b64 = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8").rstrip("=")
    
    assinatura = hmac.new(
        CHAVE_SECRETA.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    return f"{payload_b64}.{assinatura}"


def validar_token_sessao(token: str) -> Optional[int]:
    """
    Valida a assinatura e expiração do token de sessão.
    Retorna o ID do usuário autenticado ou None se inválido.
    """
    try:
        partes = token.split(".")
        if len(partes) != 2:
            return None
        payload_b64, assinatura = partes

        # Recalcular e comparar assinatura em tempo constante
        assinatura_esperada = hmac.new(
            CHAVE_SECRETA.encode("utf-8"),
            payload_b64.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(assinatura, assinatura_esperada):
            return None

        # Recompor padding Base64
        padding = "=" * ((4 - len(payload_b64) % 4) % 4)
        dados = json.loads(base64.urlsafe_b64decode(payload_b64 + padding).decode("utf-8"))

        if time.time() > dados.get("exp", 0):
            return None

        return int(dados.get("sub"))
    except Exception:
        return None


# ==========================================
# Dependências do FastAPI
# ==========================================

def obter_usuario_atual(
    request: Request,
    db: Session = Depends(obter_banco_dados)
) -> Usuario:
    """
    Dependência obrigatória: recupera o usuário logado via cookie de sessão.
    Lança erro 401 caso não autenticado.
    """
    token = request.cookies.get(NOME_COOKIE_SESSAO)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado. Por favor, realize o login."
        )

    usuario_id = validar_token_sessao(token)
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada ou inválida. Faça login novamente."
        )

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário associado à sessão não foi encontrado."
        )

    return usuario


def obter_usuario_opcional(
    request: Request,
    db: Session = Depends(obter_banco_dados)
) -> Optional[Usuario]:
    """
    Dependência opcional: retorna o usuário logado se existir sessão válida, senão None.
    """
    token = request.cookies.get(NOME_COOKIE_SESSAO)
    if not token:
        return None
    usuario_id = validar_token_sessao(token)
    if not usuario_id:
        return None
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()
