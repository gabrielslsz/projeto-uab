# Testes do Gratia

Este documento descreve a suíte automatizada que valida o comportamento atual do projeto.

## Como executar

Use o Python do ambiente virtual do projeto:

```bash
.venv/bin/python -m pytest -q
```

## Cenários cobertos

- A factory da aplicação registra apenas os blueprints existentes: `fiel` e `sacerdote`.
- A rota `/` lista sacerdotes com status `DISPONIVEL`.
- A rota `/entrar-fila` cria um atendimento e redireciona para a tela de status.
- A rota `/status/<atendimento_id>` exibe o nome informado e a posição atual na fila.
- A rota `/sacerdote/login` autentica pelo PIN e redireciona para o painel.
- A rota `/sacerdote/dashboard` mostra o sacerdote autenticado e o próximo atendimento.
- A rota `/sacerdote/chamar-proximo` altera o primeiro atendimento pendente para `CHAMADO`.
- A rota `/sacerdote/alterar-status` atualiza o status do sacerdote via JSON.
- O script `seed.py` cria os sacerdotes de teste quando o banco está vazio.

## Observações

- Os testes usam um banco SQLite temporário em disco.
- As variáveis de ambiente são isoladas por teste para evitar interferência entre execuções.
- A suíte foi ajustada para o estado atual do projeto e deve ser reexecutada após alterações em rotas, modelos ou bootstrap.
