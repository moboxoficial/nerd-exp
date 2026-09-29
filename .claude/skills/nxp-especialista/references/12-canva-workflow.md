# 12 — Fluxo de produção no Canva (com Canva MCP)

Quando o conector **Canva** estiver habilitado na sessão (claude.ai → Configurações → Conectores → Canva; no Claude Code, as ferramentas `mcp__Canva__*`), o especialista pode ler, duplicar, editar e exportar peças.

## ⭐ PADRÃO DE ENTREGA DE ARTES (obrigatório)

Toda arte do NXP é **produzida e deixada no Canva, 100% editável**, pra equipe poder ajustar depois. PNG exportado é complemento, nunca o único entregável.

### A. Onde as artes moram: UM arquivo só (regra principal)

Todas as artes finais do Instagram ficam num **único design do Canva**, no mesmo espírito do mestre (1 página por post/slide ou página panorâmica por carrossel, com quantas páginas precisar):

| Item | Valor |
|---|---|
| **Arquivo único** | `NXP 2027 — Posts Instagram (arquivo único)`, ID **`DAHWihdcqtc`** ([editar](https://www.canva.com/d/c-GYLOc3-eHsiAz)) |
| Pasta | `NXP 2027 — Posts Instagram` (`FAHWieBU748`) |
| Imagens enviadas (uploads) | subpasta `_assets (imagens enviadas)` (`FAHWirZP1-Q`), quando o Canva deixar mover |
| Lixeira manual | subpasta `🗑️ PARA APAGAR (lixeira)` (`FAHWiiIrtak`): o usuário esvazia com 1 clique |

**Estrutura final da pasta, e nada além disso:**
```
NXP 2027 — Posts Instagram/
├── NXP 2027 — Posts Instagram (arquivo único)   ← todas as artes finais
├── _assets (imagens enviadas)/
└── 🗑️ PARA APAGAR (lixeira)/                    ← temporário; o usuário apaga
```
- **Proibido** deixar design solto na raiz do Canva, subpastas por campanha, cópias "NXP Pop Festival"/"Cópia de…", `_apoio` ou rascunhos visíveis.
- **Organização dentro do arquivo**: ordem cronológica de publicação. Cada página leva nas **notas** (`replace_speaker_notes`) o texto `[Nome padrão do post] — slide X/N — publicar DD/MM HHh @perfil. Legenda: entregas/…/LEGENDA.md`. Isso é o índice.
- **Nome padrão de cada peça** (vai nas notas, no registro e na pasta de `entregas/`): `NXP · [Formato] · [Campanha/Tema] · [Variação] · v[N]` (para o perfil NerdVerso, `NERDVERSO · …`).
- Se um dia o arquivo passar de ~300 páginas ou a API parar de abrir transação nele (acontece com o mestre de 329 págs.), crie `NXP 2027 — Posts Instagram (arquivo único) · vol. 2` na mesma pasta e registre aqui. Nunca volte a um design por post.

### B. Fluxo de produção (sem deixar lixo)

A API **não apaga designs nem pastas**. Por isso todo design temporário tem destino obrigatório:

1. **Área de trabalho temporária**: `copy-design` com as páginas-modelo do mestre `DAHF08WuL5g` (1 design temporário por lote). Título já no padrão da peça.
2. **Editar** no temporário: textos, imagens e crop. Manter camadas editáveis: texto como texto, imagens como fill substituível, logos soltos. Nunca achatar em imagem.
3. **Salvar (commit) logo após cada bloco de edições**, porque a conexão MCP pode cair.
4. **QA** pela miniatura + `13-checklist-qa.md`.
5. **Consolidar**: `merge-designs` com `type: modify_existing_design`, `design_id: DAHWihdcqtc`, **uma operação `insert_pages` por chamada** (a API só aceita 1 por vez), com `after_page_number` pra manter a ordem cronológica.
6. **Indexar**: abrir transação no arquivo único e escrever as notas das páginas novas (item A), depois commit.
7. **Conferir** o arquivo único (`page_metadata` + miniaturas/export das páginas novas).
8. **Descartar o temporário**: `move-item-to-folder` → `FAHWiiIrtak` (lixeira). O mesmo vale para rascunhos de extração de fotos. **Nenhum design temporário fica fora da lixeira ao fim da tarefa.**
9. **Exportar PNG** do arquivo único (`export-design` com `pages: [...]`) e fatiar panorâmicos em 1080×1350 em `entregas/AAAA-MM-DD_[formato]_[campanha]/` com `LEGENDA.md`.
10. **Registrar** na tabela abaixo (páginas do arquivo único).
11. **Responder** com: link do arquivo único + **páginas** de cada peça, o que ficou editável ou pendente, PNGs, e lembrar de esvaziar a lixeira se ela tiver itens.

**Revisar uma arte já consolidada**: editar direto no arquivo único (abrir transação, editar só a página, commit). Se a API não abrir transação por causa do tamanho, use `copy-design` com `page_numbers` → edite → `merge-designs` (`delete_pages` a antiga + `insert_pages` a nova, em chamadas separadas) → temporário para a lixeira.

**Imagens de parceiros/terceiros**: subir com `upload-asset-from-url` ou `create-upload-url` e aplicar como fill. Uploads feitos pela API caem numa área de uploads do app que às vezes não pode ser movida ("Not allowed to access this folder"). Nesse caso, deixe como está (não aparece como design solto) e registre o mediaId aqui.

**Reaproveitar fotos do mestre**: `update_fill` com um mediaId do mestre falha ("media bundle… not found" / `permission_denied`). Solução: `copy-design` da página com a foto → apagar os outros elementos → exportar JPG 2× → `create-upload-url` → usar o novo mediaId. **Depois mover o rascunho pra lixeira.** Fotos já reenviadas: descoberta `MAHWiYgpK0I`, cosplay M3GAN `MAHWiRiGQCc`, diversão (cabelo verde) `MAHWiXRVEEA`, sobrevivente Once Human `MAHWh9ai7fQ`, carro GWM recortado `MAHWhwiChXc`, logo Once Human `MAHWh4OS6OM`.

**Armadilhas**: `replace_text` em parágrafo de corpo às vezes liga marcador de lista (corrija com `format_text` `list_level: 0`). `merge-designs` aceita só 1 operação por chamada. Nunca editar o mestre sem pedido explícito, nunca apagar páginas do mestre.

### Registro: índice do arquivo único `DAHWihdcqtc`

| Págs. | Peça | Publicação | Legenda |
|---|---|---|---|
| 1 | NXP · Estático · NXP É: Descoberta · v1 | 01/10 12h @nerdexperience | `entregas/2026-10-01_estatico_nxp-e-descoberta/` |
| 2–5 | NXP · Carrossel · TBT NXP · Portal 404 · v1 | 01/10 14h @nerdexperience | `entregas/2026-10-01_carrossel_tbt-nxp/` |
| 6 | NERDVERSO · Carrossel · Tirinha #2 · Rob deixa a PaTech · v1 (panorâmica, 4 slides) | 02/10 12h @nerdverso | `entregas/2026-10-02_carrossel_tirinha-nerdverso-2/` |
| 7 | NXP · Carrossel · Cosplay · Jurado 01 · v1 (panorâmica, 6 slides) | 02/10 16h collab | `entregas/2026-10-02_carrossel_cosplay-jurado-01/` |
| 8 | NXP · Estático · NXP É: Magia · v1 | 03/10 09h @nerdexperience | `entregas/2026-10-03_estatico_nxp-e-magia/` |
| 9–10 | NXP · Carrossel · Ativação Once Human · Padrão · v1 (5 slides em 2 panorâmicas) | [A CONFIRMAR] | `entregas/2026-09-28_carrossel_once-human/` |
| 11 | NXP · Carrossel · Ativação Once Human · Premium · v1 (panorâmica, 4 slides) | [A CONFIRMAR] | `entregas/2026-09-28_carrossel_once-human/premium/` |

Designs individuais antigos (`DAHWiYo_tAw`, `DAHWiYqdMGQ`, `DAHWiVT8S20`, `DAHWiRCztp8`, `DAHWicfBZ1k`, `DAHWhhoHjC8`, `DAHWhgYqm84`) e rascunhos (`DAHWiQHwBso`, `DAHWiZwoy7Q`, `DAHWiXNK4lw`, `DAHWieoOa7M`) foram para a lixeira em 2026-09-29. **Não usar mais.**

Modelos que funcionaram bem: **Ativação/Atração confirmada** (págs. 198 + 204 do mestre) para anúncio informativo; **série "NXP apresenta"** (págs. 286–300, ex.: 292 Tempus) para anúncios premium/colabs, com recorte do personagem/produto sem fundo.

## Referências fixas

| Item | Valor |
|---|---|
| Design mestre | `DAHF08WuL5g` — "NXP Pop Festival" (328 págs.) |
| Brand Kit | "nerd" — `kAGyIHc9_Bg` (conferir se contém as 9 cores, 3 fontes e logos; completar se faltar) |
| Páginas de referência | 2 (cores/fontes/texturas), 3 (logos/ícones/portais), "TEMPLATES", "INTERAÇÃO", "POSTS" |

## Ler / pesquisar

- Texto de páginas: `read-design` com `filter.fields=["design_content"]` e `page_indices=[…]`.
- Miniaturas: `filter.fields=["thumbnails"]`, `thumbnail_pages=[…]` (lotes de até 30 páginas; a resposta é grande).
- Formatos: `filter.fields=["page_metadata"]` (dimensões por página).
- Buscar outros designs: `search-designs` (ex.: "NXP", "Nerd Experience", "Lótus", "Pixel").

## Criar uma peça nova (fluxo seguro)

1. **Escolha o modelo** mais parecido (ver `09-biblioteca-canva.md`) e confirme pela miniatura.
2. **Nunca edite o mestre direto** sem pedir: prefira `copy-design` (cópia do design) ou peça ao usuário para duplicar a página no Canva. Se editar o mestre, abra transação (`read-design` com `open_transaction: true`), edite só a página nova e mostre a miniatura antes de salvar.
3. **Edite o texto** com `edit-design` (substituir strings nos elementos de texto). Mantenha fontes/cores do modelo — só troque conteúdo.
4. **Troque imagens** com `upload-asset-from-url` + `edit-design`; use `remove-background` para recortar convidados.
5. **Revise** com a miniatura e o `13-checklist-qa.md`.
6. **Exporte** com `export-design` (`get-export-formats` antes): PNG para estáticos, MP4 para animados, `pages` só com as páginas novas. Exportar muitas páginas de uma vez pode estourar o tempo: faça lotes de ≤ 40.
7. **Organize**: consolide no arquivo único `DAHWihdcqtc` e mande o temporário pra lixeira (ver PADRÃO, seção B).

## Gerar do zero (quando não há modelo)

- `generate-design-structured` / `generate-design` com um briefing que contenha: formato e medida, modo de cor (portal/neon/mundo), textos exatos com destaque, elementos (portal, blobs, ícones), assinatura (logo + 27 e 28 + Expominas) e **o Brand Kit "nerd"**. Depois ajuste manualmente — o gerador tende a "limpar" demais; reforce granulado, blobs e portal.
- `resize-design` para desdobrar um feed em story/banner (sempre revisar zona segura).

## Comentários e aprovação

- `comment-on-design` para deixar a revisão na própria página ("QA: trocar 'feveriro' → 'fevereiro'").
- `list-comments` / `reply-to-comment` para acompanhar ajustes da equipe.

## Sem MCP?

Entregue a **ficha de produção** (formato, textos por linha com destaque, layout, elementos, legenda) para o designer montar duplicando a página-modelo indicada.
