---
name: mobox-criar-post
description: Cria posts, carrosséis e stories de Instagram da MOBOX Produções (@moboxproducoes) — vagas/trabalhe conosco, institucionais, "você sabia?", serviços, M.AG — do briefing (texto, áudio ou conversa) até a arte pronta no Canva e a legenda. Use sempre que o pedido envolver Mobox, MOBOX Produções, M.AG by Mobox, "produzindo o impossível", post de vaga da Mobox, ou o Canva "Mobox - Posts". Não use para o Nerd Experience (NXP), que tem skills próprias.
---

# Criar post MOBOX

Antes de começar, leia `references/aprendizados.md`: são as correções que a equipe já fez em entregas anteriores e valem como regra.

## Passo 1 — Briefing

O briefing pode chegar como texto, áudio (conversa gravada) ou print.

- **Áudio**: transcreva com `faster-whisper` (modelo `medium`, `language="pt"`). Converta antes para WAV mono 16 kHz com `ffmpeg` (o `av` do container quebra com `.m4a`). Extraia só os fatos; piadas e comentários internos ficam de fora da arte (ex.: "paga um Claude Max" não vira benefício).
- Pergunte só o que faltar e for bloqueante. O que não for informado (salário, modalidade, local, prazo) fica fora da arte e vira pendência na entrega, nunca inventado.

## Passo 2 — Referência visual

1. O perfil do Instagram costuma bloquear acesso automático (HTTP 429). A fonte confiável dos posts publicados é o Canva **"Mobox - Posts"** (`DAGQIT9UKTY`). Veja `references/canva.md`.
2. Ache um post do mesmo tipo e use a página dele como modelo. Nunca desenhe do zero se existe modelo.

## Passo 3 — Montagem no Canva

1. `copy-design` só da página-modelo → design novo e independente (o original fica intacto).
2. Renomeie: `Mobox - [Tipo] [Assunto]` (ex.: `Mobox - Vaga de trabalho em IA e Automação`).
3. Edite os textos com `find_and_replace_text` quando o bloco tem várias cores (preserva o estilo de cada trecho); `replace_text` achata a formatação e às vezes liga `listLevel: 1` e muda o tamanho da fonte — corrija com `format_text` (`list_level: 0`, tamanho original).
4. **Bullets são imagens separadas do texto.** Depois de trocar o texto, realinhe cada ícone com a 1ª linha do seu item (e agrupe os ícones). Itens novos precisam de ícone novo; itens removidos levam o ícone junto. Nunca deixe ícone órfão.
5. Confira cada slide na miniatura e, se houver dúvida de quebra de linha, exporte PNG para ver em tamanho real.
6. Mostre a prévia e peça aprovação. Ao aprovar ("quero o novo", "salva", "pode subir"), faça `commit` na hora: o link do Canva só mostra a versão nova depois de salvar.
7. Entregue o link de edição retornado pelo Canva depois do commit.

## Passo 4 — Legenda

Tom da marca (ver `references/identidade.md`): direto, frases curtas, 1 emoji por bloco no máximo, CTA claro (link da bio), fechar com hashtags incluindo `#mobox #produzindooimpossivel`.

## Passo 5 — Entrega

- Link do Canva + prévia.
- Legenda pronta para colar.
- Lista curta de pendências (ex.: atualizar o formulário da bio, salário/modalidade não definidos).
- Carrossel montado como página única larga (5400×1350 = 5 slides de 1080×1350): avise que precisa fatiar em 5 imagens ou ofereça exportar já separado.

## Passo 6 — Aprender com as alterações da equipe

Quando o usuário editar a arte e pedir para você "ver o que mudou":
1. Leia o design (`read-design` com `design_content`) e compare com o que você entregou, elemento por elemento (texto, posição, elementos removidos/adicionados).
2. Explique cada mudança e o porquê provável.
3. Aponte o que parece inacabado (texto terminando em vírgula, ícone sem texto, título que ficou inconsistente com outro slide) e ofereça corrigir.
4. Registre as regras novas em `references/aprendizados.md` (data, peça, regra, exemplo antes → depois).
5. Se abrir transação só para ler, feche com `cancel`.
