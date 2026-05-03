# Deployment Guide

Como fazer deploy do sistema em produção.

## 🚀 Pre-Deployment Checklist

- [ ] Testes end-to-end passando
- [ ] Logs limpos (sem warnings)
- [ ] Performance aceitável (< 15s)
- [ ] Todos os tokens gerados
- [ ] Configuração testada
- [ ] Documentação atualizada
- [ ] Error handling implementado

---

## 📦 Preparação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Credenciais

```bash
# Copiar template
cp config/.env.example config/.env

# Editar com valores reais
# - META_ACCESS_TOKEN
# - GHL_API_KEY
# - SLACK_BOT_TOKEN
```

### 3. Validar Configuração

```bash
python -c "
import os
import json
with open('.claude/settings.local.json') as f:
    config = json.load(f)
    required = ['META_ACCESS_TOKEN', 'GHL_API_KEY', 'SLACK_BOT_TOKEN']
    for key in required:
        if key not in config.get('env', {}):
            print(f'❌ Missing: {key}')
        else:
            print(f'✓ {key}')
"
```

---

## 🐳 Deployment Options

### Opção 1: Local (Desenvolvimento)

```bash
# Executar manualmente
python src/main.py

# Executar com logs
LOG_LEVEL=INFO python src/main.py

# Executar em background
nohup python src/main.py > logs/main.log 2>&1 &
```

### Opção 2: Scheduled (Cron)

```bash
# Editar crontab
crontab -e

# Agendar diariamente às 8h da manhã
0 8 * * * cd /path/to/project && python src/main.py >> logs/daily.log 2>&1

# Agendar semanalmente (segunda-feira às 9h)
0 9 * * 1 cd /path/to/project && python src/main.py >> logs/weekly.log 2>&1
```

### Opção 3: Docker

**Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

**Build e Run**
```bash
# Build
docker build -t meta-newsletter .

# Run
docker run \
  -e META_ACCESS_TOKEN=your_token \
  -e GHL_API_KEY=your_key \
  -e SLACK_BOT_TOKEN=your_token \
  meta-newsletter
```

### Opção 4: Cloud (AWS Lambda)

**handler.py**
```python
from src.main import main

def lambda_handler(event, context):
    try:
        main()
        return {
            'statusCode': 200,
            'body': 'Success'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
```

**Deploy**
```bash
# Zip files
zip -r function.zip src/ config/ requirements.txt

# Deploy to AWS
aws lambda create-function \
    --function-name meta-newsletter \
    --runtime python3.10 \
    --zip-file fileb://function.zip \
    --handler handler.lambda_handler
```

---

## 📊 Monitoring

### Logs

```bash
# Ver logs em tempo real
tail -f logs/main.log

# Ver erros
grep ERROR logs/main.log

# Contar execuções
wc -l logs/main.log
```

### Health Check

```bash
# Testar se sistema está funcional
python -c "
from src.integrations.meta_ads import MetaAdsClient
from src.integrations.ghl import GHLClient
from src.integrations.slack_notifier import SlackNotifier

print('✓ System healthy')
"
```

### Alertas (Slack)

Adicionar notificação de erro em Slack:

```python
try:
    main()
except Exception as e:
    notifier.notify_error(
        f"Production Error: {str(e)}",
        {"timestamp": datetime.now().isoformat()}
    )
```

---

## 🔄 Atualizações

### Atualizar código

```bash
# Pulle latest changes
git pull origin main

# Reinstale dependências se mudou
pip install -r requirements.txt

# Teste antes de produção
python test_newsletter.py
```

### Atualizar tokens

```bash
# Se token expirou:
1. Gerar novo token em [[../setup/meta-setup|Meta Setup]]
2. Atualizar .claude/settings.local.json
3. Testar com curl
4. Reiniciar aplicação
```

---

## 📈 Escalabilidade

### Aumentar frequência

**De diário para hora:**
```bash
# Cron a cada hora
0 * * * * cd /path && python src/main.py >> logs/main.log 2>&1
```

### Aumentar volume

**Processar múltiplas contas:**
```python
# Modificar main.py
for account_id in ACCOUNT_IDS:
    process_account(account_id)
```

### Adicionar fila (bullmq)

```python
# Para processar em background
from queue import Queue
q = Queue()
q.put({"account_id": "123"})
```

---

## 🔒 Segurança

### Checklist

- [ ] `.claude/settings.local.json` em `.gitignore`
- [ ] Tokens não em código
- [ ] Usar HTTPS para APIs
- [ ] Validar inputs
- [ ] Sanitizar logs (não exibir tokens)
- [ ] Atualizar dependências regularmente

### Sanitizar logs

```python
# Em utils.py
def sanitize_log(message: str) -> str:
    # Remove tokens
    message = message.replace(META_TOKEN, "***")
    message = message.replace(GHL_KEY, "***")
    return message
```

---

## 🆘 Rollback

Se algo der errado:

```bash
# Ver versão anterior
git log --oneline

# Reverter última versão
git revert HEAD

# Ou voltar para versão específica
git checkout <commit_id>
```

---

## 📚 Referências

- [[../guides/testing|Testing Guide]]
- [[../guides/troubleshooting|Troubleshooting]]
- [[../setup/environment|Environment Setup]]
- [[_index|Voltar ao índice]]
