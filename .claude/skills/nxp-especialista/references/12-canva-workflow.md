# 12 — Fluxo de produção no Canva (com Canva MCP)

Quando o conector **Canva** estiver habilitado na sessão (claude.ai → Configurações → Conectores → Canva; no Claude Code, as ferramentas `mcp__Canva__*`), o especialista pode ler, duplicar, editar e exportar peças.

## ⭐ PADRÃO DE ENTREGA DE ARTES (obrigatório)

Toda arte do NXP é **produzida e deixada no Canva, 100% editável**, pra equipe poder ajustar depois. PNG exportado é complemento, nunca o único entregável.

### A. Onde as artes moram: arquivo de VOLUMES (regra principal)

Todas as artes finais do Instagram ficam no **arquivo de posts NXP 2027**, no mesmo espírito do mestre: 1 página por post/slide ou 1 página panorâmica por carrossel, em ordem cronológica de publicação. **Limite da API do Canva: 100 páginas por design** (testado em 2026-09-29: a inserção que passa de 100 é cortada ou falha com "Failed to commit session"). Por isso o arquivo é dividido em **volumes de até ~95 páginas**:

| Volume | ID | Conteúdo | Link |
|---|---|---|---|
| `NXP 2027 — Posts Instagram · vol. 1` | **`DAHWihdcqtc`** | 01/10 → 19/10 (09h) + Once Human (págs. 96–98) — 98 págs. (**cheio**) | [editar](https://www.canva.com/d/3YOq9S2tH0aBx7d) |
| `NXP 2027 — Posts Instagram · vol. 2` | **`DAHWizfK3FI`** | 19/10 (13h) → 31/10 — 58 págs. (**volume ativo**, cabem ~37) | [editar](https://www.canva.com/d/HDZ3O72Z_bSSGSJ) |

- **Volume ativo** = o último. Nova peça entra nele. Antes de inserir, some as páginas: se passar de ~95, crie o próximo volume (`merge-designs` `create_new_design`, título `NXP 2027 — Posts Instagram · vol. N`), mova pra pasta `FAHWieBU748` e registre nesta tabela. Nunca volte a um design por post.
- Nunca deixe uma peça dividida entre dois volumes.

| Item | Valor |
|---|---|
| Pasta | `NXP 2027 — Posts Instagram` (`FAHWieBU748`) |
| Imagens enviadas (uploads) | subpasta `_assets (imagens enviadas)` (`FAHWirZP1-Q`), quando o Canva deixar mover |
| Lixeira manual | subpasta `🗑️ PARA APAGAR (lixeira)` (`FAHWiiIrtak`) — o usuário esvazia com 1 clique |

**Estrutura final da pasta — nada além disso:**
```
NXP 2027 — Posts Instagram/
├── NXP 2027 — Posts Instagram · vol. 1   ← artes finais (cheio)
├── NXP 2027 — Posts Instagram · vol. 2   ← artes finais (ativo)
├── _assets (imagens enviadas)/
└── 🗑️ PARA APAGAR (lixeira)/              ← temporário; o usuário apaga
```
- **Proibido**: design solto na raiz do Canva, subpasta por campanha, cópias "NXP Pop Festival"/"Cópia de…", `_apoio`, rascunho visível.
- **Índice dentro do volume**: a 1ª página de cada peça leva nas **notas** (`replace_speaker_notes`): `[Nome padrão] — início da peça (N pág.) — publicar DD/MM HHh @perfil (planilha nºX). Legenda: entregas/…/LEGENDA.md`.
- **Nome padrão de cada peça** (notas, registro e pasta de `entregas/`): `NXP · [Formato] · [Campanha/Tema] · [Variação] · v[N]` (perfil NerdVerso: `NERDVERSO · …`).
- **Produção em lote com subagentes**: cada subagente só cria temporários + PNG + LEGENDA e devolve os IDs; **o agente principal** faz os `merge-designs` (um por vez, em ordem), as notas e manda os temporários pra lixeira. Subagente nunca mexe nos volumes.

### B. Fluxo de produção (sem deixar lixo)

A API **não apaga designs nem pastas** e **não passa de 100 páginas por design**. Por isso todo design temporário tem destino obrigatório:

1. **Área de trabalho temporária**: `copy-design` com as páginas-modelo do mestre `DAHF08WuL5g` (1 design temporário por lote). Título já no padrão da peça.
2. **Editar** no temporário: textos, imagens e crop. Manter camadas editáveis: texto como texto, imagens como fill substituível, logos soltos. Nunca achatar em imagem.
3. **Salvar (commit) logo após cada bloco de edições**, porque a conexão MCP pode cair.
4. **QA** pela miniatura + `13-checklist-qa.md`.
5. **Consolidar**: `merge-designs` com `type: modify_existing_design`, `design_id: DAHWihdcqtc`, **uma operação `insert_pages` por chamada** (a API só aceita 1 por vez), com `after_page_number` pra manter a ordem cronológica.
6. **Indexar**: abrir transação no volume e escrever as notas das páginas novas (item A), depois commit.
7. **Conferir** o volume (`page_metadata` + miniaturas/export das páginas novas).
8. **Descartar o temporário**: `move-item-to-folder` → `FAHWiiIrtak` (lixeira). O mesmo vale para rascunhos de extração de fotos. **Nenhum design temporário fica fora da lixeira ao fim da tarefa.**
9. **Exportar PNG** do volume (ou do temporário antes de descartar) (`export-design` com `pages: [...]`) e fatiar panorâmicos em 1080×1350 em `entregas/AAAA-MM-DD_[formato]_[campanha]/` com `LEGENDA.md`.
10. **Registrar** no índice abaixo (volume + páginas) e atualizar a linha `Canva` da `LEGENDA.md`.
11. **Responder** com: link do volume + **páginas** de cada peça, o que ficou editável ou pendente, PNGs, e lembrar de esvaziar a lixeira se ela tiver itens.

**Revisar uma arte já consolidada**: editar direto no volume (abrir transação, editar só a página, commit). Se a API não abrir transação por causa do tamanho, use `copy-design` com `page_numbers` → edite → `merge-designs` (`delete_pages` a antiga + `insert_pages` a nova, em chamadas separadas) → temporário para a lixeira.

**Imagens de parceiros/terceiros**: subir com `upload-asset-from-url` ou `create-upload-url` e aplicar como fill. Uploads feitos pela API caem numa área de uploads do app que às vezes não pode ser movida ("Not allowed to access this folder"). Nesse caso, deixe como está (não aparece como design solto) e registre o mediaId aqui.

**Reaproveitar fotos do mestre**: `update_fill` com um mediaId do mestre falha ("media bundle… not found" / `permission_denied`). Solução: `copy-design` da página com a foto → apagar os outros elementos → exportar JPG 2× → `create-upload-url` → usar o novo mediaId. **Depois mover o rascunho pra lixeira.** Fotos já reenviadas: descoberta `MAHWiYgpK0I`, cosplay M3GAN `MAHWiRiGQCc`, diversão (cabelo verde) `MAHWiXRVEEA`, sobrevivente Once Human `MAHWh9ai7fQ`, carro GWM recortado `MAHWhwiChXc`, logo Once Human `MAHWh4OS6OM`. Do mestre (lote C1, out/2026): vampiro `MAHWiqMa4s4` (pág. 156), Macaco Louco `MAHWikkyhGg` (190), piratas NXP 2023 `MAHWii4rUjE` (268), Deadpool `MAHWiqVg4jM` (241), Ahri+2B `MAHWisgWOyc` (245), Garnet `MAHWis9Vaos` (244), Nilou `MAHWinXC1AA` (249), família Batman `MAHWilY4haU` (232), pai e filho videogame `MAHWiqewOhA` (311), família Aranha `MAHWig0WQe4` (311), pai e filho Homem-Aranha `MAHWivyJq7g` (314), card game `MAHWiswrI3Q` (237), visitante com cão `MAHWimu-Vz4` (214), gamer `MAHWimVc3wI` (242). **Evite repetir foto em peças próximas.**

**Armadilhas**: `replace_text` em parágrafo de corpo às vezes liga marcador de lista (corrija com `format_text` `list_level: 0`). `merge-designs` aceita só 1 operação por chamada. Nunca editar o mestre sem pedido explícito, nunca apagar páginas do mestre.

### Registro: índice dos volumes

| Vol. | Págs. | nº planilha | Peça | Publicação | Pasta em entregas/ |
|---|---|---|---|---|---|
| 1 | 1 | — | NXP · Estático · NXP É: Descoberta · v1 | 01/10 12h | `2026-10-01_estatico_nxp-e-descoberta/` |
| 1 | 2–5 | — | NXP · Carrossel · TBT NXP · Portal 404 · v1 | 01/10 14h | `2026-10-01_carrossel_tbt-nxp/` |
| 1 | 6 | — | NERDVERSO · Carrossel · Tirinha #2 · Rob deixa a PaTech · v1 | 02/10 12h | `2026-10-02_carrossel_tirinha-nerdverso-2/` |
| 1 | 7 | — | NXP · Carrossel · Cosplay · Jurado 01 · v1 | 02/10 16h | `2026-10-02_carrossel_cosplay-jurado-01/` |
| 1 | 8 | — | NXP · Estático · NXP É: Magia · v1 | 03/10 09h | `2026-10-03_estatico_nxp-e-magia/` |
| 1 | 9 | 11 | NXP · Estático · Contagem Regressiva · Faltam 4 Meses · v1 | 03/10 13h | `2026-10-03_estatico_faltam-4-meses/` |
| 1 | 10 | 12 | NXP · Estático · Caça-palavras · Já passou pelo NerdXP · v1 | 03/10 15h | `2026-10-03_estatico_caca-palavras/` |
| 1 | 11 | 14 | NERDVERSO · Carrossel · Bíblia do NerdVerso · v1 | 03/10 17h | `2026-10-03_carrossel_biblia-do-nerdverso/` |
| 1 | 12–17 | 13 | NXP · Carrossel · Guia do Explorador · Tudo que já sabemos do NXP 2027 · v1 | 03/10 17h | `2026-10-03_carrossel_tudo-que-ja-sabemos/` |
| 1 | 18–21 | 16 | NERDVERSO · Carrossel · Repost Teorias da Semana · Template · v1 | 04/10 20h | `2026-10-04_carrossel_repost-teorias-template/` |
| 1 | 22 | 17 | NERDVERSO · Estático · Segundou · v1 | 05/10 09h | `2026-10-05_estatico_segundou/` |
| 1 | 23 | 18 | NXP · Estático · Dia das Crianças · Teaser · v1 | 05/10 09h | `2026-10-05_estatico_dia-das-criancas-teaser/` |
| 1 | 24 | 19 | NERDVERSO · Carrossel · Dr. Pat e a PaTech · v1 | 05/10 10h | `2026-10-05_carrossel_dr-pat-e-a-patech/` |
| 1 | 25 | 20 | NERDVERSO · Estático · NXP É: Diversão · v1 | 05/10 11h | `2026-10-05_estatico_nxp-e-diversao/` |
| 1 | 26 | 21 | NXP · Estático · Serviço · Local Expominas nave pousando · v1 | 05/10 13h | `2026-10-05_estatico_local-expominas-nave/` |
| 1 | 27 | 24 | NXP · Carrossel · Atrações Confirmadas · Feh Dubs + Gaveta · v1 | 06/10 11h | `2026-10-06_carrossel_atracoes-feh-dubs-gaveta/` |
| 1 | 28 | 26 | NERDVERSO · Carrossel · NXP apresenta: Jhon · v1 | 07/10 09h | `2026-10-07_carrossel_nxp-apresenta-jhon/` |
| 1 | 29 | 27 | NXP · Carrossel · Next Level · Credencial Colecionável · v1 | 07/10 13h | `2026-10-07_carrossel_next-level-credencial/` |
| 1 | 30–31 | 28 | NXP · Carrossel · Quiz de Mundo · Em qual mundo você viveria · v1 | 07/10 17h | `2026-10-07_carrossel_quiz-mundo-nerdverso/` |
| 1 | 32–34 | 29 | NXP · Carrossel · Atração · Feh Dubs Curiosidades · v1 | 08/10 13h | `2026-10-08_carrossel_feh-dubs-curiosidades/` |
| 1 | 35 | 30 | NERDVERSO · Carrossel · Arquivo Nerd · Objetos confiscados · v1 | 08/10 13h | `2026-10-08_carrossel_arquivo-nerd-objetos-confiscados/` |
| 1 | 36 | 32 | NERDVERSO · Carrossel · Tirinha #3 · O primeiro dia de um explorador · v1 | 09/10 | `2026-10-09_carrossel_tirinha-nerdverso-3/` |
| 1 | 37–43 | 33 | NXP · Carrossel · Guia do Explorador · O que levar na mochila · v1 | 10/10 13h | `2026-10-10_carrossel_mochila/` |
| 1 | 44 | 34 | NXP · Estático · NXP É: Descoberta · v2 | 10/10 21h | `2026-10-10_estatico_nxp-e-descoberta-v2/` |
| 1 | 45–50 | 35 | NXP · Carrossel · NXP É: Família · Cosplay em família · v1 | 11/10 09h | `2026-10-11_carrossel_nxp-e-familia/` |
| 1 | 51–57 | 36 | NXP · Carrossel · Guia do Explorador · Primeiro NXP 5 coisas · v1 | 11/10 13h | `2026-10-11_carrossel_primeiro-nxp/` |
| 1 | 58 | 37 | NERDVERSO · Estático · Fan Art da Semana · Template · v1 | 11/10 13h | `2026-10-11_estatico_fan-art-da-semana-template/` |
| 1 | 59–64 | 38 | NXP · Carrossel · Dia das Crianças · A criança nerd em você · v1 | 12/10 09h | `2026-10-12_carrossel_dia-das-criancas/` |
| 1 | 65–71 | 39 | NXP · Carrossel · Guia do Explorador · Famílias e grupos · v1 | 12/10 11h | `2026-10-12_carrossel_familias-grupos/` |
| 1 | 72 | 41 | NERDVERSO · Carrossel · O que vai rolar no NXP · Guia do Rob · v1 | 12/10 21h | `2026-10-12_carrossel_o-que-vai-rolar-guia-do-rob/` |
| 1 | 73–78 | 43 | NXP · Carrossel · Serviço · Como acompanhar os anúncios · v1 | 13/10 14h | `2026-10-13_carrossel_acompanhar-anuncios/` |
| 1 | 79 | 44 | NXP · Carrossel · Atração NXP · Feh Dubs Personagens Marcantes · v1 | 13/10 21h | `2026-10-13_carrossel_feh-dubs-personagens/` |
| 1 | 80 | 46 | NERDVERSO · Carrossel · Apresentando um mundo: Pixel · v1 | 14/10 09h | `2026-10-14_carrossel_mundo-pixel/` |
| 1 | 81–86 | 49 | NXP · Carrossel · Serviço · FAQ rápido · v1 | 15/10 17h | `2026-10-15_carrossel_faq-rapido/` |
| 1 | 87 | 50 | NERDVERSO · Carrossel · Arquivo Nerd · Mapa censurado · v1 | 15/10 17h | `2026-10-15_carrossel_arquivo-nerd-mapa-censurado/` |
| 1 | 88–94 | 51 | NXP · Carrossel · Guia do Explorador · Mini kit de reparo cosplay · v1 | 17/10 13h | `2026-10-17_carrossel_kit-reparo-cosplay/` |
| 1 | 95 | 54 | NERDVERSO · Carrossel · Tempus: como surgiram os poderes · v1 | 19/10 09h | `2026-10-19_carrossel_tempus-poderes/` |
| 1 | 96–97 | — | NXP · Carrossel · Ativação Once Human · Padrão · v1 | [A CONFIRMAR] | `2026-09-28_carrossel_once-human/` |
| 1 | 98 | — | NXP · Carrossel · Ativação Once Human · Premium · v1 | [A CONFIRMAR] | `2026-09-28_carrossel_once-human/premium/` |
| 2 | 1–6 | 55 | NXP · Carrossel · Guia do Explorador · Atrações simultâneas · v1 | 19/10 13h | `2026-10-19_carrossel_atracoes-simultaneas/` |
| 2 | 7 | 56 | NERDVERSO · Carrossel · Lore Drop · Eldarion: 3 regras · v1 | 19/10 17h | `2026-10-19_carrossel_lore-drop-eldarion-regras/` |
| 2 | 8–13 | 58 | NXP · Carrossel · NXP Serviço · Organize com antecedência · v1 | 20/10 13h | `2026-10-20_carrossel_organize-com-antecedencia/` |
| 2 | 14 | 59 | NXP · Carrossel · Nerd de A a Z · A de Anime · v1 | 20/10 | `2026-10-20_carrossel_nerd-de-a-a-z-anime/` |
| 2 | 15–20 | 60 | NXP · Carrossel · Guia do Explorador · Bateria do celular · v1 | 21/10 13h | `2026-10-21_carrossel_bateria-do-celular/` |
| 2 | 21–26 | 61 | NXP · Carrossel · Guia do Explorador · Ponto de encontro (collab NerdVerso) · v1 | 24/10 13h | `2026-10-24_carrossel_ponto-de-encontro/` |
| 2 | 27–32 | 63 | NXP · Carrossel · Guia do Explorador · Fotos de cosplayers · v1 | 25/10 13h | `2026-10-25_carrossel_fotos-de-cosplayers/` |
| 2 | 33–38 | 65 | NXP · Carrossel · NXP É: Magia · Cosplays · v1 | 26/10 13h | `2026-10-26_carrossel_nxp-e-magia/` |
| 2 | 39 | 66 | NERDVERSO · Carrossel · Lore Drop · Protocolo N.E.R.D. para criaturas · v1 | 26/10 21h | `2026-10-26_carrossel_lore-drop-protocolo-nerd/` |
| 2 | 40–45 | 67 | NXP · Carrossel · Guia do Explorador · Sobreviver fantasiado · v1 | 28/10 13h | `2026-10-28_carrossel_sobreviver-fantasiado/` |
| 2 | 46–51 | 68 | NXP · Carrossel · TBT NXP · Vilões e Monstros · v1 | 29/10 21h | `2026-10-29_carrossel_tbt-viloes/` |
| 2 | 52–58 | 69 | NXP · Carrossel · Guia do Explorador · Halloween no NerdVerso · v1 | 31/10 13h | `2026-10-31_carrossel_halloween-nerdverso/` |

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
7. **Organize**: consolide no volume ativo e mande o temporário pra lixeira (ver PADRÃO, seções A e B).

## Gerar do zero (quando não há modelo)

- `generate-design-structured` / `generate-design` com um briefing que contenha: formato e medida, modo de cor (portal/neon/mundo), textos exatos com destaque, elementos (portal, blobs, ícones), assinatura (logo + 27 e 28 + Expominas) e **o Brand Kit "nerd"**. Depois ajuste manualmente — o gerador tende a "limpar" demais; reforce granulado, blobs e portal.
- `resize-design` para desdobrar um feed em story/banner (sempre revisar zona segura).

## Comentários e aprovação

- `comment-on-design` para deixar a revisão na própria página ("QA: trocar 'feveriro' → 'fevereiro'").
- `list-comments` / `reply-to-comment` para acompanhar ajustes da equipe.

## Sem MCP?

Entregue a **ficha de produção** (formato, textos por linha com destaque, layout, elementos, legenda) para o designer montar duplicando a página-modelo indicada.
