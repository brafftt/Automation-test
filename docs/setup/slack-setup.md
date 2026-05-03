# Setup: Slack

Guia para configurar notificações via Slack.

## 📋 Pré-requisitos

- Workspace Slack ativo
- Acesso de admin ao workspace
- Canal Slack onde enviar notificações

## 🤖 Criando Bot Slack

### 1. Criar App no Slack

1. Ir para [Slack API](https://api.slack.com/apps)
2. Clicar em **Create New App**
3. Selecionar **From scratch**
4. Nome: "Meta Ads Newsletter Bot"
5. Selecionar seu workspace
6. Clicar em **Create App**

### 2. Configurar Permissões

1. Na aba **OAuth & Permissions**
2. Scroll para **Scopes**
3. Em **Bot Token Scopes**, adicionar:
   ```
   chat:write
   chat:read
   channels:read
   users:read
   ```

### 3. Instalar Bot no Workspace

1. Voltar para **OAuth & Permissions**
2. Clicar em **Install to Workspace**
3. Autorizar o acesso
4. Copiar o **Bot User OAuth Token** (começa com `xoxb-`)

## 📍 Obter Channel ID

### Opção 1: Via Slack Desktop
1. Abrir o canal desejado
2. Clicar no nome do canal (topo)
3. Procurar por "Channel details"
4. Copiar o **Channel ID** (formato: C1234567)

### Opção 2: Via API
```bash
curl -X GET "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer YOUR_BOT_TOKEN"
```

## 🔐 Salvando Credenciais

Adicionar ao `.claude/settings.local.json`:

```json
{
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-seu_token_aqui",
    "SLACK_CHANNEL_ID": "C1234567890"
  }
}
```

## 🧪 Testando

### Enviar Mensagem de Teste

```bash
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer xoxb-YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"#test-channel","text":"Hello from Meta Ads Automation!"}'
```

Resposta esperada:
```json
{
  "ok": true,
  "channel": "C1234567",
  "ts": "1234567890.123456",
  "message": {
    "text": "Hello from Meta Ads Automation!"
  }
}
```

## 📚 Referências

- [[apis/slack-api|Slack API Documentation]]
- [Slack API Official](https://api.slack.com/)
- [Bot Best Practices](https://api.slack.com/best-practices)
- [[_index|Voltar ao índice]]
