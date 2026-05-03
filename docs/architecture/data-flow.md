# Data Flow

Fluxo detalhado de dados no sistema.

## 🔄 Processo Completo

### Passo 1: Autenticação
```
settings.local.json
        │
        ▼
Load Environment Variables
        │
    ┌───┴────┬─────────┬──────────┐
    │         │         │          │
    ▼         ▼         ▼          ▼
META_TOKEN GHL_KEY SLACK_TOKEN EMAIL_CONFIG
    │         │         │          │
    ▼         ▼         ▼          ▼
Meta        GHL      Slack      Templates
 Auth       Auth      Auth       Config
```

### Passo 2: Fetch Data
```
Meta Ads API
        │
        ▼
/campaigns (List)
        │
        ▼
For each Campaign:
  /insights (Get metrics)
        │
    ┌───┴────┬────────┬─────────┐
    │         │        │         │
    ▼         ▼        ▼         ▼
 spend  impressions clicks  conversions
 reach    ctr       cpc      roas
```

### Passo 3: Process Data
```
Raw Campaign Data
        │
        ▼
Filter by Performance
  (threshold > 0.7)
        │
        ▼
Calculate Metrics
        │
        ▼
Rank by Performance
        │
        ▼
Select Top 5 Items
```

### Passo 4: Generate Newsletter
```
Processed Data
        │
        ▼
Get Template
        │
        ▼
Render HTML
  (Jinja2)
        │
        ▼
Add Styles
        │
        ▼
Newsletter HTML
```

### Passo 5: Schedule Email
```
Newsletter HTML
        │
        ▼
Create/Get Contact (GHL)
        │
        ▼
Create Email Payload
        │
        ▼
Schedule via GHL API
        │
        ▼
Get Email ID
```

### Passo 6: Notify
```
Email ID + Status
        │
        ▼
Create Message Block
        │
        ▼
Send to Slack
        │
        ▼
Notification Sent
```

## 📊 Data Structures

### Meta Campaign Response
```json
{
  "id": "123456789",
  "name": "Campaign Name",
  "status": "ACTIVE",
  "insights": {
    "data": [
      {
        "spend": "1500.00",
        "impressions": "50000",
        "clicks": "2500",
        "actions": "250"
      }
    ]
  }
}
```

### Processed Item
```python
{
  "source": "meta",
  "campaign_id": "123456789",
  "campaign_name": "Campaign Name",
  "metrics": {
    "spend": 1500.0,
    "impressions": 50000,
    "clicks": 2500,
    "ctr": 5.0,
    "cpc": 0.60,
    "conversions": 250,
    "roas": 3.5
  },
  "performance_score": 0.85,
  "ranking": 1
}
```

### Newsletter Item
```json
{
  "title": "Campaign Name",
  "subtitle": "Summer Campaign 2026",
  "metrics": "3.5x ROAS, 5% CTR, $0.60 CPC",
  "summary": "Top performing campaign with excellent ROI",
  "performance_level": "excellent",
  "badges": ["high-roi", "high-reach"]
}
```

### GHL Email Payload
```json
{
  "contactId": "contact_123",
  "contactEmail": "user@example.com",
  "subject": "Weekly Newsletter - May 2026",
  "body": "<html>...</html>",
  "fromName": "Your Company",
  "fromEmail": "no-reply@company.com",
  "scheduledAt": "2026-05-10T10:00:00Z"
}
```

### Slack Notification
```json
{
  "channel": "C1234567890",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Newsletter Agendada com Sucesso!*\n5 campanhas incluídas\nEnvio em 2026-05-10"
      }
    }
  ]
}
```

## 🔄 Error Handling

```
API Call
    │
    ├─ Success (200)
    │   └─ Process Data
    │
    ├─ Client Error (4xx)
    │   └─ Log Error + Retry Logic
    │
    └─ Server Error (5xx)
        └─ Log Error + Slack Notification
```

## 📊 Performance Metrics

### Default Thresholds
```python
MIN_PERFORMANCE_SCORE = 0.7  # 70%
MAX_ITEMS = 5               # Top 5
TIME_WINDOW = "LAST_30_DAYS"
```

### Ranking Formula
```
performance_score = (
    (roas / max_roas) * 0.4 +
    (reach / max_reach) * 0.3 +
    (ctr / max_ctr) * 0.2 +
    (conversions / max_conversions) * 0.1
)
```

## 🔗 Referências

- [[overview|Architecture Overview]]
- [[components|Components]]
- [[../apis/meta-ads-api|Meta API Docs]]
- [[../apis/ghl-api|GHL API Docs]]
- [[_index|Voltar ao índice]]
