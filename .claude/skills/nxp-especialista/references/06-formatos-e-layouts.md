# 06 — Formatos e layouts

Formatos encontrados no Canva (contagem aproximada nas 328 páginas):

| Formato | Medida (px) | Uso | Qtde |
|---|---|---|---|
| **Feed retrato 4:5** | 1080×1350 | Post único / capa de carrossel | ~70 |
| **Story / Reels 9:16** | 1080×1920 | Stories, capa de reels | ~90 |
| **Carrossel panorâmico** | 2160 / 3240 / 4320 / 5400 / 6480 / 7560 × 1350 | 2 a 7 slides de 1080×1350 com fundo contínuo | ~90 |
| **Banner Sympla/site** | 2182×721 | Capa da página de venda, seções do site | ~22 |
| **KV horizontal** | 1640×924 · 1920×1080 · 1600×838 | Key visual, eventos, apresentação | ~8 |
| **Faixa de título** | 1080×200 | Cabeçalhos do guia de embaixadores | 10 |
| **Avatar** | 500×500 | Foto de perfil de convidado com portal | 2 |
| **Link/OG** | 1299×628 | Compartilhamento de link | 2 |
| Outros | 397×560 (card), 1123×794 (A4 paisagem) | Impressos pontuais | — |

## Zonas seguras

- **Story/Reels 1080×1920**: nada importante nos **250 px do topo** e **340 px da base** (UI do Instagram). Margem lateral 64 px.
- **Feed 1080×1350**: margem 60–72 px; a grade do perfil corta para 1080×1350 (4:5), então o conteúdo central (1080×1080) deve funcionar sozinho em miniatura.
- **Carrossel panorâmico**: cada divisa de slide (a cada 1080 px) não pode cortar texto nem rosto; use blobs/portal para cruzar a divisa. Primeiro slide = capa autônoma; último = assinatura + CTA.

## Layouts padrão

### A. Feed "anúncio" (ex.: lote esgotado — `assets/exemplos/feed-4x5-lote-esgotado.jpg`)
```
[ topo ]      NERD:XP  +  além do portal (lado a lado, centralizado)
[ centro ]    PORTAL grande + pills empilhadas com a mensagem
              faixas inclinadas cruzando (marquee)
[ base ]      27 e 28 (verde) | FEVEREIRO / DE 2027 (branco)
              [NO EXPOMINAS] (pill amarela)
fundo: #291833 túnel wireframe + blobs verde/ciano nos cantos
```

### B. Feed "atração confirmada"
```
topo: ATRAÇÃO CONFIRMADA (pill) + logo
centro: foto recortada do convidado com portal colorido atrás
        NOME em Genius Techo grande (ex.: ANDERSON / GAVETA)
        pill com o dia: "28 DE FEVEREIRO"
base: bloco de data + "Ingressos disponíveis — link na bio"
```

### C. Story "comunidade / data" (ex.: `story-9x16-may-the-4th.jpg`)
```
topo (abaixo de 250px): lettering temático dentro do portal
meio: foto de cosplayers do evento em tela cheia, escurecida na base
base (acima de 340px): logo NXP pequeno → título 3 linhas (branco + ciano)
      → frase de ação → pill amarela ("VAMOS REPOSTAR")
```

### D. Story teaser "Portal 404"
```
fundo preto/berinjela, portal verde girando com "?" no centro
texto curto em 2–3 linhas: "O PORTAL ESTÁ EMITINDO SINAIS…"
CTA: "Deixe seu palpite nos comentários" / "COMENTE 404"
contagem: "REVELAÇÃO AMANHÃ 10H" / "SÁBADO 04/07 — 12H"
```

### E. Carrossel panorâmico informativo (ex.: `carrossel-5x-seletiva-cosplay.jpg`)
```
slide 1: capa — logo, título grande, foto, data/local
slide 2: contexto (texto curto em Genius Techo)
slide 3: critérios/lista em etiquetas coladas ao redor de uma figura central
slide 4: "QUANDO E ONDE?" com lista com setas →
slide 5: passos em botões escuros (1,2,3,4)
slide 6: premiação dentro do portal
slide 7: fechamento — frase de marca + 27 e 28 + além do portal
fundo: degradê violeta→ciano contínuo com blobs escuros atravessando
```

### F. Banner Sympla 2182×721
Logo NERD:XP à esquerda (1/3), "além do portal" + portal ao centro, blobs e wireframes espalhados, CTA em pill "GARANTA SEU INGRESSO AGORA"; foto/cosplay opcional à esquerda.

### G. Cartão de personagem (série "NXP apresenta")
Carrossel 4320×1350 (4 slides): 1) nome gigante + ilustração + papel ("Herói de Pixel") na cor do mundo; 2) frase-conceito em balão; 3) 3 atributos em etiquetas (ex.: DISCIPLINA · JUSTIÇA · PROTEÇÃO); 4) fechamento com logo, além do portal e data.

### H. Interação
Grade de caça-palavras, bingo "Você estava na 10ª edição?", quiz "Qual mundo te representa?" (4 quadrantes coloridos por mundo), "Confissões nerds", "O que não pode faltar no palco?" — sempre com instrução de resposta ("comente", "marque", "print e poste").

## Exportação

- Feed/story: PNG (textos nítidos) ou JPG qualidade 90+; sRGB.
- Carrossel panorâmico: exportar e fatiar em 1080×1350 (ver comando ffmpeg/ImageMagick em `11-video-e-motion.md`).
- Nome de arquivo: `AAAA-MM-DD_formato_campanha_vN` (ex.: `2026-10-07_feed_dia-criancas_v2.png`).
