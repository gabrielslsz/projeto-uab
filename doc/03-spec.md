# Gratia - visão consolidada

Este documento resume o estado atual do sistema implementado no repositório.

## Escopo

- Recepção pública para escolha de sacerdote disponível.
- Identificação do fiel e entrada em fila.
- Painel do sacerdote com login por PIN, chamada do próximo fiel e alteração de status.
- Atualização em tempo real com SocketIO.

## Persistência

- [app/models/models.py](../app/models/models.py) contém os modelos `Sacerdote`, `Agenda` e `Atendimento`.
- O banco padrão usa SQLite em `app/db/gratia.db` quando `GRATIA_DATABASE_URI` não é definido.

## Inicialização

- [app/__init__.py](../app/__init__.py) cria a factory da aplicação e registra os blueprints.
- [run.py](../run.py) cria a aplicação, garante o diretório do banco e sobe o servidor na porta `5001`.
- [seed.py](../seed.py) cria sacerdotes de teste quando o banco está vazio.

## Rotas principais

- `/` lista sacerdotes disponíveis.
- `/identificacao/<sacerdote_id>` exibe a tela de identificação.
- `/entrar-fila` cria o atendimento.
- `/status/<atendimento_id>` mostra a posição na fila.
- `/sacerdote/login` autentica o sacerdote por PIN.
- `/sacerdote/dashboard` mostra a fila atual.
- `/sacerdote/chamar-proximo` chama o próximo atendimento.
- `/sacerdote/alterar-status` atualiza o status do sacerdote.
- `/sacerdote/logout` encerra a sessão.

## Testes

A suíte automatizada está documentada em [doc/testing.md](doc/testing.md) e cobre os fluxos principais do sistema.
