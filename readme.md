# Sistema de Atendimento

Projeto Flask alinhado à especificação em `doc/03-especs.md`.

## O que está implementado

- Configuração por variáveis de ambiente com `dotenv`
- Factory da aplicação com registro de blueprints modulares
- Modelos de usuários, tickets e logs de operação
- Login, cadastro de cliente e criação de atendente com auditoria
- Bootstrap do usuário Proprietário inicial no primeiro boot

## Dependências

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- python-dotenv 1.0.0
- gunicorn 21.2.0
- pytest 7.4.3

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Configure `.env` com base em `.env.example`.
4. Inicie a aplicação com `python run.py`.

## Como testar

Execute `pytest -q` dentro do ambiente virtual já com as dependências instaladas. A configuração detalhada está em `doc/testing.md`.