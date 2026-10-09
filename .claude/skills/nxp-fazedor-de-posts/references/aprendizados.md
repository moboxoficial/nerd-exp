# Aprendizados — o que a equipe ajustou e o que deu errado

Diário vivo do fazedor de posts. **Toda peça termina com uma entrada aqui** (passo 9 do `SKILL.md`). Antes de criar uma peça, leia as seções "Preferências da equipe" e "Armadilhas".

## Preferências da equipe (o que a equipe faz quando mexe na arte)

Cada item vem de uma correção real. Quando a mesma preferência aparecer de novo, suba para o `SKILL.md`.

- **Rostos grandes na capa.** O ponto de entrada é a cara do convidado: a dupla ocupa a largura toda do slide, com o portal visível atrás. (Jovem Nerd e Azaghal, 08/10/2026)
- **Topo em linha única**: NERD:XP + selo "além do portal" + bloco de data lado a lado. Nada de selo solto no meio da foto. (08/10/2026)
- **Título pode invadir a foto**: o nome do convidado sobreposto à base da foto, com contorno escuro, em vez de uma faixa separada. (08/10/2026)
- **Não aceita emenda visível**: dois retângulos escuros vizinhos precisam ter a borda alinhada. (08/10/2026)
- **Foto da equipe > foto da internet**: a equipe mandou a foto de estúdio oficial assim que viu o placeholder. Peça a foto logo no briefing. (08/10/2026)
- **Anúncio de atração segue o post do Gaveta** (pág. 137 do mestre: carrossel 3 slides com card central verde, nome grande, foto no portal e selo roxo). Não o template genérico de "Atração confirmada" (pág. 202) nem o carrossel "Feh Dubs + Gaveta", que é para duas atrações separadas. (09/10/2026)
- **"Faz o card completo"**: a equipe espera a arte pronta para publicar, não rascunho com placeholder. Se faltar a foto, peça antes de montar ou resolva com uma fonte licenciada. (08/10/2026)

## Armadilhas técnicas

- Wikimedia bloqueia o sandbox e o Canva (429). Flickr original funciona. (08/10/2026)
- A paisagem placeholder da pág. 202 está em dois elementos. Se apagar um só, ela continua aparecendo. (08/10/2026)
- O texto escuro do template some quando o fundo vira escuro. Recolorir a data do topo. (08/10/2026)
- O blob rosa do slide 2 vaza para o slide 1 quando o fundo da capa muda. (08/10/2026)
- `replace_shape` reseta o crop da imagem. (08/10/2026)
- A conexão com o Canva pode cair (reinício do worker) e a transação aberta some com as edições não salvas. Faça `commit` assim que a miniatura estiver boa e não acumule muitos blocos sem salvar. (09/10/2026)
- Para achar uma peça antiga no mestre, `search-designs` não acha páginas. Leia `design_content` em blocos de 50 páginas, procure o texto (ex.: "Mestre da Criação") e depois veja `page_metadata` + miniaturas só das páginas candidatas. (09/10/2026)
- Recorte de pessoa passando da divisa do slide (1080 px) aparece como pedaço solto no slide seguinte. Conferir em `divisa-K.png`. (08/10/2026)

## Registro por peça

| Data | Peça | O que a equipe mudou depois | Lição |
|---|---|---|---|
| 09/10/2026 | NXP · Carrossel · Atração · Jovem Nerd e Azaghal (modelo Gaveta) · v2 | Pediu para refazer no modelo do post do Gaveta | Atração = modelo pág. 137; perguntar "segue o modelo de qual post?" quando houver referência anterior |
| 08/10/2026 | NXP · Carrossel · Atração · Jovem Nerd e Azaghal · v1 | Ampliou a dupla, alinhou o topo, pôs contorno no título, corrigiu a emenda da faixa escura | Capa de atração = rosto grande + portal; conferir as divisas; pedir a foto oficial no briefing |
