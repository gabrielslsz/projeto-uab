# Estado Atual da Implementação

Este documento descreve o estado real do projeto após o alinhamento com `doc/03-especs.md`.

## Base técnica

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- python-dotenv 1.0.0
- gunicorn 21.2.0

## Configuração e bootstrap

- `config.py` carrega as variáveis de ambiente com `dotenv` e expõe `Config`.
- `app/database.py` mantém a instância única de `SQLAlchemy`.
- `app/__init__.py` cria a aplicação com `create_app()` e registra os blueprints `auth`, `proprietario`, `administrador`, `atendente` e `cliente`.
- `run.py` inicializa o banco, cria o diretório do SQLite quando necessário e garante a criação do usuário Proprietário inicial.

## Modelos

- `app/models/usuario_model.py` define `UsuarioModel` com `nome`, `email`, `senha_hash`, `role` e `criado_por_id`.
- `app/models/ticket_model.py` define `TicketModel` com `cliente_id`, `assunto`, `descricao`, `status`, `data_criacao` e `data_atualizacao`.
- `app/models/log_model.py` define `LogOperacaoModel` com `usuario_id`, `acao`, `tabela_afetada`, `registro_afetado_id` e `data_hora`.
- `app/models/models.py` foi mantido como camada de compatibilidade para imports legados.

## Controladores

- `app/controllers/auth_controller.py` implementa `POST /login` e `POST /cadastro-cliente`.
- `app/controllers/administrador_controller.py` implementa a verificação de permissão e `POST /admin/atendentes/novo`.
- `app/controllers/proprietario_controller.py`, `app/controllers/atendente_controller.py` e `app/controllers/cliente_controller.py` expõem painéis mínimos para suportar os redirecionamentos.

## Otimizações internas

- A busca de usuários por email é cacheada em memória e invalidada após cadastros para reduzir consultas repetidas.
- A auditoria de criação de atendentes é enfileirada em um job leve em memória, mantendo a resposta da requisição mais previsível.
- A implementação usa apenas biblioteca padrão para cache e fila, sem adicionar dependências externas.

## Apresentação

- `app/templates/base.html` fornece a estrutura base com Bootstrap e layout neutro para as páginas Jinja2.
- Os templates legados do fluxo anterior permanecem no repositório, mas não fazem parte do novo caminho principal da aplicação.

## Execução

- A aplicação principal sobe com `python run.py`.
- O servidor escuta em `0.0.0.0:5000`.
- O banco padrão usa SQLite em `app/db/atendimento.db` quando `DATABASE_URI` não é definido.