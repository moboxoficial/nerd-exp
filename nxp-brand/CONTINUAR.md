# Continuar o trabalho do NXP em outra sessão (Claude Code, claude.ai ou Codex)

Documento de passagem: onde as coisas estão e qual é o próximo passo. Cole no primeiro prompt da nova sessão:
> "Leia `nxp-brand/CONTINUAR.md` e `CLAUDE.md` (ou `AGENTS.md`) e continue de onde parou."

## Estado em 2026-09-29

| Item | Onde |
|---|---|
| Regras da marca e do fluxo | `.claude/skills/nxp-especialista/` (SKILL.md + `references/01…14`) |
| Padrão de entrega no Canva (obrigatório) | `.claude/skills/nxp-especialista/references/12-canva-workflow.md`, seção "PADRÃO DE ENTREGA" |
| Índice de tudo que já foi produzido | mesmo arquivo, seção "Registro: índice dos volumes" |
| Planilha de conteúdo | https://docs.google.com/spreadsheets/d/1dfdtfDN4gaFATh5Dn2gcq3DqosHl9Zqy (dá pra baixar em CSV/XLSX com `export?format=xlsx`) |
| Mapa de outubro | `entregas/MAPA_outubro_feed.md`: 100% coberto |
| Lista de feed de outubro e novembro | `entregas/LISTA_posts-feed-planilha.md` |
| PNGs e legendas | `entregas/AAAA-MM-DD_[formato]_[slug]/` (slides + `LEGENDA.md`) |

### Canva
- Design mestre (modelos, somente leitura): `DAHF08WuL5g`
- Pasta: `NXP 2027 — Posts Instagram` (`FAHWieBU748`)
- **vol. 1** `DAHWihdcqtc`: 98 páginas, **cheio**
- **vol. 2** `DAHWizfK3FI`: 58 páginas, **ativo** (cabem cerca de 37 páginas; depois disso, abrir o vol. 3)
- Lixeira manual: `🗑️ PARA APAGAR (lixeira)` (`FAHWiiIrtak`). O usuário esvazia no Canva, porque a API não apaga.
- Limites da API: no máximo 100 páginas por design; `merge-designs` aceita 1 operação por chamada; mediaId do mestre não funciona em outro design (use o método de extração).

## Próximo passo
**Novembro**: 104 peças de feed/carrossel/card, já mapeadas em `entregas/MAPA_novembro_feed.md` (fonte: aba NOVEMBRO, que é o calendário oficial; ignore as linhas de novembro da aba OUTUBRO). Mesmo processo de outubro:
1. Mapear (`entregas/MAPA_novembro_feed.md`): o que já tem arte (link canva.link na planilha), o que é duplicado e o que falta produzir.
2. Produzir em lotes por tema (subagente `nxp-diretor-de-arte`). Cada lote entrega só os temporários, os PNGs e as LEGENDAs, junto com os IDs.
3. O agente principal consolida no volume ativo (1 `insert_pages` por chamada, em ordem cronológica), escreve o índice nas notas, manda os temporários pra lixeira e atualiza o índice na skill e as LEGENDAs.
4. Fazer commit e push.

## Pendências abertas (do usuário)
- Esvaziar a lixeira do Canva.
- Aprovar: personagem Jhon (nº 26), conteúdo narrativo novo (Arquivo Nerd, Eldarion, protocolo, Tirinha #3), CTA do Pixel, critérios do jurado de cosplay.
- Completar os `[A CONFIRMAR]` de cada `LEGENDA.md` (promo 404, credencial Next Level, URL da Bíblia, acesso ao Expominas, meia-entrada…).
- Autorização de imagem de menores nas fotos (Família, Dia das Crianças, Magia).
- Google Drive: o conector respondia "operation not enabled". Com acesso, trocar as fotos repetidas.

## Rodar sem pedidos de aprovação
- **Claude Code (terminal/app):** inicie com `claude --permission-mode bypassPermissions` (ou alterne com `Shift+Tab`). Para ficar permanente, em `~/.claude/settings.json` use `"permissions": {"defaultMode": "bypassPermissions"}` ou libere as ferramentas com `/permissions` (`mcp__Canva__*`, `Bash`, `Edit`, `Write`).
- **claude.ai/code (nuvem):** escolha o modo de permissão no seletor da sessão, antes de enviar o primeiro prompt.
- **Codex:** `codex --full-auto` ou `codex --dangerously-bypass-approvals-and-sandbox`. O Codex lê o `AGENTS.md` da raiz. É preciso conectar o MCP do Canva no Codex (`~/.codex/config.toml`, seção `[mcp_servers]`) para ele conseguir editar os designs.
