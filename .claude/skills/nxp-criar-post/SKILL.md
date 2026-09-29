---
name: nxp-criar-post
description: Fluxo passo a passo para criar uma peça de Instagram do Nerd Experience (feed, story, reels, carrossel ou banner) do briefing até a arte pronta no Canva e a legenda. Use quando o usuário pedir "cria um post/story/carrossel/reels do NXP", "faz uma arte pra anunciar X", "preciso divulgar a promoção Y", ou colar um briefing de campanha do Nerd Experience.
---

# Criar peça NXP

Pré-requisito: carregue a skill **nxp-especialista** (identidade, voz e checklist). Se ela não estiver disponível, peça para o usuário instalá-la antes.

## Passo 1 — Briefing mínimo (pergunte só o que faltar, em uma mensagem)

| Campo | Exemplo | Padrão se não informado |
|---|---|---|
| Objetivo | vender 2º lote / anunciar atração / engajar | deduzir do pedido |
| Formato(s) | feed 4:5, story, reels, carrossel | feed + story |
| Mensagem-chave | "2º lote acaba domingo" | — (obrigatório) |
| Dados factuais | preço, datas, cupom, nomes | `[A CONFIRMAR]` |
| Ativos | fotos, logo de parceiro, vídeo | fotos de edições anteriores |
| Prazo / data de publicação | 07/10 às 12h | próximo horário forte (12h ou 19h) |

## Passo 2 — Conceito (3 opções curtas)

Para cada opção: título da arte (com destaque marcado em `[ ]`), modo de cor, elemento-âncora (portal/blob/foto/personagem), página-modelo do Canva sugerida (`references/09-biblioteca-canva.md` da nxp-especialista). Recomende uma.

## Passo 3 — Ficha de produção (da opção escolhida)

Entregue exatamente nesta ordem:
1. Formato e medida
2. Texto da arte linha por linha (com destaques e pills)
3. Layout (topo / centro / base + elementos)
4. Legenda completa + hashtags + primeiro comentário + alt text
5. Desdobramentos (story/reels/carrossel) em 1–2 linhas cada

## Passo 4 — Montagem

- **Com Canva MCP (padrão obrigatório)**: siga o "PADRÃO DE ENTREGA DE ARTES" em `references/12-canva-workflow.md` da nxp-especialista — copiar modelo num temporário → editar textos → trocar imagens → salvar → consolidar com `merge-designs` no **arquivo único** `DAHWihdcqtc` (1 `insert_pages` por chamada) → escrever nas notas da página o nome `NXP · [Formato] · [Campanha] · [Variação] · vN` + data e perfil → mover o temporário e os rascunhos pra `🗑️ PARA APAGAR (lixeira)` → exportar PNG do arquivo único. A arte fica **editável no Canva**; sempre entregar o link do arquivo único + as páginas junto dos PNGs. Nunca deixar design solto nem criar subpasta por campanha.
- **Sem Canva MCP**: a ficha do Passo 3 é o entregável para o designer. Se o usuário quiser um rascunho visual, gere um HTML/PNG simples com os tokens de `assets/tokens.css` (dentro da skill nxp-especialista) (marcando que é mock, não arte final).

## Passo 5 — QA

Rode `references/13-checklist-qa.md` e liste só os itens reprovados com a correção. Termine com: "Pronto para publicar" ou "Pendências: …".
