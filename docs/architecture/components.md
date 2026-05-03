# Components

Descrição detalhada de cada componente do sistema.

## 1️⃣ Meta Ads Integration

**Arquivo**: `src/integrations/meta_ads.py`

### Responsabilidades
- Autenticar com Meta API usando token
- Buscar lista de campanhas
- Extrair insights de performance
- Filtrar dados por performance
- Retornar dados estruturados

### Interface

```python
class MetaAdsClient:
    def __init__(self, access_token: str, business_account_id: str)
    def get_campaigns(self) -> List[Campaign]
    def get_campaign_insights(self, campaign_id: str) -> CampaignInsights
    def get_all_insights(self) -> List[CampaignInsights]
    def filter_by_performance(self, insights: List, threshold: float)
```

### Dependências
- `requests` library
- Meta API v18.0+

### Errors Tratados
- `Invalid OAuth Token`
- `Insufficient permissions`
- `Rate limit exceeded`
- `Business account not found`

---

## 2️⃣ Newsletter Generator

**Arquivo**: `src/newsletter/generator.py`

### Responsabilidades
- Processar dados do Meta
- Ranquear conteúdo por performance
- Gerar HTML formatado
- Criar email profissional

### Interface

```python
class NewsletterGenerator:
    def __init__(self, template_name: str = "default")
    def process_insights(self, insights: List[dict]) -> List[NewsletterItem]
    def rank_items(self, items: List[dict]) -> List[dict]
    def generate_html(self, items: List[dict]) -> str
    def get_email_body(self, items: List[dict]) -> dict
```

### Templates

**Location**: `src/newsletter/templates/`

- `base.html` - Template base
- `section.html` - Seção de item
- `footer.html` - Rodapé

### Dependências
- `jinja2` template engine
- CSS styles

### Outputs
- HTML formatado
- Plain text (fallback)

---

## 3️⃣ GHL Integration

**Arquivo**: `src/integrations/ghl.py`

### Responsabilidades
- Autenticar com GHL API
- Listar/criar contatos
- Agendar emails
- Verificar status

### Interface

```python
class GHLClient:
    def __init__(self, api_key: str, business_id: str)
    def get_contacts(self, limit: int = 50) -> List[Contact]
    def create_contact(self, email: str, name: str) -> Contact
    def schedule_email(self, contact_id: str, email_data: dict) -> str
    def get_campaign_status(self, campaign_id: str) -> dict
```

### Dependências
- `requests` library
- GHL API

### Error Handling
- `Unauthorized` - Invalid API key
- `Not Found` - Contact/campaign not found
- `Rate Limit` - Too many requests

---

## 4️⃣ Slack Notifier

**Arquivo**: `src/integrations/slack_notifier.py`

### Responsabilidades
- Enviar notificações ao Slack
- Usar Slack MCP tools
- Registrar eventos

### Interface

```python
class SlackNotifier:
    def __init__(self, channel_id: str)
    def notify_success(self, message: str, details: dict)
    def notify_error(self, error: str, details: dict)
    def notify_scheduled(self, email_id: str, scheduled_at: str)
```

### Message Types

1. **Success** - Newsletter criada e agendada
2. **Error** - Falha em algum passo
3. **Info** - Informações de status
4. **Debug** - Logs detalhados

### Features
- Block Kit formatting
- Error tracking
- Timestamp logging

---

## 5️⃣ Main Orchestrator

**Arquivo**: `src/main.py`

### Responsabilidades
- Coordenar fluxo completo
- Trata erros
- Registra logs
- Executa retry logic

### Fluxo

```python
def main():
    1. Load environment
    2. Initialize clients
    3. Fetch insights
    4. Process data
    5. Generate newsletter
    6. Schedule email
    7. Notify Slack
    8. Log results
```

### Error Handling

```
Try:
  - Execute all steps
Except:
  - Log error
  - Notify Slack
  - Raise exception
Finally:
  - Close connections
  - Save logs
```

---

## 6️⃣ Utils Module

**Arquivo**: `src/utils.py`

### Functions

```python
def load_env() -> dict
def validate_tokens() -> bool
def format_number(value: float) -> str
def parse_date(date_str: str) -> datetime
def create_logger() -> Logger
def retry_request(func, max_retries: int = 3)
```

### Logging

- INFO - Normal operations
- WARNING - Potential issues
- ERROR - Failures
- DEBUG - Detailed info

---

## 📊 Dependencies Graph

```
main.py
├── MetaAdsClient
│   └── requests
├── NewsletterGenerator
│   ├── jinja2
│   └── templates
├── GHLClient
│   └── requests
├── SlackNotifier
│   └── slack_send_message (MCP)
└── utils
    ├── logging
    ├── os/dotenv
    └── datetime
```

---

## 🔗 Referências

- [[overview|Architecture Overview]]
- [[data-flow|Data Flow]]
- [[../guides/testing|Testing Guide]]
- [[_index|Voltar ao índice]]
