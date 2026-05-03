# Architecture Overview

Visão geral da arquitetura e fluxo do sistema.

## 🎯 Objetivo

Automatizar a criação de newsletters baseado em insights de performance de ads do Meta, agendando no GoHighLevel e notificando via Slack.

## 📊 Fluxo de Dados

```
┌─────────────────┐
│  Meta Ads API   │  (Lê insights de campaigns)
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Newsletter Generator │  (Processa e filtra dados)
└────────┬────────────┘
         │
         ▼
┌──────────────────┐
│  Newsletter HTML  │  (Template formatado)
└────────┬─────────┘
         │
         ▼
┌────────────────┐
│   GHL API      │  (Agenda envio)
└────────┬───────┘
         │
         ▼
┌──────────────────┐
│  Slack Message   │  (Notifica conclusão)
└──────────────────┘
```

## 🏗️ Componentes

### 1. **Meta Ads Integration** (`src/integrations/meta_ads.py`)
- Conecta à Meta Ads API
- Autentica com token
- Lê insights de campaigns
- Filtra por performance
- Retorna dados estruturados

### 2. **Newsletter Generator** (`src/newsletter/generator.py`)
- Recebe dados do Meta
- Processa e ranqueia conteúdo
- Gera HTML formatado
- Cria email profissional

### 3. **GHL Integration** (`src/integrations/ghl.py`)
- Conecta à GHL API
- Cria ou obtém contatos
- Agenda email para envio
- Verifica status

### 4. **Slack Notifier** (`src/integrations/slack_notifier.py`)
- Envia notificações ao Slack
- Usa Slack MCP tools
- Registra eventos

### 5. **Main Orchestrator** (`src/main.py`)
- Coordena todo o fluxo
- Trata erros
- Registra logs
- Executa configuração

## 📁 Estrutura de Pastas

```
src/
├── integrations/
│   ├── meta_ads.py       # Meta API Client
│   ├── ghl.py            # GHL API Client
│   └── slack_notifier.py # Slack Notifier
├── newsletter/
│   ├── generator.py      # Newsletter Logic
│   ├── templates.py      # Email Templates
│   └── styles.css        # Email Styles
├── main.py              # Orchestrator
└── utils.py             # Utilitários

docs/                   # Obsidian Vault
├── setup/              # Guias de setup
├── apis/               # Documentação de APIs
├── architecture/       # Arquitetura
├── guides/             # Tutoriais
└── reference/          # Referências
```

## 🔄 Fluxo de Execução

1. **Load Environment** - Carrega variáveis de ambiente
2. **Authenticate** - Autentica em todas as APIs
3. **Fetch Data** - Busca insights do Meta
4. **Process Data** - Processa e filtra
5. **Generate Newsletter** - Cria email HTML
6. **Schedule Email** - Agenda no GHL
7. **Notify** - Notifica no Slack
8. **Log** - Registra sucesso/erro

## 🔐 Fluxo de Autenticação

```
┌──────────────────────┐
│ settings.local.json  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Load Environment    │
└──────────┬───────────┘
           │
      ┌────┴────┬─────────┬──────────┐
      │          │         │          │
      ▼          ▼         ▼          ▼
   Meta       GHL      Slack       Email
   Auth       Auth      Auth        Config
```

## 📊 Data Models

### Meta Insights
```python
{
  "campaign_id": "123",
  "campaign_name": "Summer 2026",
  "spend": 1500.00,
  "impressions": 50000,
  "clicks": 2500,
  "reach": 35000,
  "ctr": 5.0,
  "cpc": 0.60,
  "conversions": 250,
  "roas": 3.5
}
```

### Newsletter Item
```python
{
  "title": "Best Performing Content",
  "metric": 3.5,  # ROAS
  "description": "Lorem ipsum",
  "performance": "excellent",
  "date": "2026-05-03"
}
```

### Email Payload (GHL)
```python
{
  "contactId": "contact_123",
  "subject": "Newsletter - May 2026",
  "body": "<html>...</html>",
  "scheduledAt": "2026-05-10T10:00:00Z"
}
```

## ✅ Validações

- ✓ Token Meta válido e com permissões
- ✓ Conexão GHL funcional
- ✓ Bot Slack no canal correto
- ✓ Dados de campaign existem
- ✓ Email body não vazio

## 🔗 Referências

- [[data-flow|Data Flow Detalhado]]
- [[components|Componentes Detalhados]]
- [[../guides/testing|Testing Guide]]
- [[_index|Voltar ao índice]]
