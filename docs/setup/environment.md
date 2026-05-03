# Variáveis de Ambiente

Guia completo sobre configuração de variáveis de ambiente.

## 📝 Arquivo de Configuração

### Localização
```
.claude/settings.local.json
```

### Formato

```json
{
  "env": {
    "META_ACCESS_TOKEN": "seu_token",
    "META_BUSINESS_ACCOUNT_ID": "seu_id",
    "GHL_API_KEY": "sua_chave",
    "GHL_BUSINESS_ID": "seu_id",
    "SLACK_BOT_TOKEN": "xoxb-seu_token",
    "SLACK_CHANNEL_ID": "C1234567890",
    "NEWSLETTER_FROM_EMAIL": "seu_email@example.com",
    "NEWSLETTER_FROM_NAME": "Your Name",
    "LOG_LEVEL": "INFO"
  }
}
```

## 🔐 Variáveis Obrigatórias

| Variável | Descrição | Obtém em |
|----------|-----------|----------|
| `META_ACCESS_TOKEN` | Token de acesso da Meta | [[setup/meta-setup|Meta Setup]] |
| `META_BUSINESS_ACCOUNT_ID` | ID da conta de negócios | [[setup/meta-setup|Meta Setup]] |
| `GHL_API_KEY` | Chave de API do GHL | [[setup/ghl-setup|GHL Setup]] |
| `GHL_BUSINESS_ID` | ID do negócio no GHL | [[setup/ghl-setup|GHL Setup]] |
| `SLACK_BOT_TOKEN` | Token do bot Slack | [[setup/slack-setup|Slack Setup]] |
| `SLACK_CHANNEL_ID` | ID do canal Slack | [[setup/slack-setup|Slack Setup]] |

## 📌 Variáveis Opcionais

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `NEWSLETTER_FROM_EMAIL` | - | Email de origem |
| `NEWSLETTER_FROM_NAME` | - | Nome para exibir |
| `LOG_LEVEL` | `INFO` | Nível de logging |

## ✅ Verificando Configuração

### Testar Credenciais

```bash
# Meta
curl -X GET "https://graph.instagram.com/me?access_token=YOUR_TOKEN"

# GHL
curl -X GET "https://api.gohighlevel.com/v1/calendars" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Slack
curl -X POST "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer YOUR_BOT_TOKEN"
```

### Verificar Arquivo Local

```bash
cat .claude/settings.local.json
```

## 🚨 Segurança

- ✅ `.claude/settings.local.json` está em `.gitignore`
- ✅ Nunca commitar credenciais
- ✅ Usar variáveis de ambiente em produção
- ✅ Regenerar tokens regularmente
- ✅ Revogar acesso quando não usar mais

## 🔄 Recarregar Variáveis

```python
import os
from dotenv import load_dotenv

# Recarregar de .env
load_dotenv()

# Obter variáveis
token = os.getenv('META_ACCESS_TOKEN')
```

## 🔗 Referências

- [[setup/meta-setup|Meta Setup]]
- [[setup/ghl-setup|GHL Setup]]
- [[setup/slack-setup|Slack Setup]]
- [[_index|Voltar ao índice]]
