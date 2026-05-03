# GoHighLevel (GHL) API Documentation

Referência dos endpoints da GHL API usados neste projeto.

## 🔐 Autenticação

Todos os requests requerem header:

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Base URL**
```
https://api.gohighlevel.com/v1
```

---

## 📊 Endpoints

### 1. List Campaigns

**Endpoint**
```
GET /campaigns
```

**Query Parameters**
```
limit: integer - Padrão: 20, Máximo: 100
offset: integer - Para paginação
```

**Exemplo**
```bash
curl -X GET "https://api.gohighlevel.com/v1/campaigns?limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Resposta**
```json
{
  "success": true,
  "data": [
    {
      "id": "campaign_123",
      "name": "Spring Campaign",
      "status": "active",
      "type": "email",
      "createdAt": "2026-01-01T00:00:00Z"
    }
  ],
  "pageInfo": {
    "total": 50,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 2. Get Campaign

**Endpoint**
```
GET /campaigns/{campaignId}
```

**Exemplo**
```bash
curl -X GET "https://api.gohighlevel.com/v1/campaigns/campaign_123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Resposta**
```json
{
  "success": true,
  "data": {
    "id": "campaign_123",
    "name": "Campaign Name",
    "status": "active",
    "emails": [
      {
        "id": "email_1",
        "subject": "Welcome Email",
        "body": "...",
        "scheduledAt": "2026-05-10T10:00:00Z"
      }
    ]
  }
}
```

---

### 3. Create Email Campaign

**Endpoint**
```
POST /emails
```

**Request Body**
```json
{
  "contactId": "contact_123",
  "subject": "Newsletter - May 2026",
  "body": "<html>...</html>",
  "scheduledAt": "2026-05-10T10:00:00Z",
  "fromName": "Your Name",
  "fromEmail": "your@email.com"
}
```

**Exemplo**
```bash
curl -X POST "https://api.gohighlevel.com/v1/emails" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contactId": "contact_123",
    "subject": "Newsletter",
    "body": "<h1>Hi</h1>",
    "scheduledAt": "2026-05-10T10:00:00Z"
  }'
```

**Resposta**
```json
{
  "success": true,
  "data": {
    "id": "email_123",
    "status": "scheduled",
    "scheduledAt": "2026-05-10T10:00:00Z"
  }
}
```

---

### 4. List Contacts

**Endpoint**
```
GET /contacts
```

**Query Parameters**
```
limit: integer
offset: integer
email: string - Filtrar por email
status: string - active, inactive, etc
```

**Exemplo**
```bash
curl -X GET "https://api.gohighlevel.com/v1/contacts?limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Resposta**
```json
{
  "success": true,
  "data": [
    {
      "id": "contact_123",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "status": "active"
    }
  ],
  "pageInfo": {
    "total": 500,
    "limit": 50,
    "offset": 0
  }
}
```

---

### 5. Create Contact

**Endpoint**
```
POST /contacts
```

**Request Body**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "tags": ["newsletter", "active"]
}
```

**Exemplo**
```bash
curl -X POST "https://api.gohighlevel.com/v1/contacts" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "email": "jane@example.com"
  }'
```

**Resposta**
```json
{
  "success": true,
  "data": {
    "id": "contact_456",
    "email": "jane@example.com"
  }
}
```

---

## 📋 Request/Response Patterns

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Error description"
  }
}
```

---

## ⚠️ Erros Comuns

| Código | Erro | Solução |
|--------|------|---------|
| 401 | `Unauthorized` | API Key inválida |
| 404 | `Not Found` | Resource não existe |
| 429 | `Too Many Requests` | Rate limit excedido |
| 400 | `Bad Request` | JSON inválido |

---

## 📌 Rate Limiting

- Limite: **100 requests** por minuto
- Headers de resposta:
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 95`
  - `X-RateLimit-Reset: 1234567890`

---

## 🔗 Referências

- [GHL API Oficial](https://gohighlevel.com/api)
- [[setup/ghl-setup|GHL Setup Guide]]
- [[_index|Voltar ao índice]]
