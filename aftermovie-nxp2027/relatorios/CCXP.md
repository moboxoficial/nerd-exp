# CCXP — Análise de aftermovies e recaps no Instagram (para o NXP)

Data da análise: 30/09/2026. Analista: Claude (a pedido da produção NXP).
Material: 6 vídeos oficiais baixados do Instagram (via /embed), analisados com `analyze.py` (planos, cor, áudio) e **leitura visual de todas as contact sheets**, além de frames extras e faixas de legenda extraídas.

> **Limitações (com honestidade):**
> - **CCXP23 (edição de 10 anos): não consegui analisar.** O aftermovie existe no YouTube oficial (`youtube.com/watch?v=cpddyr7pGMY`, 2:40, publicado em 07/03/2024), mas o YouTube bloqueou o download neste ambiente (erro 403 e "confirme que não é um robô"; Piped e Invidious também falharam). Não achei o reel equivalente no Instagram.
> - Instagram não permite listar o perfil. As URLs vieram de buscas restritas a instagram.com, e **pode existir um aftermovie de CCXP25 mais longo que não encontrei**. O mais próximo foi o reel de encerramento (22 s).
> - **Não ouço o áudio.** Tudo o que digo sobre fala e narração vem das **legendas embutidas** e da curva de loudness. BPM e "cortes no beat" são estimativas automáticas.
> - "Plays" = `video_view_count` do embed no dia da coleta. São aproximados.

---

## 1. Vídeos analisados

| # | Vídeo | URL | Publicação (aprox.) | Duração | Formato | Plays | Papel |
|---|---|---|---|---|---|---|---|
| A | **Aftermovie CCXP24** "Nossos mundos vão se encontrar novamente" | https://www.instagram.com/reel/DHwc_aGR0Se/ | fim de mar/2025 (no YouTube em 29/03/2025) | 2:35,7 | **16:9 horizontal** 1276×720, 23,98 fps | ~46 mil | Aftermovie "cinema" que abre a pré-venda |
| B | **"Anatomia de uma CCXP"** (venda CCXP25) | https://www.instagram.com/reel/DIRMisjxqXk/ | abr/2025 (no YouTube em 09/04/2025, **388 mil views**) | 1:11,4 | 9:16, 720×1280 | ~14 mil | Recap/manifesto de marca com arquivo de várias edições + CTA de vendas |
| C | **Encerramento CCXP25** "Obrigada por mais uma edição…" | https://www.instagram.com/reel/DSA0IAYEVm4/ | dez/2025 (logo após o evento) | 0:22 | 9:16, 720×1280, 24 fps | **~68 mil, 886 comentários** | Recap imediato + anúncio da data da CCXP26 |
| D | **CCXP México** "¡Vive la locura de #CCXPMX25!" (@ccxp_mx) | https://www.instagram.com/reel/DIe3L5DspPU/ | abr/2025 (antes da MX25, com imagens da MX24) | 0:26,4 | 9:16, 360×640 (baixa resolução no embed) | ~2,3 mil | Aftermovie-teaser de vendas |
| E | CCXP MX "Mais que uma Comic Con" (no @ccxpoficial) | https://www.instagram.com/reel/DB_7Q4Xx5Uc/ | nov/2024 | 0:24,3 | 9:16, 360×640 | ~37 mil | Anúncio da data com recap curto |
| F | Teaser "CCXP26 É AMANHÃ! Abertura de vendas" | https://www.instagram.com/reel/DZX8ukvKgN2/ | jun/2026 | 0:06,4 | **4:5** 720×900, **sem áudio** | ~38 mil | Lembrete de venda (fotos em stop-motion) |

Arquivos: `$S/competidores/ccxp/` (mp4, `*.meta.json`, `an_*/summary|color|audio.json`, `an_*/sheet_XX.jpg`, `x24_sheet.jpg`, `subs24.jpg`, `x25v_sheet.jpg`, `x25e.jpg`, `xmx_af.jpg`, `xmx.jpg`, `x26.jpg`).

### Métricas técnicas (analyze.py)

| | A CCXP24 | B Anatomia | C Encerr. 25 | D MX | E MX anúncio | F teaser 26 |
|---|---|---|---|---|---|---|
| Nº de planos | 142 | 112 | 84 | 3* | 10 | 7 |
| Plano médio | 1,10 s | 0,64 s | **0,26 s** | n/a* | 2,43 s | 0,91 s |
| Ritmo por quinto (plano médio) | 1,3 / 0,92 / **0,62** / 1,2 / 2,59 | **0,42** / 0,65 / 0,53 / 0,49 / 3,57 | 2,2 / 1,1 / 0,15 / **0,11** / 0,37 | – | 2,4 / 1,6 / 0,7 / 4,9 / 4,9 | – |
| BPM estimado | 99 | 129 | 112 | 172 (talvez 86) | 123 | sem áudio |
| Cortes no beat | 45% | 38% | 36% | – | 22% | – |
| Saturação média | 0,50 | 0,30 | 0,47 | 0,47 | 0,32 | 0,32 |
| Brilho médio | 0,40 (escuro) | 0,53 | 0,49 | 0,29 | 0,23 | 0,52 |
| Temperatura (R–B) | 0,00 neutro | +0,05 | **+0,14 quente** | +0,03 | 0,00 | +0,09 |

*No D, o detector de cortes falhou porque o vídeo é uma colagem de 2 a 4 vídeos simultâneos com texto por cima. Olhando os frames, o ritmo real é alto.

---

## 2. Análise por vídeo

### A. Aftermovie CCXP24 (2:35, horizontal) — o "filme"

**Conceito:** a CCXP como **multiverso/portal**. Um narrador em voz over, com legenda amarela em itálico, conduz a história como se fosse uma convocação de "viajantes", e fecha com uma mesa de RPG que "aponta" para a próxima edição.

**Roteiro com timestamps (texto das legendas embutidas):**

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:04 | **Hook** | **FPV/drone com um boneco do Goku "voando"** em primeiro plano sobre a fachada e o estacionamento do São Paulo Expo e mergulhando na fila. Sem texto nos 3 primeiros segundos, e o impacto vem da imagem. |
| 0:04–0:10 | Convocação | Cosplays na fila olham para a câmera e fazem careta (Furiosa, Eggman com Sonic, Mandrake). VO: *"Atenção, viajantes de todos os universos…"* / *"Este é o chamado final."* |
| 0:10–0:19 | Portal | Close do Olho de Agamotto brilhando num cosplay de Doutor Estranho, que **abre um portal com VFX de faíscas** (0:13,9). *"O portal está aberto." "Nosso destino?" "Um lugar onde mundos se encontram."* |
| 0:19–0:57 | Desenvolvimento 1: entrada no evento | Pavilhão, estandes (Prime Video, Apple TV+), Árvore de Todos os Mundos, palcos com lasers vermelhos (Palco Thunder), celebridades no palco, fãs com cartaz ("NORMAN, I'M A ZOMBIE"), ativações (dragão cuspindo fogo, túnel neon "A primeira vez a gente nunca esquece", dinossauro animatrônico), sessão de *A Roda do Tempo* com **flash branco de transição** (0:57,5). |
| 0:57–1:12 | Virada de tom: manifesto | *"O que é viver o épico pra você? É dançar como se nada mais existisse? Testemunhar o nascimento de um universo? Das muralhas do Magic Market aos gritos do Palco Thunder, seguimos… vivendo o épico."* **É o trecho mais rápido do vídeo (plano médio de 0,62 s entre 1:02 e 1:33).** Montagem de um plano por palavra, no beat. |
| 1:12–1:55 | Desenvolvimento 2: estrelas e estandes | Sonoras curtas de celebridades como pontuação: *"Nós amamos vocês!"* (1:14), *"E aí, Brasil!"* (1:45), *"Eu amo o Brasil!"* (1:47), *"Vocês são incríveis!"* (1:48), *"CCXP 24!"* (1:52). Passeio pelos estandes (Porta dos Fundos, Xbox, Max, Roku, Paramount+ com "Dexter"), Artists' Alley, autógrafos, fãs chorando com Funko na mão. |
| 1:55–2:05 | **Clímax** | Chuva de papel picado sobre a plateia (1:59), pirotecnia de faíscas no palco (2:02), elenco no palco. |
| 2:06 | Respiro | Plano geral escuro do auditório com o logo CCXP24 no telão. Queda de loudness. |
| 2:08–2:25 | **Epílogo** | Mestre de RPG, jogadores e um D20 no tabuleiro. *"Que bela jornada fizemos até aqui." "As possibilidades continuam infinitas." "Mas uma coisa é certa…" "Nossos mundos voltarão a se encontrar."* **Light leak/flash** (2:18). O mestre atravessa um portal com o letreiro **CCXP25** (2:25). |
| 2:30–2:35 | **Cartela/CTA** | Logo CCXP com glow amarelo + "É festival. É evento. É multiverso. É cultura pop." + **"De 4 a 7 de dezembro • ccxp.com.br"**. |

- **Tipos de plano:** FPV/drone (hook), aberto de multidão e fila, close de cosplay olhando para a lente, reação de público (grito, choro, braços para cima), palco e painel com celebridade (muitos), estandes e ativações de marca, Artists' Alley, gaming. Tudo em estabilizador/gimbal com lente clara (fundo desfocado). Tem pouco POV bruto e poucos bastidores.
- **Cor:** contraste alto, pretos profundos, luz de palco saturada (magenta, azul, vermelho) e dia neutro e limpo. Look "cinema digital" sem LUT autoral forte. É o mais escuro do conjunto (brilho 0,40).
- **Motion graphics:** só legendas amarelas em itálico e a cartela final. **Nenhum número** (público, área, painéis).
- **VFX:** portal de faíscas (0:13), flashes e light leaks de transição (0:57, 2:18), lens flare de palco.
- **Áudio:** trilha orquestral/épica de trailer (~99 BPM) com loudness quase constante (-18 dB) e respiros em 0:09, 0:15, 1:03, 1:10 e 2:06–2:13. Voz over de narrador, sonoras de celebridades e som de plateia. A legenda do post invoca o "hino" da plateia (ÔÔÔÔ-ôôôô).
- **Legenda do post:** *"Esto-ÔÔÔÔÔôôôô…u pronta pra mais uma. Sobe o hino da CCXP. ✏️🗓️ Pré-venda disponível dia 31/03 e Abertura de Vendas para o público dia 09/04."* Promete pertencimento (o hino) e dá as datas de venda.
- **Patrocínio:** só orgânico, no cenário (Palco Thunder by Claro tv+, Palco Omelete by Banco do Brasil, estandes dos streamings). Não há cartela de patrocinador.

### B. "Anatomia de uma CCXP" (1:11, vertical) — o manifesto de marca

**Conceito:** um "dossiê" da CCXP com **arquivo de várias edições** (Keanu Reeves, Zendaya e Austin Butler, Gal Gadot com o telão de *WW84*, Will Smith, Giancarlo Esposito, Anya Taylor-Joy, Chris Hemsworth, Bella Ramsey etc.). **É a peça de maior alcance da CCXP no YouTube (388 mil views)**, o que sugere mídia paga.

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:01 | **Hook** | Flash de projetor/lente num fundo escuro com grão, estourando em branco de película (0:00,4). |
| 0:01–0:04 | Título | "A N A T O M I A" em letras espaçadas vira **"ANATOMIA DE UMA CCXP"** sobre closes de estrelas (Esposito, Zendaya, Keanu), com moldura arredondada tipo película/Polaroid e grão pesado em sépia/P&B. |
| 0:04–0:08 | Público | Fãs gritando, criança sorrindo, cosplay chorando, Coringa: **o fã tratado com o mesmo peso da estrela**. |
| 0:08–0:10 | **Stutter** | Esposito no palco com sabre de luz e **cortes a cada 2–3 frames** (freeze/strobe), preto e **silhueta de papel branco recortado** (0:09,6) como transição. |
| 0:10–0:35 | Colagem | Will Smith gritando em P&B com **máscara de papel** (0:12,7), **colagem de papel rasgado** em fundo rosa, roxo, amarelo e verde (0:13–0:25), Gal Gadot recortada com fundo roxo, telões, ewoks, Anya Taylor-Joy, cosplay mirim de Leia, **círculos de mira desenhados** (0:33). |
| 0:35–0:45 | Detalhe | Manopla do Infinito colorida que vira P&B com contorno branco (0:35), autógrafo (split em 3), cosplay de Kuzco em stop-motion com borda de sticker (0:37–0:38), cabeça de cavalo, pai e filha em cosplay. |
| 0:46–0:49 | **Taxonomia tipográfica** | Palavras gigantes no beat: **FILME / SÉRIE / QUA-DRI-NHO / ANIME / COSPLAY**. É a mesma lista da descrição do post ("É filme, série, quadrinho, anime, cosplay…"). |
| 0:49–0:57 | **Clímax** | Palcos, Sandra Oh, Game of Thrones, Crunchyroll, WW84, e **mural em grade de celebridades** sobre fundo azul-claro (0:54,7–0:57) que vai se preenchendo. |
| 0:57–0:59 | Emoção | Sabre de luz, fã sorrindo, **fã chorando** (0:58,9). Emoção sempre no fim. |
| 0:59–1:01 | Papel picado | Plateia com confete (0:59,5). |
| 1:01–1:11 | **CTA** | Logo CCXP com texto datilografado "É MULTI…" que vira **"É CULTURA POP."**, selo "4 a 7 de DEZ", **"VENDAS ABERTAS / CORRA E GARANTA SEU INGRESSO / ccxp.com.br"**. O áudio faz fade até o silêncio (1:07–1:11). |

- **Ritmo:** o mais rápido dos longos (0,64 s). Abre em alta (0,42 s no primeiro quinto) e mantém até o fim, sem curva de filme. Tem 10 s de cartela no final (14% do vídeo).
- **Cor e look:** **vintage/scrapbook**. Saturação baixa (0,30), sépia e P&B, grão de película, bordas arredondadas, papel creme. Blocos de cor chapada (rosa, amarelo, roxo, verde-água) aparecem só nas colagens. É um look autoral e bem reconhecível.
- **VFX e motion:** recortes de papel, torn paper, stickers com contorno branco, stop-motion de fotos, split-screen, typewriter, kinetic type, grão e película.
- **Áudio:** faixa pop/eletrônica a ~129 BPM, sem voz over aparente. Os fades para o silêncio marcam início e fim.
- **Legenda:** *"A venda de ingressos pra #CCXP já começou, junte-se ao maior… festival? Evento? Multiverso? Bom, chame do que quiser, desde que você se sinta em casa. Corra no link da bio…"* Promete pertencimento ("se sinta em casa") e a escala ("o maior").

### C. Encerramento CCXP25 (22 s) — o recap relâmpago (o de maior engajamento)

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:02 | **Hook** | Letreiro gigante **CCXP25** amarelo e magenta na entrada, com a fila embaixo. A marca e a escala aparecem no primeiro frame. |
| 0:02–0:05 | Mensagem | Plano alto da fila e depois da plateia do palco com o texto **"NOSSOS MUNDOS VÃO SE ENCONTRAR NOVAMENTE…"** (fonte bold branca centralizada, safe zone de Reels). |
| 0:05–0:11 | **Escala** | 4–5 planos longos, altos, em movimento (drone indoor/grua) sobre corredores lotados. A multidão é a protagonista. O **áudio fica baixo (-25 a -32 dB)**, construindo tensão. |
| 0:11–0:15,5 | **DROP e "face cascade"** | O loudness sobe para -12 dB e começa uma **sequência de ~55 retratos frontais (2 frames cada, ~12 fps), com olhos alinhados no mesmo ponto da tela**: fãs comuns, cosplays (Pennywise, Ghostface natalino, Master Chief, Deadpool, Loki, Chaves) e fãs sem fantasia. O efeito é hipnótico e cada um vira "eu estava lá". |
| 0:15,5–0:16,4 | Colecionáveis | A mesma cascata com rostos de estátuas (Batman, Hellboy, Deadpool, Obi-Wan, Fera, Loki, Wolverine). |
| 0:16,5–0:19,5 | **Virada de edição** | Logo **CCXP25** sobre clipes de palco e celebridades, que vira **CCXP26** com glitch e ganha **"DE 3 A 6 DE DEZEMBRO"**. |
| 0:19,5–0:22 | Final | Letreiro por cima do palco com convidados segurando a bandeira do Brasil. Não há cartela preta, e o loop volta direto ao início. |

- **Cor:** a mais **quente** do conjunto (+0,14), pele bonita, pretos cheios. Retratos com flash/luz de preenchimento e fundo desfocado.
- **Legenda:** *"Obrigada por mais uma edição cheia de energia, sorrisos e momentos que vão ficar na memória. E por aqui, a contagem regressiva para a CCXP26 já começou. ⏳⏳⏳"*. Traz agradecimento, contagem regressiva e nenhum link. **68 mil plays e 886 comentários (o maior engajamento da amostra)**. O público se procura nos rostos.

### D. CCXP México — "¡Vive la locura de #CCXPMX25!" (26 s)

- **Hook (0:00–0:02):** letras "C C X" que se montam sobre a multidão, e em seguida **"Banamex Presenta: CCXP MX 25 — SERÁ ÉPICA"** (rosa e amarelo-limão). O **patrocinador master aparece antes de tudo.**
- **0:03–0:10:** colagem em grade de 2 a 4 vídeos simultâneos (Wolverine, Deadpool, Master Chief, Miles Morales, ativação Hot Wheels), com o contador "40…".
- **0:08–0:12:** **"40.000 m² de fandom"** em tipografia gigante sobre os clipes. **É o único vídeo da amostra com número de escala.**
- **0:13–0:20:** painéis com celebridades e "LO MEJOR ESTÁ POR SUCEDER" em kinetic type.
- **0:20–0:26:** cartela magenta com padrão de doodles, "CCXP MX 25 — Más que una Comic Con — 30/05 al 01/06 — www.ccxp.mx" e ícones das redes.
- **Cor:** escura (brilho 0,29) com um véu de escurecimento por baixo do texto. Paleta da marca MX em magenta e limão.
- **Legenda:** *"¡La energía, la emoción, la magia geek… TODO está en este video! … El año pasado hicimos historia juntos… vienen nuevas sorpresas…"*, com Banamex e Ticketmaster marcados.

### E. "Mais que uma Comic Con" (anúncio MX, 24 s) e F. Teaser "É AMANHÃ!" (6 s)

- **E:** texto em fade no preto, "A CCXP MX ESTÁ DE VOLTA", e **"MAIS QUE UMA COMIC CON"** em kinetic type vazado sobre a multidão, que vira em espanhol "MÁS QUE UNA COMIC CON". Seguem 10 s de imagens (painel, plateia, Artists' Valley, show de lasers) e **10 s de cartela estática** (citibanamex Presenta, datas, site). **40% do vídeo é cartela.** Legenda bilíngue PT/ES.
- **F:** **fotos de cosplay em stop-motion** (Pikachu, Pikachu-Deadpool, Goku e Naruto, Harley Quinn), 4:5, **sem áudio**, com overlay fixo "CCXP26 — **É AMANHÃ!** ABERTURA DE VENDAS." e rodapé "É cultura pop · 03–06 DEZ". Foi feito para funcionar sem som no feed e deu ~38 mil plays com um asset baratíssimo.

---

## 3. Padrões recorrentes da CCXP

1. **Portfólio em três camadas:** (a) **recap relâmpago** logo no fim do evento (22 s, vertical, data da próxima edição); (b) **aftermovie "filme"** longo meses depois, usado para abrir a **pré-venda**; (c) **manifesto de marca** com arquivo de várias edições para as **vendas abertas**. O aftermovie não é memória, é **peça de conversão do próximo ciclo**.
2. **Mesma linha narrativa em todas as peças:** "mundos/multiverso/portal" e "nossos mundos vão se encontrar novamente". A frase vira assinatura e bio do perfil.
3. **Todo vídeo termina com a data da próxima edição** (ou "vendas abertas") e o site. O "link na bio" fica na legenda.
4. **Estrelas no centro, fã como coprotagonista:** a reação do público (grito, choro, braços erguidos) sempre vem colada ao plano da celebridade.
5. **Ritmo acelera até ~60% do vídeo e desacelera no epílogo emocional** (A e C). O manifesto (B) já começa acelerado.
6. **Tipografia bold, branca ou amarela, centralizada**, usada com parcimônia. Números e dados quase nunca aparecem no Brasil.
7. **Patrocinador quase nunca em cartela no Brasil** (aparece só no cenário). No México, o naming sponsor abre e fecha o vídeo.

## 4. O que eles fazem MUITO bem

- **Hooks visuais sem texto** que prendem em menos de 2 s: FPV com o Goku (A 0:00), flash de projetor (B 0:00), letreiro gigante (C 0:00).
- **Roteiro com voz over e legenda embutida** (A): tem começo, meio e fim, funciona sem som e transforma o evento em "saga".
- **Uso do rosto do público como conteúdo** (C 0:11–0:15): gera identificação, compartilhamento e comentários ("me achei!").
- **Look autoral no manifesto** (B): scrapbook com grão e recortes, que torna o arquivo antigo "novo" e diferencia a peça.
- **Continuidade de edição para edição:** logo CCXP25 que vira CCXP26 (C 0:16–0:19) e portal com letreiro CCXP25 no aftermovie de 24 (A 2:25).
- **Qualidade de captação alta:** gimbal, FPV, grua e retratos com luz. Parece cinema.

## 5. Pontos fracos e lacunas que o NXP pode explorar

| Lacuna na CCXP | Oportunidade para o NXP |
|---|---|
| O aftermovie principal está em **16:9 horizontal e com 2:35 no Reels** (A), ruim para retenção e tela cheia. | Aftermovie **nativo 9:16**, com 45–60 s no Reels e versão longa no YouTube. |
| O aftermovie longo sai **~4 meses depois** do evento. No calor do pós-evento há só 22 s. | Soltar no dia seguinte um aftermovie completo (45–60 s) e, na mesma semana, "parte 2" e cortes por público (cosplay, games, K-pop etc.). |
| **Dependência de celebridades internacionais**, que o NXP não vai ter no mesmo nível. | Transformar **o fã, o cosplayer e o creator mineiro** em estrela, com nome na tela e marcação. Dá para vender como "o evento onde VOCÊ é o protagonista". |
| **Quase nenhuma fala real do público** (só sonoras de estrelas). | Sonoras curtas de fãs ("primeira vez aqui", "vim de Montes Claros"), com legenda. |
| **Nenhum número de escala** nos vídeos brasileiros. | Kinetic type com números reais ("X mil pessoas", "X horas de programação", "X cosplays"), como a MX faz com "40.000 m² de fandom". |
| CTA fraco: só data e site, **sem lote, preço ou urgência na tela**. A cartela ocupa 5–10 s de tela parada. | Cartela curta (≤ 3 s) com **lote/preço + "link na bio" + contagem regressiva**, e loop sem tela preta (como o C). |
| Patrocinador sem crédito no Brasil. | Cota vendável de **"apresentado por"** com vinheta de 1 s no início e selo na cartela (modelo Banamex). |
| Tom épico e sério, com pouco humor e pouca regionalidade. | Humor e identidade mineira (sotaque, "uai", referências a BH) como diferencial de tom. |

## 6. Técnicas "roubáveis" (com timestamp de exemplo)

1. **FPV com personagem "voando" no hook.** Um action figure preso no drone FPV sobrevoa a fachada e mergulha na fila. Ex.: **A 0:00–0:04**. No NXP: um boneco icônico sobrevoando a entrada do pavilhão.
2. **"Face cascade" sincronizada com o drop.** De 10 a 11 s de planos de escala com áudio baixo, depois ~50 retratos frontais de 2 frames cada, **olhos alinhados no mesmo ponto**, entrando no drop. Ex.: **C 0:05–0:15,5**. Pede um fotógrafo ou videomaker só para retratos padronizados (mesma altura e enquadramento) durante o evento.
3. **Morph de edição com data.** O logo da edição atual vira o da próxima com glitch e ganha a data por cima de imagens de clímax. Ex.: **C 0:16,5–0:19,5**.
4. **Voz over narrativa com legenda amarela embutida**, usando um enredo de "convocação" e epílogo. Ex.: **A 0:04–0:19 e 2:08–2:25** ("Nossos mundos voltarão a se encontrar"). Para o NXP, um narrador com "missão" ou um mestre de RPG local.
5. **Transição por silhueta de papel recortado e colagem torn paper** no estilo scrapbook, com grão. Ex.: **B 0:09,6, 0:12,7 e 0:13–0:25**.
6. **Taxonomia em kinetic type no beat**, uma palavra gigante por plano, dizendo tudo o que o evento é. Ex.: **B 0:46–0:49** (FILME / SÉRIE / QUADRINHO / ANIME / COSPLAY). Para o NXP: GAMES / COSPLAY / K-POP / ANIME / CREATORS…
7. **Mural em grade que se preenche** com os melhores rostos (convidados e fãs) para fechar o clímax. Ex.: **B 0:54,7–0:57**.
8. **Stutter/freeze de 2–3 frames no pico emocional**, o gesto repetido em stop-motion. Ex.: **B 0:08,6–0:09,3** (sabre de luz) e **B 0:37,4–0:38** (Kuzco com borda de sticker).
9. *(Bônus, custo zero)* **Stop-motion de fotos + overlay fixo de urgência, sem áudio, em 4:5.** Ex.: **F 0:00–0:06** ("É AMANHÃ! Abertura de vendas").

---
*Fontes auxiliares: canal oficial do YouTube @ccxpoficial (metadados via yt-dlp: CCXP24 Aftermovie fGr6CvgLv8U, 156 s, 2,5 mil views; "Anatomia de uma CCXP" oLEZZQObtrw, 71 s, 388 mil views; CCXP23 Aftermovie cpddyr7pGMY, 160 s, 7,9 mil views, não baixado).*
