# Sistema de Atendimento

Este é um sistema web de atendimento desenvolvido com Flask, focado em segurança, RBAC (Controle de Acesso Baseado em Roles) e auditoria.

## Requisitos Técnicos
- **Linguagem:** Python 3.10+
- **Framework:** Flask 3.0.0
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Banco de Dados:** SQLite (local)
- **Autenticação:** Baseada em Sessão com Hashing de Senhas (Werkzeug)
- **Front-end:** Templates Jinja2 com Bootstrap 5.3

## Estrutura do Projeto
- `app/`: Núcleo da aplicação.
  - `controllers/`: Gerenciamento de rotas e lógica de controle (Blueprints).
  - `models/`: Definição das entidades e regras de banco de dados.
  - `templates/`: Interface do usuário.
- `tests/`: Suite de testes automatizados (Pytest).
- `config.py`: Configurações globais e carregamento de `.env`.
- `run.py`: Script de inicialização.

## Como Executar

### 1. Configuração do Ambiente
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```bash
SECRET_KEY=sua_chave_secreta
DATABASE_URI=sqlite:///atendimento.db
DEBUG_MODE=True
PROPRIETARIO_EMAIL=admin@empresa.com
PROPRIETARIO_PASSWORD=admin123
```

### 3. Rodar a Aplicação
```bash
python run.py
```
O sistema criará automaticamente as tabelas e o usuário Proprietário inicial no primeiro acesso.

## Testes Automatizados
Para garantir a estabilidade do sistema, execute:
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest
```

## Documentação de Suporte
- `doc/03-spec.md`: Especificações técnicas detalhadas.
- `testing.md`: Plano de testes e critérios de aceite.
