# Setup: GoHighLevel (GHL)

Guia para configurar integração com GoHighLevel API.

## 📋 Pré-requisitos

- Conta ativa no GoHighLevel
- Acesso a Settings/API Keys
- Business ID do GHL

## 🔑 Gerando API Key

### 1. Acessar GHL Dashboard

1. Ir para [GoHighLevel](https://app.gohighlevel.com)
2. Fazer login com sua conta
3. Clicar em seu perfil (canto superior direito)
4. Selecionar **Settings**

### 2. Gerar API Key

1. Na aba **Settings**, procurar por **API & Integrations**
2. Clicar em **API Keys**
3. Clicar em **Generate New API Key**
4. Dar um nome descritivo: "Meta Ads Newsletter"
5. Selecionar permissões:
   ```
   campaigns:read
   campaigns:write
   contacts:read
   contacts:write
   emails:read
   emails:write
   ```
6. Clicar em **Generate**
7. **Copiar e guardar** a chave (só aparece uma vez!)

### 3. Obter Business ID

1. Na aba **Settings**, procurar por **Business Info**
2. Copiar o **Business ID** (formato: xxxxx)
3. Também anota o **Location ID** se houver

## 🔐 Salvando Credenciais

Adicionar ao `.claude/settings.local.json`:

```json
{
  "env": {
    "GHL_API_KEY": "sua_api_key_aqui",
    "GHL_BUSINESS_ID": "seu_business_id_aqui"
  }
}
```

## 🧪 Testando

### Verificar Conexão

```bash
curl -X GET "https://api.gohighlevel.com/v1/calendars" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Resposta esperada:
```json
{
  "calendars": []
}
```

### Listar Contatos

```bash
curl -X GET "https://api.gohighlevel.com/v1/contacts" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📚 Endpoints Principais

- `POST /campaigns` - Criar campanha
- `GET /campaigns` - Listar campanhas
- `POST /contacts` - Criar contato
- `POST /emails` - Agendar email

Consulte [[apis/ghl-api|GHL API Documentation]] para detalhes.

## ⚠️ Troubleshooting

| Erro | Solução |
|------|---------|
| `Invalid API Key` | Verifique se copiou corretamente |
| `Unauthorized` | Regenere a API Key |
| `Not Found` | Verifique Business ID |
| `Rate Limit` | Aguarde antes de tentar novamente |

## 📚 Referências

- [[apis/ghl-api|GHL API Documentation]]
- [GoHighLevel Official](https://gohighlevel.com/)
- [[_index|Voltar ao índice]]
