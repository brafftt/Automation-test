# Setup: Meta API (Instagram)

Guia passo a passo para configurar a Meta API e gerar Access Token.

## 📋 Pré-requisitos

- Conta Meta/Facebook
- Página de Facebook ou conta de negócios
- Acesso ao Meta Developers

## 🔑 Gerando Access Token

### 1. Criar App no Meta Developers

1. Ir para [Meta Developers](https://developers.facebook.com/)
2. Clicar em "My Apps" → "Create App"
3. Selecionar tipo: **Business**
4. Preencher detalhes:
   - App Name: "Meta Ads Automation"
   - App Purpose: "Business"
5. Clicar em "Create App"

### 2. Configurar Produto (Ads Manager)

1. Na dashboard do app, clicar em "Add Product"
2. Buscar por **"Ads Manager"** ou **"Marketing API"**
3. Clicar em "Set Up"

### 3. Gerar Token

1. Ir para Settings → Basic
2. Copiar: **App ID** e **App Secret**
3. Ir para Tools → Access Token Debugger
4. Gerar novo token:
   - Acesso: **App Token**
   - Clicar em "Generate"

5. Selecionar permissões necessárias:
   ```
   ads_read
   ads_management
   instagram_basic
   instagram_graph_api
   pages_read_user_content
   ```

### 4. Obter Business Account ID

1. Ir para [Business Manager](https://business.facebook.com/)
2. Ir para Settings → Business Data
3. Copiar o **Business Account ID**

## 🔐 Salvando Credenciais

Adicionar ao `.claude/settings.local.json`:

```json
{
  "env": {
    "META_ACCESS_TOKEN": "seu_token_gerado_aqui",
    "META_BUSINESS_ACCOUNT_ID": "seu_business_id_aqui"
  }
}
```

## 🧪 Testando

### Verificar Token

```bash
curl -X GET "https://graph.instagram.com/me?access_token=YOUR_TOKEN"
```

Resposta esperada:
```json
{
  "id": "123456789",
  "name": "Your Name"
}
```

### Listar Campaigns

```bash
curl -X GET "https://graph.instagram.com/v18.0/YOUR_BUSINESS_ID/campaigns?access_token=YOUR_TOKEN"
```

## ⚠️ Troubleshooting

| Erro | Solução |
|------|---------|
| `Invalid OAuth Token` | Token expirou. Gere um novo |
| `Insufficient permissions` | Adicione as permissões no setup |
| `Business account not found` | Verifique o Business Account ID |
| `Rate limit exceeded` | Aguarde alguns minutos antes de tentar novamente |

## 📚 Referências

- [[apis/meta-ads-api|Documentação Meta Ads API]]
- [Meta Developers Official](https://developers.facebook.com/)
- [Ads Manager Documentation](https://developers.facebook.com/docs/marketing-api/)
- [[_index|Voltar ao índice]]
