URL Shortener com FastAPI e SQLAlchemy
Um encurtador de URLs moderno e assíncrono, desenvolvido com FastAPI, SQLAlchemy Async e
SQLite, com estrutura escalável, suporte a múltiplos usuários e preparado para load balancing.
Tecnologias Utilizadas
- FastAPI — framework web assíncrono e performático
- SQLAlchemy Async — ORM moderno com suporte a operações assíncronas
- SQLite — banco de dados leve e simples
- Uvicorn — servidor ASGI para rodar a aplicação
- Pytest + HTTPX — suíte de testes automatizados
- Pydantic — para validação e tipagem de dados
- Alembic (opcional) — migração de banco de dados


Instalação e Configuração
1. Clonar o repositório
git clone https://github.com/leodymann/url_shortener.git
cd url_shortener

2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate # Linux / macOS
venv\Scripts\activate # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Executar a aplicação
uvicorn app.main:app --reload
Acesse no navegador: http://127.0.0.1:8000/docs

Endpoints Principais
POST /urls/
Cria uma URL encurtada.
GET /{short_hash}
Redireciona automaticamente para a URL original.

Leody — Projeto pessoal de aprendizado e prática com FastAPI