# BGS – Brasil Game Show: análise de aftermovies e recaps em vídeo

*Benchmark para o Nerd Experience (NXP, BH). Análise feita em 30/09/2026, com a BGS 2026 ainda por acontecer (9 a 12/10/2026). As últimas edições realizadas são, portanto, 2023, 2024 e 2025.*

## 0. Resumo honesto do levantamento

- **Handle confirmado:** Instagram **@brasilgameshow**, com cerca de 360 mil seguidores e cerca de 5,8 mil posts ("A Maior Feira de Games da América Latina"). Não existe um @bgsoficial oficial. O YouTube oficial é o canal "Brasil Game Show" (`UCCroahB_nJSmvuU4IvfGa1A`).
- **A BGS não publica no Instagram um "aftermovie" clássico pós-evento**, com 2 a 5 minutos, "obrigado" e data da próxima edição, pelo menos não um que eu tenha encontrado. Busquei por "aftermovie", "vídeo oficial", "melhores momentos", "obrigado", "saudade", "#VivaOGame", "#BGS23", "#BGS24" e "#BGS25", e verifiquei cada post pela página /embed. No Instagram, o formato que ela usa são **recaps diários "same-day edit"** (cerca de 45 s, 9:16), produzidos pela agência **Whido (@whidobr)** e usados como **peça de venda de ingresso durante o evento**. O Instagram também recebe cortes de "hero moment" (Kojima) e um vídeo institucional de aniversário.
- As peças "oficiais" longas e de maior alcance estão no **YouTube**:

| Peça (YouTube) | Data | Duração | Views | Natureza |
|---|---|---|---|---|
| [Vídeo Oficial #BGS23 – Viva O Game](https://www.youtube.com/watch?v=Kme0qu-9mFw) | 22/11/2023 | 4:53 | 56,7 mil | **o único aftermovie "de verdade"** (pós-evento, 16:9) |
| [BGS 2022 – Vídeo Oficial](https://www.youtube.com/watch?v=EDLgDdMBBF4) | 07/02/2023 | 4:38 | 839 mil | aftermovie de 2022 |
| [BGS 2024 – Viva O Game](https://www.youtube.com/watch?v=RfEay-NdFzE) | 01/07/2024 | 1:24 | 887 mil | comercial pré-evento (views típicas de mídia paga) |
| [BGS 2025 – Uma Nova Fase!](https://www.youtube.com/watch?v=dE-c5zqj9EM) | 11/08/2025 | 0:30 | 1,1 mi | comercial pré-evento (nova casa: Distrito Anhembi) |
| [Momentos BGS25](https://www.youtube.com/shorts/bvXOkPi5SWQ) (Short) | 15/12/2025 | 0:48 | 209 | recap pós-evento vertical (Whido) |

- **Limitação:** não consegui baixar nenhum vídeo do YouTube. O yt-dlp recebe "HTTP 403" e "Sign in to confirm you're not a bot" em todos os clientes. **Não analisei quadro a quadro** o vídeo oficial da BGS23, o de 2022, os comerciais de 2024/25 nem o Short "Momentos BGS25". A seguir, tudo o que tem análise visual vem dos **4 reels do Instagram baixados e analisados** com o analyze.py e com a leitura das contact sheets e de frames extras.
- **Não encontrei nenhum recap pós-evento da BGS24 no Instagram.** A cobertura de 2024 foi feita em carrossel de fotos (ex.: [DBB4N2IsLq5](https://www.instagram.com/p/DBB4N2IsLq5/) e [DCAP4S8tfeK](https://www.instagram.com/p/DCAP4S8tfeK/)). Em 2024, a peça em vídeo mais "aftermovie" é o reel de 15 anos (junho de 2024), que é retrospectivo.

## 1. Vídeos analisados

| # | Reel | Data aprox. | Duração | Formato | Plays | Autor da edição |
|---|---|---|---|---|---|---|
| A | [O PRIMEIRO DIA DE #BGS2025 FOI INSANO](https://www.instagram.com/reel/DPnDhiekhVG/) | 09-10/10/2025 | 46,1 s | 9:16, 30 fps | **27,4 mil** | @whidobr |
| B | [A BGS tá explodindo em diversão…](https://www.instagram.com/reel/DPpuh9Ej1WU/) | ~11/10/2025 | 43,6 s | 9:16, 23,98 fps | 13,8 mil | @whidobr |
| C | [Um momento pra ficar na história (Kojima na abertura)](https://www.instagram.com/reel/DPrtqeZAgoc/) | ~10-11/10/2025 | 18,7 s | 9:16 | 16,2 mil | @whidobr |
| D | [Há exatos 15 anos… (#BGS15anos)](https://www.instagram.com/reel/C8fYkFdJhD7/) | 21/06/2024 | 43,9 s | 9:16 | 3,5 mil | (institucional) |

Os arquivos, as análises e as contact sheets estão em `competidores/bgs/` (`v3_*`, `v5_*`, `v4_*` e `v6_*`, com as respectivas pastas `an_*`).

### Métricas técnicas (analyze.py)

| Métrica | A – Dia 1 BGS25 | B – "Explodindo" | C – Kojima | D – 15 anos |
|---|---|---|---|---|
| Nº de planos detectados | 72* | 60* | 4 (1 plano real) | 18 |
| Plano médio | 0,63 s* | 0,73 s* | 18 s (oner) | 2,44 s |
| Ritmo por quinto (plano médio) | 0,38 / 0,46 / 0,40 / 0,38 / **0,77** | **0,31** / 0,87 / 0,79 / 1,09 / 1,25 | contínuo | 8,8 / 2,9 / 1,25 / **0,98** / 4,4 |
| BPM estimado | 129 | 99 | 99 | 103 |
| Cortes no beat | 23,5 % | **50,8 %** | n/a | 23,5 % |
| Drops (subidas bruscas) | 0, 11, 17, 21, 27, 35, 40, 42 s | 0, **23** s | nenhum | 0, 5, 10 s |
| Saturação média | **0,44** | 0,32 | 0,22 | 0,37 |
| Brilho médio | 0,47 | 0,47 | 0,43 | **0,32** |
| Temperatura (R−B) | **+0,09 (quente)** | +0,03 (neutro) | +0,07 | 0,00 |

\* *O detector conta como corte cada flash de light leak ou film burn e cada doodle animado, então os números de A e B saem inflados. Na leitura visual, o ritmo real de A fica em cerca de 1 plano por 0,8 a 1 s. Em B, a abertura tem cortes reais de 3 a 4 quadros.*

---

## 2. Análise por vídeo

### A. "O primeiro dia de #BGS2025 foi insano!" (a peça de maior alcance)

**Legenda:** "O PRIMEIRO DIA DE #BGS2025 FOI INSANO! 🔥🎮 Teve jogo, teve emoção e MUITA energia gamer no ar! E o melhor? A BGS TÁ SÓ COMEÇANDO! 👀 Ainda tem MUITO mais vindo aí: convidados incríveis, campeonatos, brindes, experiências únicas… Não dá pra perder, vem pra BGS! 📹 @whidobr". O post teve 119 comentários. A promessa é FOMO: o evento continua e ainda dá tempo de ir.

**Estrutura**

| Tempo | Bloco | O que aparece |
|---|---|---|
| 0:00–0:01,4 | **Hook** | Drone/FPV em voo rasante sobre a multidão **correndo pra dentro** do pavilhão na abertura dos portões, com o **logo "BGS25" em overlay** no centro da tela desde o primeiro quadro |
| 0:01,4–0:02,5 | Transição-assinatura | **Light leak** laranja com **rabiscos/doodles cor creme animados** (traço de pincel), e o logo "se desfaz" |
| 0:02,5–0:06 | Cerimônia de abertura | Apresentadores no palco, plateia aplaudindo, palestrante com camiseta "Hype Con / BGS25" |
| 0:06–0:13 | Pavilhão | Multidão, plateia de palco, cosplay, **fliperama Top Game ("Order Select")**. **Moldura PiP** (o quadro encolhe dentro de outro) sempre com os doodles por cima |
| 0:13–0:20 | Depoimento 1 | Convidado japonês de moletom Dodgers com **legenda amarela**: "Eu estou aqui há nove horas / e já consigo sentir a paixão do povo brasileiro!" Na sequência, um plano do palco com telão |
| 0:20–0:29 | Depoimento 2 e público | Fãs: "**Já quero voltar no ano que vem!**" Na sequência: fã "selfie" com fone, cosplay de foice (PiP e doodle), aéreo da multidão, meet & greet |
| 0:29–0:35 | Ativações | Artista fazendo **stencil com spray ao vivo**, cosplay no palco, **VR**, **POV de simulador de corrida (Sensa)** |
| 0:35–0:44 | Clímax emocional | Executivo discursando, depois o **concerto "A New World – intimate music from Final Fantasy"** (orquestra no palco), plateia emocionada, **POV do celular filmando o show**. O ritmo cai de 0,38 para 0,77 s por plano |
| 0:42,9–0:45 | Respiro de humor | Close de **cosplay de Deadpool punk** "tapando o rosto" (gesto de fofura) |
| 0:45,5–0:46 | **End card** | Logo BGS25 sobre preto. **Não tem data, CTA ou ingresso na tela** (tudo isso fica na legenda) |

- **Tipos de plano:** aéreo e FPV indoor, multidão aberta, close de cosplay, reação e depoimento de público, palco com painel e show, ativação de marca, POV handheld, fliperama e VR. Não aparece gameplay em tela cheia. Também não aparecem time-lapse nem slow motion evidentes.
- **Cor:** a peça mais quente e saturada do conjunto. Os pretos são esmagados, os light leaks são laranja, vermelho e amarelo, e as luzes do pavilhão ficam em teal. O look é "filme analógico / film burn" sobre um grade contrastado.
- **Motion graphics e VFX:** logo BGS25 como bug no hook e no fim, doodles animados cor creme (a marca visual da Whido em 2025), molduras PiP que encolhem e expandem, light leaks e flashes brancos como transição, e legendas amarelas em sans simples. Não há números de público, datas nem HUD gamer.
- **Áudio (inferido pelos dados):** trilha eletrônica/pop a cerca de 129 BPM com vários "impulsos" (drops em 11, 17, 21, 27 e 35 s) e depoimentos em voz direta, legendados. Só 23,5 % dos cortes caem no beat. A sensação de energia vem dos flashes e não da sincronia com a música.
- **Patrocinadores e marcas visíveis:** Top Game (arcades), Sensa (simuladores), Final Fantasy/Square Enix (concerto), marca "Hype Con". Nenhum aparece em destaque pago evidente: as marcas entram como "cenário".

### B. "A BGS tá explodindo em diversão, jogos, encontros e surpresas!"

**Legenda:** "E se você ainda não veio, ainda dá tempo de fazer parte dessa história! **Ingressos para domingo disponíveis (por enquanto!)** 📹 @whidobr". É o CTA de escassez mais explícito do conjunto.

| Tempo | Bloco | O que aparece |
|---|---|---|
| 0:00–0:04,5 | **Hook "portões abrindo"** | Rajada de **cortes de 3 a 4 quadros com film burn branco e laranja**: corredor vazio e grades (pré-abertura), público entrando, banner **"UMA NOVA FASE"** (slogan de 2025), **mascote de batata frita McCain** com um fã dentro, fãs reagindo, tesoura cortando uma fita vermelha, corredor de grades iluminado. Plano médio de 0,31 s, **50,8 % dos cortes no beat** |
| 0:04,5–0:11 | Multidão e emoção | Aéreo de multidão, fã segurando a plaquinha "❤ BGS", **senhora de cabelo branco gargalhando** (quebra o estereótipo), cosplay, plongée de estande, jogador de Mortal Kombat |
| 0:11–0:23 | Tour de estandes | **Nintendo**, cosplay de V de Vingança, **loja Kojima Productions**, "Experiência Mega Evolução" (Pokémon), **colecionável dourado Bot_GS** (mascote da BGS, "Nova Fase") na mão de crianças fantasiadas, loja Sonic, estande "QD", camisa **FURIA/Pokerstars** |
| 0:23 | **Drop** | Whip pan com motion blur, e o ritmo "respira" |
| 0:23–0:36 | Ativações | Simulador de corrida, **logo Monster Energy em neon verde**, cosplays, arena **"8-Bit Ultra"**, headset de VR, cosplay rosa no palco do BGS Cosplay |
| 0:36–0:39,8 | Encerramento | Aéreo da multidão e do pavilhão lotado, apresentadora num estande |
| 0:39,9–0:43,5 | **End card** | Film burn que "queima" para preto, **logo BGS25 fixo por cerca de 3,5 s**. Não tem data nem CTA na tela |

- **Ritmo:** a peça desacelera de propósito (0,31 s, depois 0,87, 1,09 e 1,25 s por plano). O começo é frenético e depois vira passeio.
- **Cor:** neutra e menos saturada (0,32). O contraste vem das luzes do evento (magenta, azul, verde) e dos flashes de film burn estourados em branco e laranja.
- **Marcas visíveis:** McCain, Nintendo, Kojima Productions, Pokémon, Sonic, Monster Energy, FURIA/Pokerstars e Bot_GS. **Muitas marcas em 43 s, integradas como "atração"** e não como vinheta de patrocinador.

### C. Kojima na cerimônia de abertura (hero moment)

**Legenda:** "🎥✨ Um momento pra ficar na história da #BGS2025! A cerimônia de abertura foi ainda mais inesquecível com a presença do lendário Hideo Kojima! … Vem curtir a BGS com a gente! 📹 @whidobr"

- **Um único plano de cerca de 18 s com drone FPV** (depois de um flash branco de 0,2 s). A câmera entra por cima da plateia no escuro, com o rosto de Kojima nos telões, desce até a área do **corte de fita** (o mascote Bot_GS gigante, figurinos encapuzados, fotógrafos) e segue em travelling rasante ao longo da grade enquanto a comitiva caminha.
- Não tem texto na tela nem cortes (0 % no beat), e o áudio é contínuo, sem drops (provavelmente trilha ou som ambiente).
- A cor é dessaturada (0,22) e escura, e o que dá o contraste são os telões.
- Com 16,2 mil plays em 18 s, o resultado mostra que um **nome grande e um plano "impossível" bastam**. Não é preciso montagem.

### D. "Há exatos 15 anos…" (#BGS15anos, junho de 2024)

**Legenda:** um texto institucional longo sobre a história da BGS desde 21/06/2009 ("aproximamos grandes marcas do público…, testamos centenas de jogos antes do lançamento, conhecemos lendas…"), terminando com a promessa de que "a edição especial de 15 anos será uma grande homenagem… OS GAMES!"

| Tempo | Bloco | O que aparece |
|---|---|---|
| 0:00–0:09,9 | Abertura lenta | Plano único e escuro de **plateia com lanternas de celular acesas** (clima de show) |
| 0:09,9–0:17,7 | **Tríptico vertical** | Tela dividida em 3 faixas com **material de arquivo** (BGS antiga em pavilhão claro, filas, LAN, pedido de casamento no estande Mario, mãos com aliança). Letterings grandes: "**15 ANOS DE PAIXÃO PELOS GAMES**", "**15 ANOS DE BGS**" e "**15 ANOS DE MOMENTOS INESQUECÍVEIS**" (branco com a palavra-chave em laranja) |
| 0:17,7–0:26,6 | Emoção | Pai e filha em cadeira de rodas, criança jogando, e **tipografia cinética palavra por palavra** ("OBRIGADO… POR… FAZER… PARTE… DA… HISTÓRIA") em letras gigantes com blur e glow |
| 0:26,6–0:35 | **Clímax / mosaico** | Troféu de esports, cosplays, estande Nintendo, e um **mosaico acelerado de 6 colunas** de fotos de arquivo (29,8 a 31,6 s, cortes a cada 0,2 s) |
| 0:35,5–0:41,6 | **CTA** | O **mascote Bot_GS em 3D** segura um bolo neon: "VIVA O GAME E CELEBRE OS 15 ANOS DE BGS COM A GENTE". Depois, o logo "15 ANOS" em vermelho |
| 0:41,6–0:43,9 | Fecho | Ícone "play" da marca sobre cinza |

- **Áudio:** trilha a 103 BPM com um crescendo de loudness de 19 a 26 s (de −20 para cerca de −9,5 dB), que é o pico emocional, e queda no mosaico.
- **Cor:** a mais escura (brilho 0,32), com arquivo dessaturado puxado para teal e acentos laranja e vermelho da marca.
- **Alcance baixo (3,5 mil):** o institucional sem "gente real" performa bem pior que o same-day edit.

---

## 3. Padrões recorrentes da BGS

1. **O same-day edit substitui o aftermovie.** O vídeo sai no mesmo dia (a Whido fala em peças de até 60 s entregues no dia e mais de 4 mil arquivos brutos) e serve para **vender o ingresso dos dias seguintes**, com legendas do tipo "ainda dá tempo", "ingressos para domingo (por enquanto!)" e "a BGS tá só começando".
2. **O hook é a abertura dos portões e a multidão em movimento**, com drone ou FPV e o logo da edição sobreposto logo no primeiro quadro.
3. **Tem uma "gramática de filme" própria:** light leak, film burn e flash branco em quase todas as transições. Em 2025, a isso se somam os doodles cor creme e as molduras PiP.
4. **O ritmo desacelera ao longo do vídeo:** o começo é frenético (0,3 a 0,4 s por plano) e o final respira (0,8 a 1,3 s), fechando num momento emocional (concerto, multidão) ou de humor (Deadpool).
5. **Quem é gente real aparece em destaque:** senhora rindo, criança cosplayer, cadeirante, depoimentos legendados ("Já quero voltar no ano que vem!").
6. **Os patrocinadores entram como atração** (McCain, Monster, Nintendo, Kojima Productions, Pokémon), e não como vinheta. Não há cartela "patrocinado por".
7. **O end card é minimalista** (só o logo da edição sobre preto). **Data, CTA e ingresso ficam só na legenda.**
8. **Os hero moments com celebridade saem como peças separadas** (Kojima, com um único plano de drone FPV).
9. **Os grandes números de views estão no YouTube, em comerciais** (887 mil e 1,1 mi, típicos de mídia paga). O aftermovie longo e orgânico de 2023 teve só 56,7 mil views.

## 4. O que a BGS faz MUITO bem

- **Velocidade:** conteúdo no ar no mesmo dia, transformando o evento em curso numa máquina de FOMO e venda.
- **Drone FPV indoor:** dá escala ("maior feira da América Latina") sem precisar de números na tela. O reel do Kojima é praticamente um plano só.
- **Identidade visual consistente:** logo BGS25 com bug, doodles e mascote (o Bot_GS vira colecionável, personagem 3D do CTA e escultura gigante no corte de fita).
- **Diversidade de público** bem escolhida (idosa, crianças, PcD, cosplayers de vários fandoms), o que amplia a percepção de que "a BGS é pra todo mundo".
- **Densidade de atrações por segundo:** o reel B mostra cerca de 15 marcas e ativações em 43 s sem parecer um anúncio.

## 5. Pontos fracos e lacunas que o NXP pode explorar

| Lacuna na BGS | Oportunidade para o NXP |
|---|---|
| Não há aftermovie pós-evento no Instagram em 2023, 2024 nem 2025. O "obrigado" oficial fica no YouTube (56 mil views em 2023) ou vira um Short com 209 views | **Ser dono do "aftermovie de BH"**: publicar em até 48 h, 60 a 90 s, 9:16, com collab post com os criadores e o post fixado no topo do perfil |
| O end card não traz data da próxima edição nem CTA na tela | Fechar com **data do NXP seguinte + "lote 1 / pré-venda" + QR/link**, lido em voz ou em texto grande |
| Não há prova social em números (público, horas, jogos, cosplayers) | Usar **contadores animados estilo HUD** ("+XX mil nerds", "XX horas de jogo") |
| Pouco gameplay e pouco HUD gamer. A estética "filme analógico" é genérica (serve para qualquer festival) | Uma **linguagem gamer/nerd própria**: UI de RPG, barra de XP, "LEVEL UP", transições em pixel e glitch, legendas estilo caixa de diálogo |
| O áudio é trilha genérica e poucos cortes caem no beat (23,5 % no reel A) | **Edição 100 % no beat**, com SFX de game (coin, level up, hit), um trecho de fala marcante como hook e trilha regional |
| As falas de convidados e fãs aparecem sem nome nem lettering de quem é | **Lower thirds** com nome e @ do cosplayer ou convidado (gera marcação e compartilhamento) |
| Não há regionalidade (poderia ser em qualquer pavilhão) | **Orgulho mineiro**: sotaque, "uai", marcos de BH e vista aérea de fora do local no hook |
| O institucional sem gente real vai mal (3,5 mil) | Deixar o institucional como carrossel e **apostar sempre em rosto e reação** |

## 6. Técnicas "roubáveis" (com timestamp de exemplo)

1. **Hook "portões abrindo" com logo no quadro 1** (reel A, 0:00 a 0:01,4): drone/FPV sobre gente correndo pra dentro, com o logo "NXP26" centralizado em overlay. Em 1,5 s o espectador sabe onde está e que está lotado.
2. **Rajada de 3 a 4 quadros com film burn** (reel B, 0:00 a 0:04,5): de 10 a 12 cortes em 4 s, metade no beat, alternando o corredor vazio e o evento cheio (o "antes e depois" da abertura).
3. **Oner de drone FPV num hero moment** (reel C, 0:00 a 0:18): um único plano que atravessa a plateia até o convidado principal ou o corte de fita. Funciona como post separado e dispensa montagem.
4. **Depoimento curto legendado como virada** (reel A, 0:15 a 0:18 e 0:20,4): "Já quero voltar no ano que vem!" vira o CTA de retorno na boca do público. No NXP, fazer a pergunta direto ("Volta ano que vem?") e usar a resposta como penúltimo plano.
5. **Doodle/traço animado e PiP que encolhe** (reel A, 0:03,7 a 0:04,3 e 0:23,3 a 0:23,8): uma camada de identidade barata de replicar em After Effects ou CapCut. No NXP, trocar o doodle por pixel art ou traço de HQ.
6. **Tríptico vertical de arquivo com lettering em duas cores** (reel D, 0:09,9 a 0:17,7): 3 faixas empilhadas no 9:16 com frase curta, palavra-chave na cor da marca. Ótimo para o "X anos de NXP" ou para comparar edições.
7. **Tipografia cinética palavra por palavra + mosaico acelerado** (reel D, 0:20 a 0:26 e 0:29,8 a 0:31,6): "OBRIGADO / POR / FAZER / PARTE" em letras gigantes com blur, seguido de um mosaico de 6 colunas a 0,2 s por quadro, como clímax de retrospectiva.
8. **Mascote como personagem do CTA** (reel D, 0:35,5): o Bot_GS 3D segura o bolo com o texto do convite. O NXP pode criar ou usar um mascote que "anuncia" a data e o lote no end card. É aqui que o NXP supera a BGS, colocando **data e ingresso na tela**.

## 7. Fontes consultadas

- Instagram: https://www.instagram.com/brasilgameshow/ e os reels DPnDhiekhVG, DPpuh9Ej1WU, DPrtqeZAgoc e C8fYkFdJhD7 (baixados). Também foram verificados, mas não servem como recap: DBB4N2IsLq5 (carrossel), DCp5Rc3tu8h (carrossel #TBT), DA84MPsPcLb, DCAP4S8tfeK, DW8qgGtAF99 (venda da BGS26) e DGQxkj4OcPO.
- YouTube (só metadados): Kme0qu-9mFw, EDLgDdMBBF4, RfEay-NdFzE, dE-c5zqj9EM, bvXOkPi5SWQ, NU4_U3oLstI, _t29vbJq6kQ e q8AWGCVRRcA.
- Agência: https://www.whido.com.br/cobertura-oficial-da-bgs24/ (cobertura oficial com same-day edits e cinco vídeos oficiais).
