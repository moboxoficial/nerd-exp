# Receitas de Canva (testadas na prática)

Complementam `12-canva-workflow.md` da skill `nxp-especialista`. Quando uma receita mudar, atualize aqui e registre em `aprendizados.md`.

## Fotos de convidados

1. **Melhor fonte: o arquivo que a equipe manda no chat.** Ele fica em `/tmp/.../images/N.jpg`. Para subir no Canva:
   - `create-upload-url` → `curl -X POST -H "Content-Type: application/octet-stream" --data-binary @arquivo "<uploadUrl>"` → a resposta traz o `mediaId`.
   - A URL de upload vale para um envio só. Se falhar, peça outra.
2. **Recorte sem fundo**: `remove-background` com `{"type":"MEDIA","id":"<mediaId>"}` gera um novo `mediaId` com transparência. Fica ótimo sobre o portal neon.
3. **Busca na web (último recurso)**: o sandbox e o Canva recebem 429 do Wikimedia (`upload.wikimedia.org` e a API). As versões no Flickr (`live.staticflickr.com/..._o.jpg`, vindas do campo "Source" da página do Commons) baixam normalmente. Sempre confira a licença (CC BY / CC BY-SA) e anote o crédito. Prefira pedir a foto oficial à equipe.
4. Resolução: abaixo de ~1000 px de largura a foto fica suave na capa. Registre na ficha e peça a versão em alta.

## Template "Atração confirmada" — pág. 202 do mestre (carrossel 3240×1350)

`copy-design` com `page_numbers: [202]`. Mapa dos elementos (os IDs se mantêm na cópia):

| Slide | Elemento | ID | Observação |
|---|---|---|---|
| 1 | Título linha 1 (branco) | `LBBq230YJsv329fj` | fonte larga: "JOVEM NERD" (10 caracteres) cabe em **110 px** |
| 1 | Título linha 2 (ciano) | `LBVgzDgm3fTbCbFH` | 112 px |
| 1 | Pill ciano | `LBWX11qRc3pK2hvt` | "ATRAÇÕES CONFIRMADAS" cabe em **56 px** |
| 1 | Selo "maior evento nerd da galáxia" | `LBrjq8ZSQktB1pZc` | imagem |
| 1 | Paisagem placeholder | `LB1VrMR80BsBWqPV` **e** `LBt8Sjqx11CzKcZS` | **a paisagem está em DOIS elementos**: apague os dois |
| 1 | Faixa escura de baixo | `LBkMgM8GgNb0H908` | começa em y≈838 |
| 1 | Grupo logo + além do portal | `LBtgFGB6JcxzqZBT` | |
| 1 | Grupo data do topo | `LB7LzDTylHnMJ9gr` | o texto vem em `#291833`: fica **invisível** em fundo escuro, recolorir para `#01FF9F` / branco |
| 2 | Pills amarelas | `LB3wJSTJn9vj4tZw`, `LBmbDJc78Bcp2QrZ` | 12 caracteres cabem em **78 px** |
| 2 | Texto corrido | `LBPsw4m0Ckw4yK3S` | ~45 palavras no máximo |
| 2 | Blob com foto | `LBMb0LgRsN1npqT9` | o formato original tem um "dente" que corta rostos (ver abaixo) |
| 2 | Blob escuro decorativo | `LBX2DKndW27R371t` | fica por cima da foto se não reordenar |
| 1–2 | Blob rosa atravessando | `LB6ttDy5wvGtcz61` | vaza uma faixa rosa na lateral direita do slide 1 |
| 3 | Assinatura (data, Expominas, ingressos) | grupo `LB3yPjWKRL3bzwMH` | normalmente não mexe |

### Capa com a dupla recortada sobre o portal

1. `delete_element` nos dois elementos de paisagem.
2. `insert_shape` retângulo `#291833` 1080×860 em (0,0).
3. `insert_fill` do portal `MAHFzkYrLZs` (≈860×860, centralizado). Funcionou na cópia do template.
4. `insert_fill` do recorte (proporção da foto, ~1020 px de largura).
5. **Camadas**: o que é inserido vai para o topo. Ordem final com `layer_element` → `front`, um por vez: retângulo escuro → portal → recorte → faixa escura → logo → data → título. Assim o retângulo cobre também o vazamento rosa.
6. Desça o título para baixo da linha dos corpos (y≈868 / 978 / 1122 / 1228) ou use contorno ou degradê escuro se ele ficar por cima da foto.

### Foto dentro de blob

- `crop_media` em shape força "cover": `left`/`top` só podem ser ≤ 0 e a imagem precisa cobrir o shape inteiro.
- Se um rosto cair no recorte do blob, troque o formato: `replace_shape` com um blob arredondado, por exemplo `M250 8 C370 -4 470 80 474 205 C478 330 420 470 270 482 C140 492 30 430 8 300 C-12 175 60 90 140 40 C175 18 210 12 250 8 Z` (viewBox 477.4×486.9).
- **`replace_shape` reseta o crop**: refaça o `crop_media` depois.
- Traga o blob da foto para frente (`layer_element` front) se um blob decorativo estiver cobrindo a foto.

## Texto

- `add_text` não aplica a Genius Techo. Prefira reaproveitar caixas de texto do template.
- Depois de `replace_text`, confira a altura do elemento na resposta: se dobrou, quebrou linha. Reduza a fonte até voltar a uma linha.

## Exportar e fatiar

- `export-design` (png, `pages: [N]`) → `.claude/skills/nxp-fazedor-de-posts/scripts/fatiar.sh "<url>" entregas/<pasta>`.
- O download de `export-download.canva.com` funciona no sandbox (testado em 08/10/2026).
- Sempre olhe `preview.png` e cada `divisa-K.png` antes de entregar.

## Transações

- `read-design` com `open_transaction: true` → `edit-design` (`keep_open`) → conferir a miniatura → `commit`.
- No temporário, pode salvar sem pedir. No volume e no mestre, só com aprovação. `merge-designs` sempre pede aprovação explícita.
