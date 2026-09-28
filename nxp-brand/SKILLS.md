# Skills do time criativo NXP — o que cada função precisa e como instalar

Skills são pastas com instruções (`SKILL.md`) que o Claude carrega sozinho quando o pedido combina com a descrição delas. Elas funcionam no **Claude Code** (terminal/app no Mac e nesta sessão na nuvem) e no **claude.ai / app Claude** (Configurações → Capacidades → Skills).

## 1. Skills próprias do NXP (já estão neste repositório)

| Skill | Função | Quando ativa |
|---|---|---|
| `nxp-especialista` | Base de conhecimento: identidade, cores, fontes, elementos, formatos, voz, lore, biblioteca do Canva, social, vídeo, QA, exemplos | Qualquer pedido sobre NXP/NerdVerso |
| `nxp-criar-post` | Fluxo briefing → conceito → ficha de produção → Canva → QA | "Cria um post/story/carrossel/reels…" |
| `nxp-revisar-arte` | Revisão crítica com veredito e correções | "Revisa essa arte", "tá no padrão?" |
| `nxp-planejar-campanha` | Calendário editorial e sequências de campanha | "Calendário do mês", "campanha do lote" |
| Subagente `nxp-diretor-de-arte` | Isola trabalhos grandes (campanha inteira, lote de revisões) | Delegação automática ou "usa o diretor de arte" |

## 2. Mapa de competências → skills recomendadas

| Função | Competências | Skills |
|---|---|---|
| **Designer / diretor de arte** | Identidade visual, composição, hierarquia tipográfica, cor, grid, adaptação de formatos, pôster/KV, mock de layout | `nxp-especialista` · `nxp-revisar-arte` · Anthropic **canvas-design** (pôsteres/artes estáticas em PNG/PDF) · **frontend-design** (landing/HTML com direção de arte) · **theme-factory** (aplicar tema a decks/docs) · **algorithmic-art** (texturas/fundos generativos p5.js) |
| **Social media** | Calendário, pilares, legendas, hashtags, stories com stickers, comunidade, métricas | `nxp-planejar-campanha` · `nxp-criar-post` · marketingskills **social**, **content-strategy**, **community-marketing**, **analytics**, **marketing-ideas** |
| **Copywriter** | Ganchos, CTA, voz de marca, revisão | marketingskills **copywriting**, **copy-editing**, **marketing-psychology**, **offers** |
| **Editor de vídeo / motion** | Roteiro de reels, ritmo, legendas, export, GIF | `nxp-especialista` (ref. 11) · marketingskills **video** · Anthropic **slack-gif-creator** (GIFs animados otimizados) |
| **Expert em redes / growth** | Lançamentos, viradas de lote, eventos, influenciadores/afiliados, anúncios | marketingskills **launch**, **events**, **influencer-marketing**, **ad-creative**, **image**, **product-marketing** |
| **Documentos e apresentações** | Deck para patrocinador, relatório, planilha de calendário | Anthropic **pptx**, **docx**, **xlsx**, **pdf** (já habilitadas no claude.ai; no Claude Code via plugin `document-skills`) |
| **Criar novas skills** | Transformar processos em skills | Anthropic **skill-creator** |

O arquivo `.claude/product-marketing.md` já foi preenchido com o contexto do NXP — as skills do marketingskills leem esse arquivo automaticamente e não vão ficar perguntando o básico.

## 3. Como instalar as skills de terceiros (você roda — 2 minutos)

> Por segurança, código de terceiros não foi copiado para dentro do repositório: você instala direto da fonte oficial e decide o que habilitar.

### No Claude Code (Mac ou nuvem), dentro de uma sessão:

```text
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
/plugin install document-skills@anthropic-agent-skills

/plugin marketplace add coreyhaines31/marketingskills
/plugin install marketing-skills@marketingskills
```

Depois rode `/plugin` para ver/desabilitar o que não usar. Repositórios:
- Anthropic (oficial): https://github.com/anthropics/skills — `example-skills` inclui canvas-design, frontend-design, theme-factory, algorithmic-art, slack-gif-creator, skill-creator, web-artifacts-builder, entre outras.
- Corey Haines (MIT, 50 skills de marketing): https://github.com/coreyhaines31/marketingskills
- Outras coleções citadas em tutoriais (avaliar antes): https://github.com/BrianRWagner/ai-marketing-claude-code-skills · https://github.com/charlie947/social-media-skills (focado em LinkedIn) · lista curada https://github.com/BehiSecc/awesome-claude-skills

### No claude.ai / app Claude

1. Configurações → **Capacidades** → ative **Skills** (e "Code execution").
2. As skills da Anthropic (pptx, docx, xlsx, pdf, canvas-design etc.) aparecem como opção nativa — ative as que quiser.
3. Para as skills do NXP: rode `scripts/empacotar-para-claude-ai.sh` e faça upload dos `.zip` gerados em `dist/claude-ai/` (Configurações → Capacidades → Skills → Upload).
4. Conecte o **Canva** em Configurações → Conectores para o especialista ler/editar o design.

## 4. Ferramentas de sistema úteis no Mac (para vídeo e imagem)

```bash
brew install ffmpeg imagemagick
```
Fontes: instale Lexend Deca (Google Fonts) e as licenças de Genius Techo e Deli se for produzir fora do Canva.
