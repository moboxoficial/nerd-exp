# Nerd Experience (NXP): análise dos aftermovies próprios e banco de footage

Data: 30/09/2026. Pasta: `$S/nxp/` (vídeos em `raw/`, análises em `analise/<arquivo>/`, metadados em `meta/`, storyboards do YouTube em `yt_sb/`). O catálogo plano a plano está em `CATALOGO.csv`.

---

## 0. Resumo honesto

- **Baixei 30 vídeos do Instagram** via `/embed`, entre reels do @nerdexperience e collabs/republicações (@estadodeminas, @nerdcomunica, @minas_shopping, @moboxproducoes, @nerdverso.nxp, @omelete, @filme10). O JSON de cada download está em `meta/ig_<code>.json`. Tentei outros 17 shortcodes, que falharam porque eram foto ou carrossel sem vídeo (lista em `meta/ig_failed.txt`).
- **Só 9 desses 30 têm cenas reais do evento.** Os outros 21 são talking head em estúdio, notícia geek, promo gráfico ou conteúdo sem relação com o evento. O feed do @nerdexperience de 2025/26 é quase todo quadro de estúdio ("UPDATE NXP", "Jogo do Contato" etc.).
- **O material limpo e utilizável se concentra em 2 vídeos.** O primeiro é o aftermovie da 12ª edição (`ig_DO4cd4Uj1ZR`, 720x1280). O segundo é o teaser do Minas Shopping, com imagens da 11ª edição (`ig_DOyHlxnCJvI`, 504x896).
- **Resolução típica: 360x640 a 720x1280, sempre vertical**, com a recompressão do Instagram. Nenhum arquivo passa de 720p.
- **O YouTube não baixou.** O canal oficial (@nerdexperience, UC2TIV0LAfVRaFy1FihRhwyw) tem os aftermovies antigos em **1080p horizontal**, mas o googlevideo devolveu **HTTP 403** para qualquer cliente testado. Os clientes web/tv/ios/mweb pedem login ("Sign in to confirm you're not a bot"). Consegui apenas os metadados (`meta/yt_*.info.json`) e os storyboards de 160x90 (`yt_sb/*_sheet.jpg`). Com eles fiz a análise visual dos aftermovies antigos, mas **não há arquivos de vídeo do YouTube no banco**.
- **O TikTok também não baixou.** O perfil @nerdexperience tem 73,1 mil seguidores e 696 vídeos, mas o extrator respondeu "IP address is blocked".
- **Listar o perfil do Instagram não funciona**: devolve 429/401, e o `/embed` do perfil não traz os posts. Todos os shortcodes vieram de busca na web, então o banco é uma amostra do perfil, não o perfil inteiro.

---

## 1. Inventário do banco (30 arquivos, 148 MB)

| Arquivo | Dono | Duração | Res. | Conteúdo | Footage do evento? |
|---|---|---|---|---|---|
| ig_DO4cd4Uj1ZR | nerdexperience | 76s | 720x1280 | **Aftermovie 12ª ed. 2025** ("Último dia de NXP...") | **SIM: principal fonte limpa** |
| ig_DOyHlxnCJvI | minas_shopping | 32s | 504x896 | Teaser "última chamada" 12ª ed.; 0-16s com imagens de edição anterior | **SIM: 3-16s limpos** |
| ig_DO15ZhYgTeT | nerdcomunica | 83s | 720x1280 | "Tour pela NXP 2025", celular + legendas | Sim, legenda queimada em tudo |
| ig_DO-4dGfFF9G | estadodeminas | 90s | 360x640 | Matéria EM/Glitch Clube, 12ª ed. (vídeo "Leo Lima e Nerd Experience") | Sim, logos EM + legenda em tudo |
| ig_DZ8fHR3AGDI | nerdexperience | 28s | 720x1280 | "O NXP evoluiu" (promo 2027); 18-22s reaproveita palco da 12ª | Pouco, legenda |
| ig_DAOf-QmRtuG | nerdexperience | 19s | 360x640 | Arena Claro Gaming 2024 com apresentador | 10-15s, legenda |
| ig_C-pmbwKxJ9W | nerdexperience | 9s | 360x640 | Promo 11ª ed. com post-it "Somos o evento mais NERD de MG" | Flashes, post-it em tudo |
| ig_DO3HOJSElTt | nerdexperience | 74s | 720x1280 | Pedro Patrus visita a 12ª ed. (institucional) | Pouco, legenda |
| ig_DPFCB4wlQyl | nerdexperience | 7s | 720x1280 | Slideshow de **fotos** de cosplay com marca d'água "Nerd Experience" | Fotos, com marca d'água |
| ig_DE8Tnv8xl80 | nerdexperience | 47s | 360x640 | Corrida Naruto na UFMG (jan/25), "BH cidade mais nerd" | Não é o evento (multidão de BH) |
| ig_DY29oDhD77J, ig_DZazEMakQ57, ig_DZnqgCGgANj, ig_DaIgDc_lppM, ig_DZD1vLEkdth, ig_DZtGTYth6dk | nerdexperience | 22-62s | 360-720p | Promos 2027 (Expominas, ingressos, 10 anos, Next Level, Lótus) em estúdio | Não |
| ig_DJcjANTpkNo, ig_DKfNzOVxVYc, ig_DOopKtDFEPp, ig_DKkpQ6WhbSR, ig_DJPCCC3vS4z, ig_C8Xt3l3xta6, ig_C9NA0UOvwQx | nerdexperience | 7-61s | 360-720p | Promos 2024/25 em estúdio (data, lote, Next Level, Pixel) | Não |
| ig_C-BZ3acxoOv | nerdexperience | 38s | 720x1280 | Anúncio do dublador Luiz Carlos Persy (clipes de filmes) | Não |
| ig_C_qGM8gCvX6, ig_DN3zdEJ3isz | nerdexperience | 93/112s | 360x640 | Notícias (Disney, BTS) | Não |
| ig_C4slk20OxNV | moboxproducoes | 85s | 720x1280 | "Quem é a MOBOX" (talking head) | Não |
| ig_DSK4zuxjYd8 | nerdverso.nxp | 27s | 476x846 | Promo do Pixel 2ª ed. (chroma) | Não |
| ig_DXy_Ncqk49X | omelete | 142s | 360x640 | Quiz Fanta x Xbox (redação Omelete) | Não |
| ig_DaS_4iqDkYT | filme10 | 10s | 720x900 | Wendel Bezerra (clipe) | Não |

**Vídeos do YouTube oficial que precisam ser baixados de outra máquina** (1080p, horizontal; metadados em `meta/`):

| ID | Título | Data | Duração | Views | Observação pelo storyboard |
|---|---|---|---|---|---|
| **pscovXF_iGE** | NERD EXPERIENCE - MARÇO DE 2023 (9ª ed.) | 06/09/2023 | 3min14 | 897 | **O mais rico do acervo.** Multidão lotando o palco com luz roxa/rosa, arena Monster, palco Fanta, piscina de bolinhas, banda, desfile cosplay, cosplays de Mandalorian, Ghostface e Scream. |
| oyZi6dmhu9g | NXP: Juntos, no próximo nível (retrospectiva 2018-22) | 05/01/2023 | 1min33 | 3.019 | Multidões 2019/2022, cosplays de rua, VR. Cartelas e legendas por cima em quase tudo. |
| RsuL199yQUk | AfterMovie NXP BH Junho 2019 | 24/06/2019 | 1min29 | 639 | Salão lotado, cosplays, VR, logo antigo |
| 9gsNsYHiw2o | Veja como foi NXP BH 2ª Edição (Shopping Cidade) | 18/09/2019 | 1min | 1.621 | Aftermovie curto |
| 0kYY2VENizU | Veja como foi o NXP - Novembro 2019 | 17/10/2020 | 1min | 255 | Aftermovie curto |
| vPKuU3cyDlE | Conheça o Nerd Experience | 05/11/2021 | 1min | 7.230 | Institucional |
| kyNfwAWvdSg | Vem aí o NXP 2025 – Conheça Novos Mundos | 08/09/2025 | 30s | 28.952 | Teaser 2048x1080 |
| xu7O5cR2A8M | Repórter Nerdão no NXP 2022 | 23/12/2022 | 11min44 | 93 | Entrevistas com público e cosplayers (720p) |
| 6pkeUbn8oLE | BH NXP | 2024 | 5min | 62 | Caminhada 360° pela Pampulha: não é o evento |

Canais de terceiros com cobertura do evento: "Nerd experience 2025 Desfiles 21/09 Sem cortes" (eUMEW4kS7g8, desfile cosplay completo da 12ª); "Cosplayers parade on the Fanta stage – NXP 2023" (8t9M72T17iw); "Nerd Experience 1 | Primeiro/Segundo Dia | 2023" da agência Do Brasil Live Mkt (feivYtVBuAs, xY6Cpew3UMg), que provavelmente é um recap de ativação Coca-Cola/Fanta com captação profissional; Tecnologia Incrível (0KJa8E2SOKk, DEj5eAp7smw); Chechel Otaku Side (várias coberturas). **Todos exigem autorização de uso.**

---

## 2. Análise crítica dos aftermovies e recaps próprios

### 2.1 Aftermovie 12ª edição (IG DO4cd4Uj1ZR, set/2025): o melhor que o NXP já fez

- **Estrutura:** 0-10s de abertura com cenografia (banner "Conheça Novos Mundos", parede NXP, portal) e depoimentos em off legendados ("Tô muito feliz de poder participar", "Não é à toa que não é a minha primeira vez"). Segue uma rajada de retratos de cosplay (10-28s), ativações como prancha, basquete e arco (18-34s), games (35-40s), palco e painel com plateia (41-53s), show da banda (54-61s) e o fã cantando (61-64s). Termina com uma **cartela "NXP 12ª edição – CONHEÇA" de 12s em silêncio** (64-76s).
- **Ritmo:** 53 planos em 76s. O plano médio fica em 1,43s, chegando a 0,84s no trecho de cosplay e a 5s na cartela final. Só **17% dos cortes caem no beat** (BPM ~103), e a montagem é mais descritiva que musical.
- **Cor:** look cinematográfico, com lente de pouca profundidade de campo, retratos com fundo desfocado e tons quentes nos cosplays. As luzes do palco puxam para ciano e roxo. Saturação média de 0,37. É a melhor captação do acervo.
- **Áudio:** curva de loudness em ~-15 dB, com **queda de energia entre 31s e 46s (-20 a -29 dB)**, justamente na parte de games e painel. Nos últimos 8s há silêncio total (-120 dB). O áudio não cresce para um clímax.
- **Tipografia e marca:** só aparece na legenda de depoimento e na cartela final. Não há nenhum número (público, edição, área) nem nome de atração.
- **CTA:** fraco. A cartela diz apenas "CONHEÇA", sem data, local ou ingresso, e em silêncio.
- **O que funciona:** a qualidade de imagem, a variedade de rostos e cosplays, as **reações do público** (fã maravilhada, punho erguido, fã cantando), o show ao vivo com palco e o arco dramático painel → show.
- **O que está fraco para venda:**
  - Abre com letreiros e cenografia, e não com o pico de emoção.
  - Não há plano aberto de multidão, drone ou establishing do Minas Shopping: nada mostra a escala dos 10 mil.
  - Os convidados famosos não são identificados.
  - A energia cai no meio.
  - O final é mudo e sem data.
  - É vertical-only.

### 2.2 Aftermovies antigos (YouTube, analisados pelo storyboard)

- **Junho 2019 (RsuL199yQUk, 89s, 16:9):** abertura em P&B com salão lotado, depois cor saturada azul/magenta com glitch. Tem muita multidão e cosplay e fecha com VR e o logo MOBOX. A escala do público está bem mostrada, mas faltam foco e narrativa. O logo antigo (N/X losango) e os efeitos de glitch datam o vídeo, e o final termina na assinatura da produtora, sem CTA de data.
- **Retrospectiva 2018-22 (oyZi6dmhu9g, 93s):** é narrativo ("surgiu de um sonho", "em 2019 fizemos a 1ª edição", pandemia com manchetes de "BH amanhece de portas fechadas", as edições online de 2020/21, "vocês estavam lá!", "gritamos com as vozes oficiais do Homem de Ferro e do Thor", fechando em "18 e 19 de março, juntos no próximo nível"). Tem arco emocional e CTA com data. Em compensação, **a legenda cobre quase todos os planos**, tem ~15s de interface de live e usa muito material de celular e de pandemia. Serve de referência de roteiro, não de footage.
- **Março 2023 / 9ª ed. (pscovXF_iGE, 3min14):** material excelente, com plateia lotada em frente ao palco sob luz roxa, ativações Monster e Fanta, banda, piscina de bolinhas e cosplays. Mas tem **3min14**, longo demais para anúncio, e o storyboard sugere clima de vlog. Precisa virar um corte de 30 a 60s.

### 2.3 Teasers e recaps curtos

- **Minas Shopping (DOyHlxnCJvI):** o melhor ritmo do acervo, com cortes de 0,4-0,6s sobre a música: sabre de luz, capacete do Homem de Ferro, barbudo gargalhando, cosplayer idoso gritando, criança gamer. Na sequência vêm cartelas de atrações (Muca Muriçoca, Sérgio Stern, Mauro Ramos) e "save the date". É um modelo de teaser de venda que funciona, mas tem só 504p.
- **Post-it (C-pmbwKxJ9W):** ideia boa de marca ("Somos o evento mais NERD de MG!"), mas o post-it cobre todos os planos.
- **Feed 2026/27:** quase só talking head em estúdio. A página pouco mostra o evento em si e o público real, que é o que vende.

### 2.4 O que um aftermovie de venda precisa (e o acervo não tem)

1. Um gancho nos primeiros 2s com o pico de emoção (multidão pulando, grito, reveal de cosplay).
2. Prova de escala: plano aberto e drone do pavilhão cheio, fila de entrada.
3. Os famosos identificados com lower thirds (dubladores, influenciadores) e momentos deles com fãs.
4. Números na tela: 10 mil pessoas, 12 edições, 10 anos, 4 universos.
5. Música que cresce, com cortes no beat e um drop.
6. CTA falado e escrito com data, local e ingresso (27 e 28/fev/2027 – Expominas).
7. Versões 16:9 e 9:16.

---

## 3. Lacunas de footage

1. **Planos abertos de multidão e drone:** quase nada. O único plano de plateia limpo é o `DO4cd4Uj1ZR` 47,6-48,6s. Salão lotado existe só no YouTube (2019 e 2023), que não baixou.
2. **Famosos em ação com fãs identificáveis:** faltam meet & greet, autógrafos, dublador fazendo voz ao vivo. Há painéis da 12ª (Sérgio Stern, Mauro Ramos) apenas com legenda queimada.
3. **Material horizontal e em alta:** zero. O banco inteiro é vertical ≤720p. Isso é crítico para um anúncio 16:9 e para telão.
4. **Entrada e fila, abertura de portões, contagem regressiva.**
5. **Concurso e desfile cosplay em palco:** limpo, não há. Só `DZ8fHR3AGDI` com legenda, e o desfile completo de terceiros (eUMEW4kS7g8).
6. **Kids, família e pet:** um menino gamer (DOyHlxnCJvI 14,5s) e cachorros apenas com logo ou post-it.
7. **Ativações de marca patrocinadora limpas** (Fanta, Monster, Claro, Netflix) para mostrar ao patrocinador: só com legenda ou de 2023 no YouTube.
8. **Bastidores e montagem, time MOBOX, Expominas** (o novo local ainda não tem imagem do evento).

**Recomendação:**
- Pedir à MOBOX os **brutos originais** do aftermovie da 12ª (ele foi claramente filmado em 4K/cinema; o IG entrega 720p) e os masters dos aftermovies do YouTube.
- Baixar o YouTube a partir de uma máquina com cookies.
- Pedir ao Estado de Minas e ao @nerdcomunica os arquivos sem legenda.

---

## 4. Nomes e números encontrados nas legendas e na imprensa

- **Edições e datas:**
  - 1ª em BH: jun/2019. 2ª: 31/ago-01/set/2019, no Shopping Cidade, com patrocínio da Prefeitura de BH. Houve outra em nov/2019.
  - Edições online em 2020/21 ("Nerd Experience Live").
  - 9ª: 18-19/mar/2023, Minas Shopping.
  - 11ª: 21-22/set/2024, Minas Shopping.
  - **12ª: 20-21/set/2025, Minas Shopping, tema "Conheça Novos Mundos"**, com 4 universos: Eldarion (medieval), Pixel (games e tecnologia), Lótus (cultura asiática) e Nexos (cinema e séries).
  - **Próxima: "Nerd XP Pop Festival – Além do Portal", 27-28/fev/2027, Expominas** ("o maior espaço da nossa história"; "10 anos de Nerd Experience").
- **Público:**
  - 9ª ed.: ~7 mil pessoas em 2 dias, o dobro da edição anterior e com investimento ~10x maior (Diário do Comércio).
  - 12ª ed.: **~10 mil visitantes** (Estado de Minas).
  - A MOBOX cita também produzir "a terceira maior Parada do país, que leva mais de 250 mil pessoas" (outro evento).
- **Atrações e convidados:**
  - 2023: Guilherme Briggs, Marcos Castro, Muca Muriçoca, Angélica Moreno (Pandangelica), Gordox, TK Raps.
  - 2024: Luiz Carlos Persy (@lcpersy) e Caito Mainier.
  - Shorts do YouTube citam Wendell Bezerra no NXP.
  - 2025: Sérgio Stern e Mauro Ramos (painel de dubladores de Sulley e Mike Wazowski), Muca Muriçoca, uma banda ao vivo e o concurso cosplay.
  - 2027: Feh Dubs e O Gaveta ("primeira atração").
  - Rostos da casa: Túlio Gama (host dos quadros) e Ado Viana, diretor, que resume o evento como "de fã pra fã".
- **Marcas:**
  - Coca-Cola FEMSA como patrocinadora master em 2023, com o palco Fanta (quizzes e sampling) e a Arena Monster de e-sports.
  - Fanta Halloween em 2025.
  - Arena e-Sports by Claro Gaming em 2024.
  - PUC Minas, Netflix (letreiro no palco em 2025), Cineart, Pokerstars (camiseta de apresentadora).
  - Backdrop com apoio do Governo de Minas/FAPEMIG.
- **Produtos de ingresso:** Next Level (camiseta exclusiva, pin, pôster, tirante, mochila, meet & greet garantido, entrada 1h antes, tour de bastidores na sexta) e lotes promocionais a R$25.
- **Redes:** IG @nerdexperience com ~31 mil seguidores e 1.763 posts; TikTok com 73,1 mil seguidores e 696 vídeos; X @nerdexperience_; YouTube @nerdexperience.
- **Cosplayers identificáveis:** não consegui ler nomes ou @ nos planos. Cosplays reconhecíveis: Batman Que Ri (aparece em 3 fontes, figura recorrente), Yor Forger, Megumin, Inuyasha, Miles Morales, Deadpool, Iron Spider, Elsa, Darth Vader, Frieren e Jinx.

---

## 5. Top planos (ver CATALOGO.csv, nota ≥ 4)

Todos são verticais. Os de `DO4cd4Uj1ZR` estão em 720p com a melhor qualidade; os de `DOyHlxnCJvI` estão em 504p.

- **Reações:** DO4cd4 52,27-54,00 (punho erguido) · 61,43-64,33 (fã cantando) · 50,47-52,27 (fã maravilhada) · DOyH 8,13-8,63 (barbudo gargalhando)
- **Multidão:** DO4cd4 47,60-48,63 (plateia sorrindo)
- **Palco:** DO4cd4 54,00-55,63 (vocalista) · 48,63-50,47 (convidado na beira do palco) · 41,40-42,90 (apresentadora)
- **Cosplay:** DO4cd4 9,80-10,50 (Twilight piscando) · 11,43-11,97 (Batman Que Ri) · 24,83-25,47 (Yor) · DOyH 11,60-12,27 (cosplayer idoso gritando) · 3,00-3,90 (sabre de luz) · 6,50-7,13 (capacete Homem de Ferro)
- **Mascote:** DO4cd4 27,23-29,00 (robô NXP)
- **Ativações:** DO4cd4 29,13-31,40 (POV arco) · 18,90-20,10 (prancha de equilíbrio)
- **Games:** DO4cd4 36,00-37,83 (Valorant)
- **Kids:** DOyH 14,50-15,67 (menino gamer)
