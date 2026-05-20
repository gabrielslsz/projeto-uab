# Gratia

Sistema Flask para atendimento pastoral com recepção de fiéis, fila em tempo real e painel do sacerdote.

## Dependências

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-SocketIO 5.3.6
- python-dotenv 1.0.0
- pytest 7.4.3
- eventlet 0.33.3

## Estrutura principal

- [config.py](config.py): configuração da aplicação e banco SQLite padrão.
- [run.py](run.py): ponto de entrada da aplicação.
- [seed.py](seed.py): cria sacerdotes de teste quando o banco está vazio.
- [app/models/models.py](app/models/models.py): modelos `Sacerdote`, `Agenda` e `Atendimento`.
- [app/controllers/fiel_controller.py](app/controllers/fiel_controller.py): fluxo público do fiel.
- [app/controllers/sacerdote_controller.py](app/controllers/sacerdote_controller.py): painel e ações do sacerdote.
- [app/templates/](app/templates/): views Jinja2 do sistema.

## Como executar

1. Crie e ative o ambiente virtual.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Se precisar, ajuste `SECRET_KEY` e `GRATIA_DATABASE_URI` no `.env`.
4. Inicie a aplicação com `python run.py`.

A aplicação sobe em `0.0.0.0:5001`.

## Como popular o banco

Execute o seed opcional para criar sacerdotes de teste:

```bash
python seed.py
```

## Como testar

Execute a suíte automatizada com:

```bash
.venv/bin/python -m pytest -q
```

Veja os cenários em [doc/testing.md](doc/testing.md).

## Documentação

- [doc/03-especs.md](doc/03-especs.md)
- [doc/03-spec.md](doc/03-spec.md)
- [doc/04-gratia-specs.md](doc/04-gratia-specs.md)
