# Meta Ads API Documentation

Referência completa dos endpoints da Meta Ads API usados neste projeto.

## 🔐 Autenticação

Todos os requests requerem o token de acesso:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

ou como query parameter:

```
?access_token=YOUR_ACCESS_TOKEN
```

## 📊 Endpoints

### 1. Get Business Account

**Endpoint**
```
GET /v18.0/me
```

**Query Parameters**
```
access_token: string (obrigatório)
fields: string (opcional)
```

**Exemplo**
```bash
curl -X GET "https://graph.instagram.com/v18.0/me?access_token=TOKEN"
```

**Resposta**
```json
{
  "id": "123456789",
  "name": "Your Business Name",
  "email": "your@email.com"
}
```

---

### 2. List Campaigns

**Endpoint**
```
GET /v18.0/{BUSINESS_ID}/campaigns
```

**Query Parameters**
```
access_token: string (obrigatório)
fields: string (opcional) - default: id,name,status,created_time
limit: integer (opcional) - padrão: 25, máximo: 500
after: string (opcional) - cursor para paginação
```

**Exemplo**
```bash
curl -X GET "https://graph.instagram.com/v18.0/YOUR_BUSINESS_ID/campaigns?access_token=TOKEN&limit=10"
```

**Resposta**
```json
{
  "data": [
    {
      "id": "campaign_123",
      "name": "Summer Campaign 2026",
      "status": "ACTIVE",
      "created_time": "2026-01-01T00:00:00+0000"
    }
  ],
  "paging": {
    "cursors": {
      "before": "...",
      "after": "..."
    }
  }
}
```

---

### 3. Get Campaign Insights

**Endpoint**
```
GET /v18.0/{CAMPAIGN_ID}/insights
```

**Query Parameters**
```
access_token: string (obrigatório)
fields: string - métricas desejadas
time_range: object - período de tempo
date_preset: string - preset de período (THIS_MONTH, LAST_30_DAYS, etc)
```

**Fields Disponíveis**
```
spend              - Gasto total
impressions        - Número de impressões
clicks             - Número de cliques
reach              - Pessoas únicas alcançadas
frequency           - Frequência média
ctr                - Taxa de clique
cpc                - Custo por clique
cpm                - Custo por mil
actions            - Ações tomadas
action_type        - Tipo de ação
conversion_rate    - Taxa de conversão
roas               - Retorno sobre ad spend
```

**Exemplo**
```bash
curl -X GET "https://graph.instagram.com/v18.0/CAMPAIGN_ID/insights?fields=spend,impressions,clicks,reach&date_preset=LAST_30_DAYS&access_token=TOKEN"
```

**Resposta**
```json
{
  "data": [
    {
      "spend": "1500.00",
      "impressions": "50000",
      "clicks": "2500",
      "reach": "35000",
      "date_start": "2026-04-01",
      "date_stop": "2026-05-03"
    }
  ]
}
```

---

### 4. Get Adset Insights

**Endpoint**
```
GET /v18.0/{ADSET_ID}/insights
```

**Query Parameters**
```
access_token: string
fields: string
date_preset: string
```

**Exemplo**
```bash
curl -X GET "https://graph.instagram.com/v18.0/ADSET_ID/insights?fields=spend,impressions,clicks&access_token=TOKEN"
```

---

### 5. Get Ad Creative

**Endpoint**
```
GET /v18.0/{AD_ID}/adcreatives
```

**Resposta**
```json
{
  "data": [
    {
      "id": "creative_123",
      "name": "Creative Name",
      "image_url": "https://...",
      "video_url": "https://...",
      "title": "Ad Title",
      "body": "Ad Body Text"
    }
  ]
}
```

---

## 📈 Filtros e Ordenação

### Date Presets
```
TODAY, YESTERDAY, THIS_WEEK, LAST_WEEK, THIS_MONTH, LAST_MONTH, LAST_3_MONTHS, LAST_90_DAYS, LIFETIME
```

### Time Range (Custom)
```json
{
  "since": "2026-01-01",
  "until": "2026-05-03"
}
```

---

## ⚠️ Erros Comuns

| Código | Erro | Solução |
|--------|------|---------|
| 400 | `Invalid OAuth Token` | Token expirou, gere um novo |
| 403 | `Insufficient permissions` | Faltam permissões no token |
| 404 | `Ad Account not found` | Business ID incorreto |
| 429 | `Rate limit exceeded` | Aguarde antes de tentar |
| 500 | `Server error` | Tente novamente mais tarde |

## 🔗 Referências

- [Meta Docs Oficial](https://developers.facebook.com/docs/marketing-api/)
- [[setup/meta-setup|Meta Setup Guide]]
- [[architecture/data-flow|Data Flow]]
- [[_index|Voltar ao índice]]
