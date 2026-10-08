---
name: nxp-fazedor-de-posts
description: Fazedor de posts oficial do Nerd Experience (NXP) — fluxo 360 de ponta a ponta para qualquer peça de Instagram (feed, carrossel, story, reels, banner). Vai do briefing e das fotos até a arte pronta e editável no Canva, QA visual, PNGs fatiados, legenda, entrega no repositório, consolidação no volume do Canva e registro do que aprendeu. Use sempre que pedirem "cria/faz um post, card, story, carrossel, arte" do NXP, anúncio de atração, promoção, lote, contagem regressiva, ou quando a equipe mostrar uma arte ajustada ("mexi, ficou assim").
---

# Fazedor de posts NXP — fluxo 360

Este é o fluxo deste repositório. A identidade, a voz e os fatos vêm da skill **`nxp-especialista`**: carregue-a antes e use as referências dela (01 fatos, 06 formatos, 07 voz, 09 biblioteca, 12 Canva, 13 QA, 15 design). Aqui ficam o **processo completo** e o que a equipe já ensinou.

**Antes de tudo, leia `references/aprendizados.md`** (preferências da equipe e armadilhas) e `references/receitas-canva.md` (como fazer cada coisa no Canva sem tropeçar).

## Meta

A equipe pede "faz o post" e recebe a **peça completa**: arte final com foto, editável no Canva, PNGs, legenda, alt text e QA. Rascunho com placeholder só se a equipe pedir.

## 1. Briefing (uma mensagem só, perguntando apenas o que falta)

| Campo | Se não vier |
|---|---|
| Objetivo e mensagem-chave | deduza e declare a suposição |
| Formato | anúncio de atração = carrossel de 3 slides (pág. 202); demais casos: feed 4:5 + story |
| Fatos (dia, preço, cupom, @) | `[A CONFIRMAR]`, **nunca invente** |
| **Fotos / ativos** | **peça já no briefing**: "manda a foto oficial em alta?" |
| Data e horário de publicação | sugira 12h ou 19h |

Se a equipe disser só "cria", não trave: siga com as suposições e liste as pendências no final.

## 2. Conceito

Se o pedido estiver aberto, dê 3 opções curtas (título com destaque, modo de cor, âncora visual, página-modelo) e recomende uma. Se for um formato que já tem padrão (atração confirmada, contagem, lote), vá direto ao padrão.

## 3. Montagem no Canva (temporário editável)

1. `copy-design` da página-modelo do mestre `DAHF08WuL5g`. Título: `TEMP · NXP · [Formato] · [Campanha] · [Variação] · vN`.
2. Textos: reaproveite as caixas do template (a Genius Techo não entra via `add_text`). Ajuste a fonte até não quebrar linha.
3. Fotos: upload do arquivo da equipe → `remove-background` para recorte → portal atrás (receita em `receitas-canva.md`).
4. Camadas e cores: apague todos os placeholders, recolora o texto que ficar escuro sobre fundo escuro e reordene as camadas.
5. `commit` no temporário depois de cada bloco de edição.

## 4. QA visual (obrigatório, em loop até passar)

1. `export-design` png → `bash .claude/skills/nxp-fazedor-de-posts/scripts/fatiar.sh "<url>" entregas/<AAAA-MM-DD_formato_campanha>`
2. **Olhe** `preview.png`, cada `slide-N.png` em tamanho real e cada `divisa-K.png`. Procure:
   - placeholder sobrando (paisagem, lorem, "nome atração"), texto invisível ou quebrado;
   - rosto cortado por blob ou divisa, pessoa ou objeto vazando para o slide vizinho;
   - emendas entre formas, faixas de cor vazando;
   - título legível em miniatura (30%).
3. Rode o checklist `13-checklist-qa.md` da `nxp-especialista`.
4. Corrigiu? Exporte e olhe de novo. Só entregue sem ❌ de arte.

## 5. Entrega

- Em `entregas/<pasta>/`: `slide-N.png` + `LEGENDA.md` (ficha com status, Canva, texto da arte, legenda, 1º comentário, collab, alt text, desdobramentos, QA e pendências). Modelo: `entregas/2026-10-08_carrossel_atracao-jovem-nerd-azaghal/LEGENDA.md`.
- Commit + push na branch de trabalho.
- Na resposta: as imagens (SendUserFile), o link do Canva, a legenda pronta para copiar e as pendências em lista curta.

## 6. Quando a equipe mexer na arte ("mexi, ficou assim")

1. Compare a versão dela com a sua e diga o que melhorou e o que ainda falha (com a correção).
2. Exporte a versão dela do Canva, rode `fatiar.sh` e atualize os PNGs e a ficha.
3. **Registre em `aprendizados.md`** o que ela mudou, como preferência da equipe. Isso é o que faz a skill melhorar.

## 7. Consolidação no Canva (com aprovação)

Peça aprovação explícita e depois siga o "PADRÃO DE ENTREGA" de `12-canva-workflow.md`: `merge-designs` no volume ativo (1 `insert_pages` por chamada), escreva as notas da página com o nome padrão, mova o temporário para `🗑️ PARA APAGAR` e registre volume e página em `entregas/INDICE.md`.

## 8. Desdobramentos

Ofereça story 9:16 (`resize-design` + revisar as zonas seguras de 250 e 340 px) e roteiro de reels. Faça na hora se a equipe aceitar.

## 9. Aprender (fecha toda peça)

- Acrescente uma linha em "Registro por peça" de `aprendizados.md` e, se for o caso, novas armadilhas e preferências.
- Quando a mesma preferência aparecer **duas vezes**, promova-a a regra neste `SKILL.md` ou em `receitas-canva.md`.
- Receita nova no Canva (IDs de template, tamanhos de fonte que cabem, ordem de camadas) vai para `receitas-canva.md`.
- Commit junto com a peça.
