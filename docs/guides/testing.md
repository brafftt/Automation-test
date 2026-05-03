# Testing Guide

Como testar cada componente do sistema.

## 🧪 Teste de Configuração

### 1. Verificar Variáveis de Ambiente

```bash
python -c "
import json
with open('.claude/settings.local.json') as f:
    config = json.load(f)
    print('Configuração carregada:')
    for key in config.get('env', {}).keys():
        print(f'  ✓ {key}')
"
```

### 2. Testar Imports

```bash
python -c "
from src.integrations.meta_ads import MetaAdsClient
from src.integrations.ghl import GHLClient
from src.integrations.slack_notifier import SlackNotifier
from src.newsletter.generator import NewsletterGenerator
print('✓ Todos os imports OK')
"
```

---

## 🔌 Testes de Integração

### Meta API

```python
# test_meta.py
from src.integrations.meta_ads import MetaAdsClient
import os

token = os.getenv('META_ACCESS_TOKEN')
business_id = os.getenv('META_BUSINESS_ACCOUNT_ID')

client = MetaAdsClient(token, business_id)

# Teste 1: Listar campanhas
campaigns = client.get_campaigns()
print(f"✓ Encontradas {len(campaigns)} campanhas")

# Teste 2: Obter insights
for campaign in campaigns[:1]:
    insights = client.get_campaign_insights(campaign['id'])
    print(f"✓ Insights para {campaign['name']}: {insights}")
```

**Executar:**
```bash
python test_meta.py
```

### GHL API

```python
# test_ghl.py
from src.integrations.ghl import GHLClient
import os

api_key = os.getenv('GHL_API_KEY')
business_id = os.getenv('GHL_BUSINESS_ID')

client = GHLClient(api_key, business_id)

# Teste 1: Listar contatos
contacts = client.get_contacts()
print(f"✓ Encontrados {len(contacts)} contatos")

# Teste 2: Criar contato de teste
test_contact = client.create_contact(
    email="test@example.com",
    name="Test User"
)
print(f"✓ Contato criado: {test_contact['id']}")
```

**Executar:**
```bash
python test_ghl.py
```

### Slack API

```python
# test_slack.py
from src.integrations.slack_notifier import SlackNotifier
import os

channel_id = os.getenv('SLACK_CHANNEL_ID')
notifier = SlackNotifier(channel_id)

# Teste 1: Enviar mensagem
notifier.notify_success(
    "Teste de Notificação",
    {"status": "test", "timestamp": "2026-05-03"}
)
print("✓ Mensagem enviada ao Slack")
```

**Executar:**
```bash
python test_slack.py
```

---

## 📝 Teste da Newsletter

```python
# test_newsletter.py
from src.newsletter.generator import NewsletterGenerator

# Dados de teste
test_data = [
    {
        "campaign_name": "Summer Campaign",
        "spend": 1500.0,
        "impressions": 50000,
        "clicks": 2500,
        "conversions": 250,
        "roas": 3.5
    },
    {
        "campaign_name": "Spring Sale",
        "spend": 1000.0,
        "impressions": 40000,
        "clicks": 2000,
        "conversions": 200,
        "roas": 3.0
    }
]

generator = NewsletterGenerator()

# Teste 1: Processar dados
processed = generator.process_insights(test_data)
print(f"✓ Processados {len(processed)} itens")

# Teste 2: Gerar HTML
html = generator.generate_html(processed)
print(f"✓ HTML gerado ({len(html)} caracteres)")

# Teste 3: Verificar saída
if "<html>" in html and "Campaign" in html:
    print("✓ HTML contém conteúdo esperado")
```

**Executar:**
```bash
python test_newsletter.py
```

---

## 🔄 Teste End-to-End

### Executar fluxo completo

```bash
LOG_LEVEL=DEBUG python src/main.py
```

### Verificar outputs

1. ✓ Meta: Campanhas carregadas
2. ✓ Newsletter: HTML gerado
3. ✓ GHL: Email agendado
4. ✓ Slack: Notificação enviada

---

## 📊 Teste de Performance

### Medir tempo de execução

```python
import time
from src.main import main

start = time.time()
main()
end = time.time()

print(f"Tempo total: {end - start:.2f}s")
```

### Targets

- Meta fetch: < 5s
- Newsletter generation: < 2s
- GHL schedule: < 3s
- Slack notify: < 2s
- **Total: < 15s**

---

## 🐛 Teste de Erro

### Simular erros

```python
# test_errors.py
from src.integrations.meta_ads import MetaAdsClient

# Teste com token inválido
try:
    client = MetaAdsClient("invalid_token", "123456")
    client.get_campaigns()
except Exception as e:
    print(f"✓ Erro capturado: {e}")

# Teste com business_id inválido
try:
    client = MetaAdsClient(os.getenv('META_ACCESS_TOKEN'), "invalid_id")
    client.get_campaigns()
except Exception as e:
    print(f"✓ Erro capturado: {e}")
```

---

## ✅ Checklist de Testes

- [ ] Variáveis de ambiente carregadas
- [ ] Meta API conecta
- [ ] Campanhas carregadas
- [ ] Insights extraídos
- [ ] Newsletter gerada
- [ ] GHL scheduled email
- [ ] Slack notificado
- [ ] Sem erros no console
- [ ] Logs criados
- [ ] Tempo de execução aceitável

---

## 🔗 Referências

- [[../architecture/overview|Architecture]]
- [[../guides/troubleshooting|Troubleshooting]]
- [[_index|Voltar ao índice]]
