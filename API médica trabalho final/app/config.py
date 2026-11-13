"""
Configurações da aplicação da API Médica de Anamnese.
"""
import os

CAMINHO_BASE = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_PROJETO = os.path.dirname(CAMINHO_BASE)

# Banco de dados SQLite padrão
URL_BANCO_DADOS = os.getenv("URL_BANCO_DADOS", f"sqlite:///{os.path.join(DIRETORIO_PROJETO, 'anamnese.db')}")

# Chave secreta para assinatura dos cookies de sessão
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA", "chave-secreta-anamnese-medica-triagem-segura-2026")

# Configurações do cookie de sessão
NOME_COOKIE_SESSAO = "token_sessao"
SEGUNDOS_EXPIRACAO_COOKIE = 60 * 60 * 24 * 7  # 7 dias
