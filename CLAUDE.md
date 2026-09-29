# nerd-exp

Repositório do Nerd Experience (NXP). Contém:

1. **Site institucional** (Nuxt 2 + Buefy/Bulma, TypeScript) — `pages/`, `components/`, `assets/`, `nuxt.config.ts`. Comandos: `npm run dev`, `npm run build`, `npm run lint`.
2. **Especialista em artes NXP** — skills do Claude para identidade visual, social media, copy e vídeo do Nerd Experience e do NerdVerso. Entrada: `nxp-brand/README.md`.

## Trabalho criativo (posts, stories, reels, campanhas, revisão de arte, Canva)

- Use a skill `nxp-especialista` (e `nxp-criar-post`, `nxp-revisar-arte`, `nxp-planejar-campanha` conforme o pedido). Para lotes grandes, delegue ao subagente `nxp-diretor-de-arte`.
- Design mestre no Canva: `DAHF08WuL5g` ("NXP Pop Festival"). Nunca apagar/sobrescrever páginas sem confirmação.
- **Padrão de entrega**: toda arte é montada e deixada **editável no Canva** (cópia do modelo, nome `NXP · [Formato] · [Campanha] · [Variação] · vN`, pasta da campanha dentro de `NXP 2027 — Posts Instagram`), e a resposta traz o link de edição + PNGs em `entregas/`. Detalhes em `.claude/skills/nxp-especialista/references/12-canva-workflow.md`.
- Não inventar fatos do evento; marcar `[A CONFIRMAR]`.
- Responder em português do Brasil.

## Site

- A cor `$warning: #FF6700` em `assets/css/custom.scss` é da identidade antiga; a identidade 2027 está em `.claude/skills/nxp-especialista/assets/tokens.css`.
