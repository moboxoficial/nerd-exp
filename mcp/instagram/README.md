# Conector MCP do Instagram — Nerd Experience / NerdVerso

Servidor MCP que liga o Claude às contas **@nerdexperience** e **@nerdverso.nxp** pela API oficial do Instagram
(Instagram API with Instagram Login). Com ele, a operação de social media pode publicar, agendar, cuidar
da comunidade e puxar métricas conversando com o Claude.

## O que ele faz

| Área | Ferramentas |
|---|---|
| Publicação | `publicar_imagem`, `publicar_carrossel`, `publicar_reels`, `publicar_story` — na hora ou com `agendar_para` |
| Agendamento | `listar_agendamentos`, `ver_agendamento`, `reagendar`, `cancelar_agendamento` |
| Mídia | `verificar_midia` — valida o arquivo e devolve prévia com o corte (4:5, 1:1, 1.91:1, 9:16) |
| Comunidade | `comentarios_recentes`, `responder_comentario`, `ocultar_comentario`, `apagar_comentario` |
| DMs | `listar_conversas`, `ler_conversa`, `enviar_dm` |
| Números | `listar_posts`, `metricas_post`, `metricas_conta`, `limite_publicacao` |
| Contas | `listar_contas`, `renovar_tokens` |

Detalhes que já vêm resolvidos:

- **Mídia do Drive ou do Canva:** basta passar o link do Drive, o `drive_file_id` ou a URL de export do Canva.
  O servidor baixa, converte PNG para JPEG (a API só aceita JPEG), aplica o corte e entrega para a Meta.
  Arquivos do Drive precisam estar compartilhados como **"Qualquer pessoa com o link"**.
- **Agendamento de verdade:** a API do Instagram não agenda, só publica. O servidor guarda a fila e publica no
  horário. Vídeos começam a subir 20 minutos antes para a Meta processar. Se o servidor ficar fora do ar e
  perder o horário por mais de 2h, o post **não** sai atrasado: fica com erro para ser reagendado.
- **Horários em Brasília:** `2026-10-14T11:00` é 11h de Brasília.
- **Tokens:** são renovados sozinhos (valem 60 dias).
- **Validações antes de agendar:** legenda até 2.200 caracteres e 30 hashtags, proporção do feed, arquivo acessível.
- **ID da planilha:** cada post pode levar o `id_planilha` (ex: `2026-10-14_NXP_11h`) para cruzar com o calendário.

## O que a API do Instagram não faz

Isso continua sendo feito no app:

- Figurinhas nos stories (link, enquete, caixinha, música, menção)
- Música da biblioteca do Instagram nos reels
- Marcar pessoas e produtos, adicionar localização
- Editar bio, link da bio e destaques
- Aceitar convite de collab (o convite sai pela API, o aceite é da outra conta)

Outros limites da Meta: no máximo 25 posts por conta a cada 24h via API; resposta de DM só até 24h depois da
última mensagem da pessoa (7 dias com `agente_humano`).

---

## Instalação

### 1. Contas profissionais

As duas contas precisam ser **profissionais** (Empresa ou Criador de conteúdo). Não precisa de Página do Facebook.

### 2. App na Meta e tokens

1. Em [developers.facebook.com](https://developers.facebook.com/apps), crie um app do tipo **Empresa** com o caso
   de uso **"Gerenciar mensagens e conteúdo no Instagram"**.
2. Em **API do Instagram → Configuração da API com login do Instagram**:
   - Em **Gerar tokens de acesso**, adicione `@nerdexperience` e `@nerdverso.nxp` (cada conta aceita o convite em
     Configurações → Apps e sites → Convites de testador, no Instagram).
   - Clique em **Gerar token** em cada conta, faça login e copie o token (começa com `IGAA`).
3. Permissões que o app precisa ter: `instagram_business_basic`, `instagram_business_content_publish`,
   `instagram_business_manage_comments`, `instagram_business_manage_messages`,
   `instagram_business_manage_insights`.

Como as contas têm papel no próprio app, não é preciso passar pela revisão da Meta.

### Atalho: rodar no seu computador

Para testar sem hospedar, com Node 20+ instalado:

```bash
cd mcp/instagram
./scripts/rodar-local.sh
```

O script instala o que falta, pede os dois tokens (só na primeira vez), confere os tokens na Meta, abre um
endereço público temporário com o `cloudflared`, liga o servidor e adiciona o conector `instagram-nxp` no Claude Code.
Os agendamentos só saem enquanto a janela estiver aberta.

### 3. Hospedar o servidor

Requisitos: **HTTPS público** (a Meta baixa as mídias daqui) e **disco persistente** (fila de agendamentos).
Qualquer serviço que rode Docker com volume serve: Railway, Render, Fly.io ou uma VPS.
Evite hospedagens com disco temporário (como o Heroku comum), porque os agendamentos se perdem a cada reinício.

Variáveis de ambiente (veja `.env.example`):

| Variável | O que é |
|---|---|
| `MCP_ACCESS_KEY` | Senha do conector. Gere com `openssl rand -hex 24` |
| `PUBLIC_BASE_URL` | Endereço https do servidor, ex: `https://instagram-mcp.nerdexperience.com.br` |
| `IG_TOKENS` | `{"nerdexperience":"IGAA...","nerdverso":"IGAA..."}` — a chave é só o apelido da conta usado nas conversas; o perfil real vem do token (`nerdverso` → @nerdverso.nxp) |
| `DATA_DIR` | Pasta persistente (no Docker já é `/data`) |

```bash
docker build -t nxp-instagram-mcp .
docker run -d -p 3000:3000 -v nxp-ig-data:/data --env-file .env nxp-instagram-mcp
curl https://SEU-DOMINIO/health   # {"ok":true}
```

### 4. Conectar no Claude

**claude.ai:** Configurações → Conectores → **Adicionar conector personalizado** (em planos Team/Enterprise, um
administrador adiciona em Configurações da organização → Conectores).

- Nome: `Instagram NXP`
- URL: `https://SEU-DOMINIO/mcp/SUA_MCP_ACCESS_KEY`

Depois ative o conector na conversa ou no projeto em que a operação vai acontecer.

**Claude Code:**

```bash
claude mcp add --transport http instagram-nxp https://SEU-DOMINIO/mcp --header "Authorization: Bearer SUA_MCP_ACCESS_KEY"
```

> A URL com a chave funciona como senha: quem tiver a URL consegue publicar nas contas.
> Não cole em grupos nem em documentos. Se vazar, troque `MCP_ACCESS_KEY` e atualize o conector.

---

## Exemplos de uso

- "Agenda o carrossel do ID 2026-10-16_NXP_14h no @nerdexperience pra quinta 14h, com as artes da pasta do Drive, corte 4:5."
- "Publica agora esse story no nerdverso: [link do Drive]."
- "O que tem agendado pra essa semana nas duas contas?"
- "Me traz os comentários sem resposta dos últimos 10 posts e sugere respostas. Quem perguntou de ingresso, prioriza."
- "Quais foram os 5 reels com mais alcance em outubro?"

Regra de operação recomendada: o Claude prepara e mostra o post (arte, corte, legenda e horário) e **só publica,
responde ou envia DM depois do ok da pessoa responsável**.

## Desenvolvimento

```bash
npm install
npm test
cp .env.example .env   # preencha
node --env-file=.env src/server.js
```
