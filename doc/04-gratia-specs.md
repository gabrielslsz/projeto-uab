# Especificação: Gratia - Sistema de Atendimento Pastoral

## 1. Visão Geral
Sistema focado em agendamento e gerenciamento de filas para confissões e atendimentos paroquiais.

## 2. Requisitos de Negócio e UX
- **Sigilo e Privacidade:** O sistema deve anonimizar dados de atendimento imediatamente após a conclusão.
- **Acessibilidade:** Elementos visuais grandes (mínimo 18px), alto contraste e fluxos lineares.
- **Tone of Voice:** Pastoral, acolhedor e respeitoso.

## 3. Modelagem de Dados (Camada de Persistência)

### 3.1. Sacerdote (Entity)
- `id`: UUID
- `nome`: String (Ex: "Padre Antônio")
- `foto_url`: String (Opcional)
- `pin_acesso`: String (Hashed - 6 dígitos)
- `status`: Enum (DISPONIVEL, PAUSADO, OFFLINE)

### 3.2. Agenda (Entity)
- `id`: UUID
- `sacerdote_id`: FK
- `dia_semana`: Enum (SEG-DOM)
- `hora_inicio`: Time
- `hora_fim`: Time
- `vagas_agendadas`: Integer (Máximo de agendamentos fixos)
- `permite_fila_no_dia`: Boolean

### 3.3. Atendimento (Transaction - Dados Efêmeros)
- `id`: UUID
- `identificador_exibicao`: String (Ex: "Gabriel" ou "C-42")
- `telefone`: String (Para notificações)
- `tipo`: Enum (AGENDADO, FILA_PRESENCIAL)
- `status`: Enum (AGUARDANDO, CHAMADO, CONCLUIDO, CANCELADO)
- `horario_previsto`: DateTime
- `criado_em`: DateTime (Deletar após 24h)

## 4. Fluxo de Notificações
1. **Confirmação:** Imediata ao entrar na fila/agendar.
2. **Alerta de Proximidade:** Quando `posicao_fila == 2`.
3. **Chamada:** Quando o Sacerdote clica em "Chamar".

## 5. Regras de Segurança
- Uso de JWT para Sacerdotes e Secretaria.
- Links assinados (Signed URLs) para Fiéis acessarem seu status sem precisar de senha.
- Implementar "Soft Delete" e "Hard Cleanup" diário.
