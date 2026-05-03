# Mapa Mental: Meta Ads → Newsletter → GHL → Slack

```
                          ┌─────────────────────────┐
                          │  AUTOMAÇÃO NEWSLETTER   │
                          │  (Meta → GHL → Slack)   │
                          └────────────┬────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
            ┌───────▼────────┐  ┌─────▼──────────┐  ┌───▼────────────┐
            │   META ADS     │  │   NEWSLETTER   │  │   INTEGRAÇÕES  │
            │   INSIGHTS     │  │   GENERATOR    │  │                │
            └───────┬────────┘  └────────┬──────┘  └───┬────────────┘
                    │                    │             │
        ┌───────────┼─────────┐  ┌──────┼──────────┐  │
        │           │         │  │      │          │  │
    ┌───▼───┐  ┌────▼────┐ ┌─▼──▼──┐ ┌─▼──┐  ┌──▼──▼──┐
    │Fetch  │  │Filter by│ │Process│ │GHL │  │ Slack  │
    │Campaigns│ │Perform. │ │Data   │ │API │  │Notifier│
    └───┬───┘  └────┬────┘ └─┬────┬─┘ └────┘  └────────┘
        │           │        │    │
        │      Min Score    Rank  Template
        │        0.7         Top5  (HTML)
        │                         │
        │      ┌──────────────────┘
        │      │
        │    ┌─▼──────────────────────┐
        │    │  NEWSLETTER OUTPUT     │
        │    │  (Email HTML + Meta)   │
        │    └────────────┬───────────┘
        │                 │
        │         ┌───────┴─────────┐
        │         │                 │
        │    ┌────▼────┐      ┌─────▼────┐
        │    │Schedule │      │  Notify  │
        │    │in GHL   │      │ in Slack │
        │    └────┬────┘      └────┬─────┘
        │         │                │
        │         └────────┬───────┘
        │                  │
        └──────────────────┼────────────────────────┐
                          │                        │
                   ┌──────▼──────┐          ┌──────▼──────┐
                   │  ESTRUTURA  │          │   CICLO DE  │
                   │  DO PROJETO │          │   CONTEÚDO  │
                   └─────────────┘          └─────────────┘
                          │                        │
              ┌───────────┼──────────────┐       ┌─┴─────┐
              │           │              │       │       │
          ┌───▼───┐  ┌────▼────┐  ┌─────▼──┐  ┌─▼──┐  ┌─▼──┐
          │Config │  │ Sources │  │  Docs  │  │Sem1│  │Sem2│
          │ Json  │  │(Python) │  │(Vault) │  │Edu │  │Edu │
          └───────┘  └─────────┘  └────────┘  └────┘  └────┘
```

## 🧠 Lógica do Sistema

### Input (Meta Ads)
```
Meta Ads API
    ↓
[Campaign 1] [Campaign 2] [Campaign 3]
    ↓           ↓           ↓
  ROAS: 3.5  ROAS: 2.8  ROAS: 1.2
  CTR: 5%    CTR: 3%    CTR: 1%
  Reach: 50k Reach: 30k Reach: 10k
```

### Processing (Newsletter Generator)
```
Raw Insights
    ↓
1. Filter (performance_score > 0.7)
2. Rank (by ROAS, CTR, Reach)
3. Select (Top 5)
4. Format (HTML + Templates)
    ↓
Newsletter HTML
```

### Output (GHL + Slack)
```
Newsletter HTML
    ↓
GHL: Schedule Email
Slack: Notify Success
    ↓
Email Scheduled ✅
Notification Sent ✅
```

## 📊 Fluxo de Dados Completo

```
START
  │
  ├─→ Load Environment (tokens, IDs)
  │
  ├─→ Initialize Clients
  │   ├─ MetaAdsClient
  │   ├─ GHLClient
  │   ├─ SlackNotifier
  │   └─ NewsletterGenerator
  │
  ├─→ FETCH PHASE
  │   └─→ Meta API: Get all campaigns
  │       └─→ For each: Get insights
  │           └─→ Store: Raw data
  │
  ├─→ PROCESS PHASE
  │   ├─→ Calculate scores (ROAS, CTR, Reach)
  │   ├─→ Filter (min_score ≥ 0.7)
  │   ├─→ Rank (by performance)
  │   └─→ Select (top 5)
  │
  ├─→ GENERATE PHASE
  │   ├─→ Load template (Jinja2)
  │   ├─→ Render HTML
  │   ├─→ Format email
  │   └─→ Create payload
  │
  ├─→ SCHEDULE PHASE
  │   ├─→ Get or create contact (GHL)
  │   ├─→ Schedule email
  │   └─→ Get email ID
  │
  ├─→ NOTIFY PHASE
  │   └─→ Send Slack message
  │       ├─ Success blocks
  │       ├─ Email ID
  │       └─ Timestamp
  │
  └─→ END ✅
```

## 🔄 Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│         USER INTERFACE              │
│   (CLI: python src/main.py)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    ORCHESTRATOR LAYER               │
│  (src/main.py - Main)               │
│  - Coordena fluxo                   │
│  - Trata erros                      │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼──────┐ ┌─▼──────────┐
│ FETCH  │ │PROCESS  │ │  GENERATE  │
│ LAYER  │ │ LAYER   │ │  LAYER     │
├────────┤ ├─────────┤ ├────────────┤
│Meta    │ │Filter   │ │Templates   │
│GHL     │ │Rank     │ │Render      │
│Slack   │ │Validate │ │Format      │
└───┬────┘ └────┬────┘ └─┬──────────┘
    │           │        │
    └───────────┼────────┘
                │
┌───────────────▼──────────────────────┐
│   INTEGRATION LAYER                 │
│  (src/integrations/)                │
│  - MetaAdsClient                    │
│  - GHLClient                        │
│  - SlackNotifier                    │
└───────────────┬──────────────────────┘
                │
┌───────────────▼──────────────────────┐
│   EXTERNAL APIS                     │
│  - Meta Graph API                   │
│  - GHL REST API                     │
│  - Slack Web API                    │
└────────────────────────────────────────┘
```

## 🎯 Padrões de Fluxo

### Happy Path (Tudo bem)
```
Fetch ✅ → Process ✅ → Generate ✅ → Schedule ✅ → Notify ✅
                                                        │
                                                   SUCESSO 🎉
```

### Error Path (Algo correu mal)
```
Fetch ❌ → Log Error → Notify Error → Exit
         (ou)
Process ❌ → Log Error → Notify Error → Exit
         (ou)
Schedule ❌ → Log Error → Notify Error → Exit
```

## 📚 Conexões da Knowledge Base

```
                    ┌─────────────┐
                    │ _index.md   │ (HOME)
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼────┐  ┌──────────▼──────┐  ┌──────▼──┐
    │ SETUP  │  │ ARCHITECTURE    │  │GUIDES   │
    ├────────┤  ├─────────────────┤  ├─────────┤
    │Meta    │  │Overview         │  │Testing  │
    │GHL     │  │Data Flow        │  │Deploy   │
    │Slack   │  │Components       │  │News.    │
    │Env.    │  │                 │  │Perform. │
    └───┬────┘  └────────┬────────┘  └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                  ┌──────▼──────┐
                  │   APIS      │
                  ├─────────────┤
                  │Meta         │
                  │GHL          │
                  │Slack        │
                  └─────────────┘
```

---

**Dica**: Usa o Graph View do Obsidian (Cmd+Shift+G) para ver isto de forma ainda mais interativa e dinâmica! 🧠✨
