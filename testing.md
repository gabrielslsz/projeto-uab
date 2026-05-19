# Plano de Testes (TDD First) - Sistema de Atendimento

Este documento descreve a estratégia de testes automatizados para o sistema, priorizando cenários críticos e seguindo a metodologia TDD (Test Driven Development).

## 1. Estratégia de Testes

- **Framework:** `pytest`
- **Abordagem:** Testes de Unidade e Integração.
- **Banco de Dados de Teste:** SQLite em memória (`sqlite:///:memory:`) para isolamento e velocidade.
- **Isolamento:** Uso de fixtures do pytest para setup e teardown do contexto da aplicação.

## 2. Cenários de Teste por Funcionalidade

### 2.1. Modelos de Dados (Camada de Dados)
**Foco:** Validação de integridade e lógica de negócio embutida.

- **TC-01: Criptografia de Senha (UsuarioModel)**
  - **Cenário:** Verificar se a senha plana nunca é armazenada e se o hash é gerado corretamente.
  - **Critério de Sucesso:** `check_senha` retorna `True` para a senha correta e `False` para incorreta.
- **TC-02: Integridade de Enum (TicketModel)**
  - **Cenário:** Tentar criar um ticket com status fora dos permitidos (ABERTO, EM_ATENDIMENTO, RESOLVIDO).
  - **Critério de Sucesso:** O sistema deve lançar um erro de integridade.

### 2.2. Autenticação (Auth Controller)
**Foco:** Segurança e controle de acesso inicial.

- **TC-03: Login com Sucesso**
  - **Cenário:** Enviar credenciais válidas via POST para `/login`.
  - **Critério de Sucesso:** Retorno status 200 e dados do usuário na sessão.
- **TC-04: Login com Credenciais Inválidas**
  - **Cenário:** Enviar email inexistente ou senha errada.
  - **Critério de Sucesso:** Retorno status 401 e mensagem de erro "Credenciais Inválidas".
- **TC-05: Auto-cadastro de Cliente (Email Único)**
  - **Cenário:** Tentar cadastrar um cliente com um email que já existe na base.
  - **Critério de Sucesso:** Retorno status 400 e mensagem "Email já em uso".

### 2.3. Administração (Administrador Controller)
**Foco:** RBAC (Role-Based Access Control) e Auditoria.

- **TC-06: Criação de Atendente (Acesso Autorizado)**
  - **Cenário:** Usuário com role `ADMINISTRADOR` tenta criar um atendente.
  - **Critério de Sucesso:** Status 201, registro no banco e log de operação gerado.
- **TC-07: Criação de Atendente (Acesso Negado)**
  - **Cenário:** Usuário com role `CLIENTE` ou `ATENDENTE` tenta acessar a rota de criação.
  - **Critério de Sucesso:** Status 403 (Forbidden).

## 3. Execução dos Testes

Os testes devem ser executados antes de cada commit para garantir que não houve regressões.

```bash
# Executar todos os testes
pytest

# Executar com relatório de cobertura (se instalado pytest-cov)
pytest --cov=app tests/
```

## 4. Próximos Passos (TDD Workflow)

1. Criar o arquivo de teste em `tests/`.
2. Definir a fixture `app` e `client` em `tests/conftest.py`.
3. Implementar o teste (que falhará inicialmente).
4. Implementar/Ajustar o código na `app/` para fazer o teste passar.
