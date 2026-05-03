# Troubleshooting Guide

Soluções para problemas comuns no sistema.

## 🔴 Meta API Errors

### ❌ "Invalid OAuth Token"
**Causa**: Token expirou ou está inválido  
**Solução**:
1. Ir para [[../setup/meta-setup|Meta Setup]]
2. Gerar novo token
3. Atualizar `.claude/settings.local.json`
4. Testar com curl

### ❌ "Insufficient permissions"
**Causa**: Token não tem permissões necessárias  
**Solução**:
1. Adicionar permissões: `ads_read`, `ads_management`, `instagram_basic`
2. Regenerar token com novas permissões
3. Testar novamente

### ❌ "Business account not found"
**Causa**: Business Account ID incorreto  
**Solução**:
1. Ir para [Business Manager](https://business.facebook.com/)
2. Copiar Business Account ID correto
3. Atualizar configuração

### ❌ "Rate limit exceeded"
**Causa**: Muitas requisições em pouco tempo  
**Solução**:
1. Aguardar 1 minuto
2. Implementar backoff exponencial
3. Reduzir frequência de requisições

---

## 🟠 GHL API Errors

### ❌ "Unauthorized"
**Causa**: API Key inválida ou expirada  
**Solução**:
1. Ir para [[../setup/ghl-setup|GHL Setup]]
2. Regenerar API Key
3. Atualizar `.claude/settings.local.json`

### ❌ "Contact not found"
**Causa**: Contact ID não existe  
**Solução**:
1. Verificar se contact foi criado
2. Listar contatos: `GET /contacts`
3. Usar contact ID correto

### ❌ "Email failed to schedule"
**Causa**: Email body vazio ou formato inválido  
**Solução**:
1. Verificar HTML da newsletter
2. Validar campos obrigatórios
3. Testar HTML em browser

---

## 🟠 Slack Errors

### ❌ "Channel not found"
**Causa**: Channel ID inválido  
**Solução**:
1. Obter Channel ID correto (formato: C1234567)
2. Adicionar bot ao canal
3. Atualizar configuração

### ❌ "Bot not in channel"
**Causa**: Bot não foi adicionado ao canal  
**Solução**:
1. No Slack, abrir o canal
2. Clicar em "Add apps"
3. Selecionar seu bot
4. Confirmar

### ❌ "Invalid token"
**Causa**: Bot Token expirou  
**Solução**:
1. Regenerar token no Slack
2. Atualizar configuração
3. Testar com `/test`

---

## 🔵 Newsletter Generation Errors

### ❌ "No campaigns found"
**Causa**: Nenhuma campanha retornou do Meta  
**Solução**:
1. Verificar se existem campanhas no Meta
2. Verificar date range
3. Verificar permissões do token

### ❌ "No items meet performance threshold"
**Causa**: Nenhuma campanha passou no filtro  
**Solução**:
1. Reduzir performance threshold
2. Verificar performance das campanhas
3. Aumentar date range

### ❌ "Template not found"
**Causa**: Template HTML não existe  
**Solução**:
1. Verificar pasta `src/newsletter/templates/`
2. Usar template padrão
3. Criar novo template se necessário

---

## 💥 General Errors

### ❌ "Connection timeout"
**Causa**: Problema de rede ou servidor lento  
**Solução**:
1. Verificar internet
2. Aguardar e tentar novamente
3. Verificar status dos serviços (https://status.gohighlevel.com)

### ❌ "Invalid configuration"
**Causa**: Variáveis de ambiente não carregadas  
**Solução**:
1. Verificar arquivo `.claude/settings.local.json`
2. Verificar permissões do arquivo
3. Testar com `python -c "import os; print(os.getenv('META_ACCESS_TOKEN'))"`

### ❌ "JSON decode error"
**Causa**: Resposta de API não é JSON válido  
**Solução**:
1. Verificar resposta com curl
2. Verificar se o endpoint está correto
3. Verificar se o servidor está online

---

## 🛠️ Debug Mode

### Ativar logs detalhados

**No arquivo principal**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testar cada componente isoladamente

```bash
# Meta
python -c "from src.integrations.meta_ads import MetaAdsClient; print('OK')"

# GHL
python -c "from src.integrations.ghl import GHLClient; print('OK')"

# Slack
python -c "from src.integrations.slack_notifier import SlackNotifier; print('OK')"
```

### Executar com verbose

```bash
LOG_LEVEL=DEBUG python src/main.py
```

---

## 📞 Verificação de Status

### Meta
```bash
curl -X GET "https://graph.instagram.com/me?access_token=TOKEN"
```

### GHL
```bash
curl -X GET "https://api.gohighlevel.com/v1/calendars" \
  -H "Authorization: Bearer API_KEY"
```

### Slack
```bash
curl -X POST "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer BOT_TOKEN"
```

---

## 📚 Checklist de Troubleshooting

- [ ] Variáveis de ambiente carregadas?
- [ ] Tokens válidos e com permissões?
- [ ] Bots adicionados aos canais?
- [ ] Conexão com internet estável?
- [ ] Histórico de logs sem erros?
- [ ] Endpoints da API acessíveis?
- [ ] Rate limits respeitados?

---

## 🔗 Referências

- [[../setup/meta-setup|Meta Setup]]
- [[../setup/ghl-setup|GHL Setup]]
- [[../setup/slack-setup|Slack Setup]]
- [[../apis/meta-ads-api|Meta API Docs]]
- [[../apis/ghl-api|GHL API Docs]]
- [[_index|Voltar ao índice]]
