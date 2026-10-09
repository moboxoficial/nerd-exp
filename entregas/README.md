# Fazedor de posts oficial — Nerd Experience

Pasta das peças de Instagram do NXP 2027. Cada post tem uma pasta própria com os PNGs e a `LEGENDA.md` (ficha de produção, legenda, alt text e QA).

## Como pedir um post

Peça ao Claude neste repositório, por exemplo: "cria um post anunciando X". Se tiver, mande junto:

- objetivo (vender lote, anunciar atração, engajar…)
- formato (feed, story, carrossel, reels)
- dados factuais (dia, preço, cupom, @ dos convidados); o que faltar sai marcado como `[A CONFIRMAR]`
- fotos oficiais (press kit) dos convidados
- data e horário de publicação

## Fluxo (360)

O processo completo está na skill `.claude/skills/nxp-fazedor-de-posts/SKILL.md`. Em resumo:

1. Briefing: o Claude pede as fotos oficiais e os dados que faltarem.
2. A arte é montada no Canva a partir das páginas-modelo do mestre "NXP Pop Festival" (`DAHF08WuL5g`) e fica **editável**.
3. QA visual: export, fatiamento em 1080×1350 (`scripts/fatiar.sh`) e conferência de cada slide e de cada divisa.
4. Entrega aqui, em `AAAA-MM-DD_formato_campanha/`: os slides + `LEGENDA.md` (texto da arte, legenda, primeiro comentário, alt text e QA). Só publique sem nenhum ❌ no QA.
5. Com aprovação, a peça entra no volume ativo `NXP 2027 — Posts Instagram · vol. N` e é registrada no `INDICE.md`.
6. Se a equipe ajustar a arte no Canva, o Claude puxa a versão nova e registra o ajuste em `references/aprendizados.md`. É assim que a skill melhora a cada post.

## Nome das peças

`NXP · [Formato] · [Campanha] · [Variação] · vN` (perfil NerdVerso: `NERDVERSO · …`).
