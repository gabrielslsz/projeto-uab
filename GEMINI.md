# Projeto Sistema de Atendimento

Este projeto é um sistema de atendimento desenvolvido com Flask, seguindo as especificações em `doc/03-especs.md`.

## Estrutura do Projeto

- `app/`: Código fonte da aplicação Flask.
  - `controllers/`: Blueprints para as rotas da aplicação.
  - `models/`: Modelos do SQLAlchemy.
  - `templates/`: Templates HTML (Jinja2).
  - `database.py`: Inicialização do SQLAlchemy.
- `config.py`: Configurações da aplicação.
- `run.py`: Ponto de entrada da aplicação.
- `requirements.txt`: Dependências do Python.
- `.env`: Variáveis de ambiente (não versionado).
- `Dockerfile`: Configuração para containerização.

## Como Executar

### Localmente

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` (baseado no `.env.example`).

4. Execute a aplicação:
   ```bash
   python run.py
   ```

A aplicação estará disponível em `http://localhost:5000`. No primeiro acesso, um usuário Proprietário inicial será criado com as credenciais definidas no `.env`.

### Docker

1. Construa a imagem:
   ```bash
   docker build -t sistema-atendimento .
   ```

2. Execute o container:
   ```bash
   docker run -p 5000:5000 --env-file .env sistema-atendimento
   ```

## Convenções de Desenvolvimento

- Use Blueprints para organizar rotas por funcionalidade.
- Mantenha os modelos em `app/models/`.
- Siga o padrão PEP 8 para código Python.
- Sempre atualize o `requirements.txt` ao adicionar novas dependências.
