# Slack API Documentation

Referência dos endpoints Slack usados para notificações.

## 🔐 Autenticação

Todos os requests requerem header:

```
Authorization: Bearer YOUR_BOT_TOKEN
Content-Type: application/json
```

**Base URL**
```
https://slack.com/api
```

---

## 📊 Endpoints Principais

### 1. Post Message

**Endpoint**
```
POST /chat.postMessage
```

**Request Body**
```json
{
  "channel": "#channel-name ou C1234567890",
  "text": "Message text",
  "blocks": [],
  "thread_ts": "1234567890.123456"
}
```

**Exemplo - Texto Simples**
```bash
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer xoxb-YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "text": "Newsletter criada com sucesso!"
  }'
```

**Exemplo - Com Formatação**
```bash
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer xoxb-YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "Newsletter Report"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "✅ Newsletter criada\n📊 10 itens inclusos\n🎯 Agendado para amanhã"
        }
      }
    ]
  }'
```

**Resposta**
```json
{
  "ok": true,
  "channel": "C1234567890",
  "ts": "1234567890.123456",
  "message": {
    "text": "Message text"
  }
}
```

---

### 2. Update Message

**Endpoint**
```
POST /chat.update
```

**Request Body**
```json
{
  "channel": "C1234567890",
  "ts": "1234567890.123456",
  "text": "Updated message",
  "blocks": []
}
```

---

### 3. React to Message

**Endpoint**
```
POST /reactions.add
```

**Request Body**
```json
{
  "channel": "C1234567890",
  "timestamp": "1234567890.123456",
  "name": "thumbsup"
}
```

---

### 4. Send File

**Endpoint**
```
POST /files.upload
```

**Request Body (Form Data)**
```
file: <arquivo>
channels: C1234567890
title: Report
initial_comment: Check this!
```

---

## 🎨 Block Kit (Formatação Avançada)

### Section Block
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Bold* _italic_ ~strikethrough~ `code`"
  }
}
```

### Context Block (Metadados)
```json
{
  "type": "context",
  "elements": [
    {
      "type": "mrkdwn",
      "text": "📅 May 3, 2026"
    }
  ]
}
```

### Divider
```json
{
  "type": "divider"
}
```

### Button
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Clique no botão"
  },
  "accessory": {
    "type": "button",
    "text": {
      "type": "plain_text",
      "text": "View Newsletter"
    },
    "url": "https://example.com"
  }
}
```

---

## 📋 Formatação de Texto

| Formato | Sintaxe | Resultado |
|---------|---------|-----------|
| Bold | `*text*` | **text** |
| Italic | `_text_` | _text_ |
| Strikethrough | `~text~` | ~~text~~ |
| Code | `` `text` `` | `text` |
| Link | `<https://url\|label>` | [label](url) |
| Menção | `<@USERID>` | @user |

---

## ⚠️ Erros Comuns

| Código | Erro | Solução |
|--------|------|---------|
| `not_authed` | Token inválido | Verifique Bot Token |
| `invalid_auth` | Token expirou | Regenere o token |
| `channel_not_found` | Canal não existe | Verifique Channel ID |
| `rate_limited` | Rate limit | Aguarde 1 minuto |
| `not_in_channel` | Bot não está no canal | Adicione manualmente |

---

## 📌 Rate Limiting

- Limite: **50 requests** por segundo (por método)
- **Rate limit headers**:
  - `Retry-After: 10`

---

## 🔗 Referências

- [Slack API Oficial](https://api.slack.com/)
- [Block Kit](https://api.slack.com/block-kit)
- [Message Formatting](https://slack.com/help/articles/202288908)
- [[setup/slack-setup|Slack Setup Guide]]
- [[_index|Voltar ao índice]]
