# 12 — Fluxo de produção no Canva (com Canva MCP)

Quando o conector **Canva** estiver habilitado na sessão (claude.ai → Configurações → Conectores → Canva; no Claude Code, as ferramentas `mcp__Canva__*`), o especialista pode ler, duplicar, editar e exportar peças.

## ⭐ PADRÃO DE ENTREGA DE ARTES (obrigatório)

Toda arte do NXP é **produzida e deixada no Canva, 100% editável**, pra equipe poder ajustar depois. PNG exportado é complemento, nunca o único entregável.

1. **Sempre montar no Canva** a partir de uma cópia (`copy-design` com as páginas-modelo do mestre `DAHF08WuL5g`). Nunca gerar a arte final fora do Canva (HTML/PIL) nem "achatar" em imagem única.
2. **Manter camadas editáveis**: textos como texto (fonte da marca), imagens como molduras/fills substituíveis, logos e ícones como elementos soltos. Não rasterizar, não agrupar tudo, não usar imagem com texto embutido.
3. **Nome do design**: `NXP · [Formato] · [Campanha/Tema] · [Variação] · v[N]`
   - ex.: `NXP · Carrossel · Ativação Once Human · Premium (4 slides) · v1`, `NXP · Story · 2º Lote · v2`
4. **Pasta**: `NXP 2027 — Posts Instagram` (`FAHWieBU748`) → subpasta da campanha `AAAA-MM · [Campanha]` (criar com `create-folder` se não existir; conferir antes com `search-folders`).
5. **Imagens de parceiros/terceiros**: subir pro Canva (`upload-asset-from-url` ou `create-upload-url`) e aplicar como fill — assim a equipe troca pela versão final com 1 clique ("Substituir").
6. **Salvar (commit) logo após cada bloco de edições** — a conexão MCP pode cair e transações abertas se perdem.
7. **Exportar PNG** (fatiar carrossel panorâmico em 1080×1350) e salvar em `entregas/AAAA-MM-DD_[formato]_[campanha]/` com `LEGENDA.md`.
8. **Na resposta ao usuário, sempre informar**: nome do design, **link de edição do Canva**, link da pasta e o que ficou editável/pendente (ex.: "foto do carro é placeholder — substitua a imagem do slide 3").
9. **Nunca editar o design mestre** sem pedido explícito; nunca apagar páginas.

### Registro de designs entregues

| Data | Design | ID | Pasta |
|---|---|---|---|
| 2026-09-28 | NXP · Carrossel · Ativação Once Human · Padrão (5 slides) · v1 | `DAHWhhoHjC8` | 2026-10 · Ativação Once Human (`FAHWiUmhNrg`) |
| 2026-09-29 | NXP · Carrossel · Ativação Once Human · Premium (4 slides) · v1 | `DAHWhgYqm84` | 2026-10 · Ativação Once Human (`FAHWiUmhNrg`) |

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
7. **Organize**: `create-folder` "NXP 2027 / [mês] / [campanha]" e `move-item-to-folder`.

## Gerar do zero (quando não há modelo)

- `generate-design-structured` / `generate-design` com um briefing que contenha: formato e medida, modo de cor (portal/neon/mundo), textos exatos com destaque, elementos (portal, blobs, ícones), assinatura (logo + 27 e 28 + Expominas) e **o Brand Kit "nerd"**. Depois ajuste manualmente — o gerador tende a "limpar" demais; reforce granulado, blobs e portal.
- `resize-design` para desdobrar um feed em story/banner (sempre revisar zona segura).

## Comentários e aprovação

- `comment-on-design` para deixar a revisão na própria página ("QA: trocar 'feveriro' → 'fevereiro'").
- `list-comments` / `reply-to-comment` para acompanhar ajustes da equipe.

## Sem MCP?

Entregue a **ficha de produção** (formato, textos por linha com destaque, layout, elementos, legenda) para o designer montar duplicando a página-modelo indicada.
