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

## Cenários de frontend

- Renderização condicional das páginas `GET /login`, `GET /cadastro-cliente`, `GET /admin/painel`, `GET /proprietario/painel`, `GET /atendente/painel` e `GET /cliente/painel`.
- Verificação de responsividade por presença de classes e estruturas base compatíveis com desktop, tablet e mobile.
- Verificação de acessibilidade básica por presença de `skip-link`, labels, `aria-live`, `aria-atomic`, `autocomplete` e foco visível nos assets.
- Validação de estados vazios nos painéis.
- Validação de loading, erro e timeout no envio de formulários com `data-enhanced-form`.
- Integração com as respostas do backend em texto, JSON e redirecionamento.
- Regressoes visuais por verificação dos tokens do layout compartilhado, skeleton e componentes Jinja reutilizáveis.

## Observação de execução

- Os cenários automatizados nesta base usam o `pytest` com o cliente de teste do Flask e inspeção dos assets estáticos.
- Não há runner de navegador dedicado neste repositório; os testes de frontend são cobertos por renderização de páginas, integração HTTP e inspeção de assets.