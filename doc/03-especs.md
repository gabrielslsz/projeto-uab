# Especificação do sistema Gratia

Esta versão documenta exatamente o que existe no projeto atual, sem incluir módulos que não estão mais presentes.

## 1. Configuração e ambiente

### [requirements.txt](../requirements.txt)
Dependências usadas pelo projeto:

- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-SocketIO==5.3.6
- python-dotenv==1.0.0
- pytest==7.4.3
- eventlet==0.33.3

### [config.py](../config.py)
Carrega as variáveis do `.env` e define a configuração global da aplicação.

- `SECRET_KEY` usa `SECRET_KEY` do ambiente ou o valor padrão `gratia-secret-key-123`.
- `SQLALCHEMY_DATABASE_URI` usa `GRATIA_DATABASE_URI` quando existir.
- Quando `GRATIA_DATABASE_URI` não é informado, o padrão é `sqlite:///app/db/gratia.db`.
- `SQLALCHEMY_TRACK_MODIFICATIONS` fica desativado.

## 2. Inicialização e infraestrutura

### [app/database.py](../app/database.py)
Mantém a instância única do SQLAlchemy.

### [app/__init__.py](../app/__init__.py)
Define a factory `create_app()`.

- Cria a instância Flask.
- Carrega `Config`.
- Inicializa `db`.
- Inicializa `socketio` com `cors_allowed_origins="*"`.
- Registra os blueprints `fiel_bp` e `sacerdote_bp`.

### [run.py](../run.py)
É o ponto de entrada da aplicação.

- Cria a aplicação com `create_app()`.
- Garante que a pasta `app/db` exista.
- Importa os modelos `Sacerdote`, `Agenda` e `Atendimento` antes do `create_all()`.
- Executa o servidor com `socketio.run(...)` em `0.0.0.0:5001` com `debug=True`.

## 3. Camada de dados

### [app/models/models.py](../app/models/models.py)
O projeto usa três modelos principais.

#### `Sacerdote`
- Tabela `sacerdotes`.
- `id` como UUID em string.
- `nome` obrigatório.
- `pin_acesso` obrigatório.
- `status` com valores `DISPONIVEL`, `PAUSADO` e `OFFLINE`, com padrão `OFFLINE`.
- Relacionamento com `Agenda`.

#### `Agenda`
- Tabela `agendas`.
- `id` como UUID em string.
- `sacerdote_id` com chave estrangeira para `sacerdotes.id`.
- `dia_semana` de 0 a 6.
- `hora_inicio` e `hora_fim` como horário.
- `vagas_agendadas` com padrão 10.
- `permite_fila` com padrão `True`.

#### `Atendimento`
- Tabela `atendimentos`.
- `id` como UUID em string.
- `identificador_exibicao` obrigatório.
- `telefone` opcional.
- `status` com valores `AGUARDANDO`, `CHAMADO`, `CONCLUIDO` e `CANCELADO`, com padrão `AGUARDANDO`.
- `tipo` com valores `AGENDADO` e `FILA`, com padrão `FILA`.
- `sacerdote_id` com chave estrangeira para `sacerdotes.id`.
- `criado_em` com `datetime.utcnow`.

## 4. Camada de controle

### [app/controllers/fiel_controller.py](../app/controllers/fiel_controller.py)
Blueprint `fiel_bp`.

- `GET /` mostra a recepção e lista sacerdotes com status `DISPONIVEL`.
- `GET /identificacao/<sacerdote_id>` abre a tela de identificação.
- `POST /entrar-fila` cria um atendimento na fila, gera nome automático se vier vazio e emite evento `novo_fiel` via SocketIO.
- `GET /status/<atendimento_id>` exibe o status e calcula a posição na fila.

### [app/controllers/sacerdote_controller.py](../app/controllers/sacerdote_controller.py)
Blueprint `sacerdote_bp`.

- `GET` e `POST /sacerdote/login` validam o PIN do sacerdote.
- `GET /sacerdote/dashboard` mostra a fila atual e o próximo atendimento.
- `POST /sacerdote/chamar-proximo` altera o primeiro atendimento pendente para `CHAMADO` e emite `proximo_chamado`.
- `POST /sacerdote/alterar-status` atualiza o status do sacerdote via JSON.
- `GET /sacerdote/logout` limpa a sessão.

## 5. Camada de apresentação

### [app/templates/base.html](../app/templates/base.html)
Template base com Bootstrap 5, Google Fonts e identidade visual do projeto.

### Templates existentes

- [app/templates/fiel/recepcao.html](../app/templates/fiel/recepcao.html)
- [app/templates/fiel/identificacao.html](../app/templates/fiel/identificacao.html)
- [app/templates/fiel/status.html](../app/templates/fiel/status.html)
- [app/templates/sacerdote/login.html](../app/templates/sacerdote/login.html)
- [app/templates/sacerdote/dashboard.html](../app/templates/sacerdote/dashboard.html)

## 6. Fluxo principal

1. O fiel entra pela recepção em `/`.
2. Seleciona um sacerdote disponível e informa seus dados.
3. O sistema cria um registro em `atendimentos`.
4. O sacerdote faz login com PIN em `/sacerdote/login`.
5. O painel mostra a fila e permite chamar o próximo atendimento.
6. Os eventos de fila são emitidos em tempo real com SocketIO.

## 7. Bootstrap e dados de teste

### [seed.py](../seed.py)
Script auxiliar para popular o banco com sacerdotes de teste quando necessário.

- Usa `create_app()` para criar o contexto da aplicação.
- Garante a existência da pasta `app/db`.
- Executa `db.create_all()` antes de consultar o banco.
- Cria os sacerdotes `Padre Antônio` e `Padre José` quando a tabela está vazia.

## 8. Cobertura automatizada

### [tests/test_app.py](../tests/test_app.py)
Os testes automatizados cobrem os fluxos existentes no projeto:

- Registro dos blueprints carregados pela factory.
- Renderização da recepção com sacerdotes disponíveis.
- Entrada de fiel na fila e consulta do status.
- Login do sacerdote, visualização do painel, chamada do próximo fiel e alteração de status.
- Execução do `seed.py` com criação dos sacerdotes de teste.
