# Relatório de Inspeção de Segurança - Projeto Gratia

## Resumo Executivo

Esta inspeção detalhada de cibersegurança foi realizada no projeto Gratia para identificar vulnerabilidades com base nas melhores práticas de desenvolvimento seguro e no Top 10 da OWASP.

### Contagem de Achados por Severidade

| Severidade | Quantidade |
| :--- | :--- |
| Crítica | 1 |
| Alta | 2 |
| Média | 2 |
| Baixa | 1 |
| **Total** | **6** |

### As 5 Ações Mais Urgentes

1. **Hash de Credenciais:** Implementar hashing (ex: Argon2 ou BCrypt) para os PINs de acesso dos sacerdotes.
2. **Desativar Modo Debug:** Remover `debug=True` do ponto de entrada da aplicação em produção.
3. **Segurança de Segredos:** Eliminar segredos padrão (default values) para `SECRET_KEY`.
4. **Restrição de CORS:** Limitar as origens permitidas no SocketIO em vez de usar `*`.
5. **Atualização de Dependências:** Revisar e atualizar bibliotecas para mitigar vulnerabilidades conhecidas (CVEs).

---

## Detalhamento das Vulnerabilidades (Nível: SUPERFICIAL)

### 1. Armazenamento de Credenciais em Texto Claro
- **Localização:** `app/models/models.py` (Classe `Sacerdote`), `app/controllers/sacerdote_controller.py` (Função `login`)
- **Descrição:** O PIN de acesso do sacerdote é armazenado e comparado em texto claro no banco de dados.
- **Evidência:**
  ```python
  # app/models/models.py
  pin_acesso = db.Column(db.String(256), nullable=False)
  
  # app/controllers/sacerdote_controller.py
  sacerdote = Sacerdote.query.filter_by(pin_acesso=pin).first()
  ```
- **Impacto Potencial:** Em caso de vazamento do banco de dados, todos os PINs de acesso estarão expostos, permitindo acesso não autorizado.
- **Nível de Severidade:** Crítica
- **Recomendação:** Utilizar uma biblioteca como `Werkzeug.security` para gerar hashes dos PINs e a função `check_password_hash` para verificação.
- **Referências:** OWASP A07:2021 – Authentication Failures, CWE-256.

### 2. Modo Debug Ativado em Produção
- **Localização:** `run.py`, linha 22
- **Descrição:** A aplicação é iniciada com o modo de depuração ativado (`debug=True`).
- **Evidência:**
  ```python
  socketio.run(app, debug=True, host="0.0.0.0", port=5001)
  ```
- **Impacto Potencial:** Exposição de informações sensíveis do sistema (código-fonte, variáveis de ambiente) em caso de erro, além de permitir execução remota de código através do debugger interativo.
- **Nível de Severidade:** Alta
- **Recomendação:** Desativar o modo debug ou utilizar uma variável de ambiente para controlá-lo.
- **Referências:** OWASP A02:2021 – Security Misconfiguration, CWE-489.

### 3. Uso de Chave Secreta Padrão (Hardcoded)
- **Localização:** `config.py`, linha 8
- **Descrição:** O sistema define uma `SECRET_KEY` padrão caso a variável de ambiente não esteja presente.
- **Evidência:**
  ```python
  SECRET_KEY = os.getenv("SECRET_KEY", "gratia-secret-key-123")
  ```
- **Impacto Potencial:** Chaves conhecidas permitem que atacantes assinem seus próprios cookies de sessão, levando ao sequestro de contas e escalada de privilégios.
- **Nível de Severidade:** Alta
- **Recomendação:** Remover o valor padrão e lançar um erro caso a `SECRET_KEY` não seja fornecida via ambiente.
- **Referências:** OWASP A02:2021 – Security Misconfiguration, CWE-798.

### 4. Configuração Permissiva de CORS
- **Localização:** `app/__init__.py`, linha 15
- **Descrição:** O SocketIO está configurado para aceitar conexões de qualquer origem (`*`).
- **Evidência:**
  ```python
  socketio.init_app(app, cors_allowed_origins="*")
  ```
- **Impacto Potencial:** Permite que sites maliciosos interajam com o servidor SocketIO em nome do usuário (Cross-Site WebSocket Hijacking).
- **Nível de Severidade:** Média
- **Recomendação:** Definir uma lista explícita de origens permitidas baseada no domínio oficial.
- **Referências:** OWASP A01:2021 – Broken Access Control, CWE-942.

### 5. Dependências Desatualizadas e Potencialmente Vulneráveis
- **Localização:** `requirements.txt`
- **Descrição:** Versões fixas e antigas de bibliotecas como Flask (3.0.0) podem conter vulnerabilidades conhecidas.
- **Evidência:**
  ```text
  Flask==3.0.0
  ```
- **Impacto Potencial:** Exploração de falhas já corrigidas em versões mais recentes dos frameworks.
- **Nível de Severidade:** Média
- **Recomendação:** Executar auditoria de dependências (`pip audit`) e atualizar para versões estáveis mais recentes.
- **Referências:** OWASP A03:2021 – Software Supply Chain Failures.

### 6. Exposição do Servidor em Todas as Interfaces (0.0.0.0)
- **Localização:** `run.py`, linha 22
- **Descrição:** O servidor escuta em `0.0.0.0`, expondo a aplicação em todas as interfaces de rede disponíveis.
- **Evidência:**
  ```python
  socketio.run(app, debug=True, host="0.0.0.0", port=5001)
  ```
- **Impacto Potencial:** Exposição desnecessária do serviço em redes públicas ou não confiáveis se o host possuir múltiplas interfaces.
- **Nível de Severidade:** Baixa
- **Recomendação:** Vincular o serviço ao `127.0.0.1` em desenvolvimento e usar um servidor reverso (Nginx) em produção.
- **Referências:** Best Practices for Deployment.
