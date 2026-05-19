# Componentes de Frontend

## Base compartilhada

- `app/templates/base.html` define a estrutura geral, barra superior, área principal e carregamento dos assets compartilhados.

## Componentes Jinja

- `app/templates/_components.html` centraliza estados de mensagens, feedback de formulários e estados vazios.

## Estilos

- `app/static/css/frontend.css` concentra tokens de cor, foco visível, layout responsivo, estados vazios e skeletons.

## Comportamento interativo

- `app/static/js/frontend.js` intercepta formulários marcados com `data-enhanced-form`, controla loading, timeout, erro, retry e resposta de integração com o backend.

## Telas

- `app/templates/auth/login.html`.
- `app/templates/auth/cadastro_cliente.html`.
- `app/templates/administrador/painel.html`.
- `app/templates/proprietario/painel.html`.
- `app/templates/atendente/painel.html`.
- `app/templates/cliente/painel.html`.