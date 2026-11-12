# API de Gestão de Pedidos com FastAPI

Projeto desenvolvido durante meus estudos práticos de desenvolvimento back-end com Python, acompanhando aulas guiadas para consolidar a construção de APIs REST, autenticação de usuários e integração com banco de dados relacional.

## 🎯 Objetivos de Aprendizado
Durante a implementação deste projeto, pude praticar e compreender na prática:
* Estruturação de rotas modularizadas utilizando `APIRouter` (separando autenticação e pedidos).
* Validação e serialização de dados de entrada e saída com **Pydantic** (`schemas.py`).
* Mapeamento Objeto-Relacional (ORM) e relacionamentos entre tabelas com **SQLAlchemy** (`models.py`).
* Versionamento e migrações de esquema de banco de dados utilizando **Alembic**.
* Fluxo de autenticação e autorização com tokens **JWT** (Access Token e Refresh Token) e criptografia de senhas com `bcrypt`.
* Boas práticas de segurança, como o isolamento de variáveis sensíveis via `.env` e `.gitignore`.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **FastAPI** & **Uvicorn**
* **SQLAlchemy** (ORM)
* **Alembic** (Migrations)
* **SQLite** (Banco de dados local)
* **Pydantic** (Validação de dados)
* **Python-JOSE** & **Passlib / Bcrypt** (Segurança e JWT)
