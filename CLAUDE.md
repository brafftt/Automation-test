# Projeto

Este repositório contém **dois sistemas independentes**:

1. **Newsletter Automation** (em `src/`, `config/`, `scripts/newsletter*`) — pipeline Python: Meta Ads → newsletter → GHL → Slack. **Não tocar** ao trabalhar no copywriter.
2. **AI Copywriter** (em `.claude/`, `knowledge-base/`, `outputs/`, `scripts/sync_youtube.py`) — sistema multi-agente para produzir copy a partir de uma base de conhecimento. É este sistema que este ficheiro documenta.

# Como usar o copywriter

Abre o terminal na raiz do repo e corre:

```bash
claude
```

Dá um briefing em português. Exemplos:

- "Preciso de um email para a lista quente sobre o lançamento do produto X, com urgência de 48h."
- "Cria 5 variações de copy para Meta Ads sobre a oferta Y."
- "Escreve um artigo de 800 palavras sobre o tema Z para o blog."
- "Faz 3 posts para Instagram a partir da transcrição do vídeo W."

O agente principal identifica o tipo de copy, delega ao sub-agente adequado, orquestra pesquisa → escrita → auditoria de voz → edição, e escreve o resultado em `outputs/<tipo>/YYYY-MM-DD-<slug>.md`.

# Estrutura da knowledge base

| Pasta | Conteúdo |
|---|---|
| `knowledge-base/brand/voz-de-marca.md` | Voz de marca canónica (preencher antes de usar) |
| `knowledge-base/brand/personas.md` | Personas de público-alvo |
| `knowledge-base/brand/exemplos-aprovados/` | Copy passada aprovada — referência de estilo |
| `knowledge-base/produtos/` | Descrições de produtos e ofertas core |
| `knowledge-base/ofertas/` | Promoções, pricing, bónus |
| `knowledge-base/pesquisa/` | Market research, swipe files, referências |
| `knowledge-base/youtube/` | Transcrições auto-geradas (via `scripts/sync_youtube.py`) |
| `knowledge-base/pdfs/` | PDFs originais |
| `knowledge-base/docs-word/` | Documentos Word originais |
| `knowledge-base/vault-docs/` | Symlink para o Obsidian Vault em `docs/` |

MCPs conectados (ver `.mcp.json`) dão acesso adicional em tempo real a Notion, Google Drive e ao filesystem da KB/outputs.

# Sub-agentes disponíveis

Ver `.claude/agents/`:

- `pesquisador` — explora a KB + Notion + Drive e devolve síntese estruturada de factos, ângulos, quotes e exemplos.
- `copywriter` — generalista para emails, newsletters, long-form (artigos, scripts de vídeo).
- `copy-ads` — anúncios (Meta, Google) e landing pages.
- `copy-social` — posts para Instagram, LinkedIn, Twitter/X.
- `tom-de-voz` — auditoria do draft contra `voz-de-marca.md` e `exemplos-aprovados/`.
- `editor` — revisão final: clareza, gramática, ritmo, força do CTA.

# Voz de marca

Ficheiro canónico: `knowledge-base/brand/voz-de-marca.md`.

Antes de usar o copywriter, preenche esse ficheiro. Sem ele, os drafts saem genéricos.

# Convenções

- **Idioma**: sempre português (a menos que o briefing peça expressamente outro idioma).
- **Outputs**: `outputs/<tipo>/YYYY-MM-DD-<slug>.md` — nunca sobrescrever, criar novo ficheiro se já existir.
- **Citações**: cada draft deve terminar com uma secção `## Fontes` listando os ficheiros da KB consultados.
- **Nunca** escrever fora de `outputs/` ou de `knowledge-base/` (esta última só se o utilizador o pedir explicitamente).

# MCP servers

Definidos em `.mcp.json` na raiz. Tokens ficam em `.claude/settings.local.json` (gitignored).

- `notion` — leitura de páginas e bases de dados no Notion (requer `NOTION_TOKEN`).
- `gdrive` — leitura de ficheiros no Google Drive (requer credenciais em `~/.config/gdrive/credentials.json`).
- `filesystem` — acesso escoped a `knowledge-base/` e `outputs/`.

Verifica com `/mcp` dentro do Claude Code.

# Scripts

- `scripts/sync_youtube.py` — lê `scripts/youtube-sources.txt` e escreve transcrições em `knowledge-base/youtube/`.
  ```bash
  python scripts/sync_youtube.py            # sync incremental
  python scripts/sync_youtube.py --force    # re-download tudo
  python scripts/sync_youtube.py --url https://youtu.be/XXXX  # apenas 1 vídeo
  ```

# O que NÃO fazer

- Não tocar em `src/`, `scripts/newsletter*`, `config/` — pertencem ao pipeline newsletter, sistema separado.
- Não commitar `.claude/settings.local.json` (tokens) — já gitignored.
- Não escrever documentação ou meta-ficheiros a menos que o utilizador peça expressamente.
