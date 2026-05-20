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

## Testes de Frontend (Manual e Visual)

### Responsividade
- [ ] Verificar integridade do layout em 320px (Mobile).
- [ ] Verificar integridade do layout em 768px (Tablet).
- [ ] Verificar integridade do layout em 1200px+ (Desktop).

### Acessibilidade
- [ ] Verificar ordem de tabulação lógica.
- [ ] Verificar anúncio de atualização de fila por leitores de tela (aria-live).
- [ ] Verificar contraste das combinações Dourado/Branco e Dourado/Marinho.
- [ ] Garantir que o foco é visível em todos os elementos interativos.

### Integração em Tempo Real (SocketIO)
- [ ] Verificar atualização da posição na tela `status.html` quando o sacerdote chama um fiel.
- [ ] Verificar atualização da lista e contagem na fila no `dashboard.html` sem recarregar a página.

### Estados de Interface
- [ ] Verificar estado vazio "Sem sacerdotes disponíveis" na recepção.
- [ ] Verificar feedback de carregamento (*spinner*) ao clicar em "Chamar Próximo".
- [ ] Verificar mensagens de erro em caso de falha na comunicação com a API.
- [ ] Verificar validações visuais nos formulários de identificação.

## Observações

- Os testes usam um banco SQLite temporário em disco.
- As variáveis de ambiente são isoladas por teste para evitar interferência entre execuções.
- A suíte foi ajustada para o estado atual do projeto e deve ser reexecutada após alterações em rotas, modelos ou bootstrap.