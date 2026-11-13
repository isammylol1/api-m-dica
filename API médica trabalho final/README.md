# API Médica de Anamnese Simplificada e Triagem Clínica

Sistema web completo para recepção de anamnese clínica estruturada, classificação de risco e fornecimento de orientações personalizadas de triagem médica.

Construído em conformidade com as especificações (`specs.md`) e decisões de projeto (`design_decisions.md`):
- **Linguagem**: Python 3.13+
- **Framework Web**: FastAPI
- **Banco de Dados**: SQLAlchemy com persistência SQLite
- **Interface Visual**: HTML5, CSS3 puro e JavaScript nativo (sem bibliotecas externas)
- **Segurança**: Sessões via Cookies HttpOnly com assinatura HMAC-SHA256 e senhas em PBKDF2-HMAC-SHA256
- **Língua**: 100% em português (rotas, documentação, schemas e mensagens)

---

## 📋 Requisitos Atendidos

| Código | Descrição | Status |
| :--- | :--- | :--- |
| **RF01** | Cadastrar respostas da anamnese | ✅ Implementado |
| **RF02** | Receber sintomas detalhados | ✅ Implementado |
| **RF03** | Analisar informações clínicas | ✅ Implementado |
| **RF04** | Identificar sinais de alerta imediatos (*Red Flags*) | ✅ Implementado |
| **RF05** | Anamnese padrão padronizada para todas as pessoas | ✅ Implementado |
| **RF06** | Toda a API e documentação em português | ✅ Implementado |
| **RF07** | Processar as respostas e correlacionar dados | ✅ Implementado |
| **RF08** | Autenticação com cadastro e cookies para consultar histórico | ✅ Implementado |
| **RF09** | Respostas e orientações personalizadas por paciente | ✅ Implementado |
| **RF10** | Indicação de médico/hospital próximo com urgência em casos graves | ✅ Implementado |
| **RF11** | Banco de dados relacional para armazenar as respostas | ✅ Implementado |
| **RNF01** | Resposta em menos de 5 segundos (verificado em testes < 0.5s) | ✅ Atendido |
| **RNF03** | Carregamento da página em menos de 1 segundo | ✅ Atendido |
| **RNF04** | Botões com bordas arredondadas | ✅ Atendido |
| **RNF05** | Paleta de cores frias (branco, cinza e bege) | ✅ Atendido |
| **RNF06** | 100% em português | ✅ Atendido |
| **RNF07** | Controle de acesso estrito ao banco e dados de terceiros | ✅ Atendido |

---

## 🚀 Como Executar o Projeto

### 1. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

### 2. Iniciar o Servidor
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Acessar no Navegador
- **Interface Web**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Documentação Interativa Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentação Alternativa ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Como Executar os Testes Automatizados

A suíte de testes com `pytest` valida o cadastro, autenticação com cookies, regras de triagem e persistência:

```powershell
python -m pytest tests/ -v
```

---

## 📁 Estrutura de Diretórios

```
API médica trabalho final/
├── app/
│   ├── __init__.py
│   ├── config.py                # Configurações do sistema e segurança
│   ├── database.py              # Conexão e sessão com SQLAlchemy
│   ├── models.py                # Modelos ORM: Usuario e Anamnese
│   ├── schemas.py               # Schemas Pydantic em português
│   ├── auth.py                  # Criptografia e gerenciamento de cookies HttpOnly
│   ├── main.py                  # App FastAPI, middleware de performance e rotas
│   ├── services/
│   │   ├── triagem_service.py   # Motor clínico de triagem e orientações personalizadas
│   │   └── anamnese_service.py  # Persistência e busca de histórico no banco
│   ├── routers/
│   │   ├── auth_router.py       # Rotas de cadastro, login, logout e perfil
│   │   ├── anamnese_router.py   # Rotas de anamnese, triagem e consulta
│   │   └── pages_router.py      # Rotas HTML servindo templates Jinja2
│   ├── templates/               # Páginas HTML5
│   │   ├── base.html            # Layout base
│   │   ├── index.html           # Tela inicial, login e cadastro
│   │   ├── anamnese.html        # Formulário padronizado
│   │   ├── resultado.html       # Painel de resultado da triagem
│   │   └── historico.html       # Histórico de anamneses do usuário
│   └── static/                  # Arquivos estáticos puros
│       ├── css/style.css        # CSS puro com botões arredondados e paleta fria/bege
│       └── js/                  # Vanilla JS (app.js, anamnese.js, historico.js)
├── tests/
│   ├── conftest.py              # Fixtures com SQLite isolado em memória
│   ├── test_auth.py             # Testes de cadastro, login e cookies
│   ├── test_triagem.py          # Testes das regras clínicas de triagem
│   └── test_anamnese.py         # Testes de integração e tempo de resposta
├── requirements.txt             # Dependências Python
├── specs.md                     # Especificações funcionais e não-funcionais
├── design_decisions.md          # Decisões arquiteturais do projeto
└── README.md                    # Documentação do sistema
```
