# Automation: Meta Ads → Newsletter → GHL → Slack

Sistema de automação que lê insights de ads do Meta, gera newsletters com conteúdo de melhor performance e agenda no GoHighLevel (GHL), com notificações no Slack.

## Fluxo

1. **Meta Ads API** → Lê insights de campaigns e conteúdo com melhor performance orgânica
2. **Newsletter Generator** → Processa dados e cria newsletter profissional
3. **GHL API** → Agenda newsletter para envio
4. **Slack** → Notifica quando tudo está pronto

## Setup

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais

Criar arquivo `.claude/settings.local.json`:

```json
{
  "env": {
    "META_ACCESS_TOKEN": "seu_token_aqui",
    "META_BUSINESS_ACCOUNT_ID": "seu_id_aqui",
    "GHL_API_KEY": "sua_chave_ghl",
    "GHL_BUSINESS_ID": "seu_business_id",
    "SLACK_CHANNEL_ID": "seu_channel_id"
  }
}
```

### 3. Gerar tokens

- **Meta Token**: [Meta Developers](https://developers.facebook.com/) → Veja `docs/setup/meta-setup.md`
- **GHL Token**: [GoHighLevel](https://gohighlevel.com/) → Veja `docs/setup/ghl-setup.md`
- **Slack Channel**: Veja `docs/setup/slack-setup.md`

## Estrutura

```
src/
├── integrations/      # Integrações com APIs
├── newsletter/        # Geração de newsletters
├── main.py           # Orquestrador principal
└── utils.py          # Utilitários

docs/                 # Obsidian Vault (Knowledge Base)
├── setup/            # Guias de configuração
├── apis/             # Documentação de APIs
├── architecture/     # Arquitetura e fluxos
├── guides/           # Guias e troubleshooting
└── reference/        # Referências e glossário
```

## Uso

```bash
python src/main.py
```

## Documentação

Consulte o **Obsidian Vault** em `docs/` para:
- Guias de setup detalhados
- Documentação de APIs
- Diagramas de fluxo de dados
- Troubleshooting

Comece em `docs/_index.md`.

## Dependências

- **requests** - HTTP client para chamadas à API
- **python-dotenv** - Carregar variáveis de ambiente
- **jinja2** - Templates para newsletters

## Licença

MIT
