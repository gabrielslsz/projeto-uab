# Testes Automatizados

## Pré-requisitos

- Python 3.10 ou superior
- Ambiente virtual local recomendado em `.venv`

## Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Execução

```bash
.venv/bin/python -m pytest -q
```

## Escopo coberto

- Registro dos blueprints da aplicação
- Criação do Proprietário inicial no bootstrap
- Fluxo de login por role
- Criação de atendente e auditoria da operação
- Escoamento da fila de jobs antes da validação do log assíncrono
- Reutilização do cache de lookup de usuário durante autenticação e cadastro