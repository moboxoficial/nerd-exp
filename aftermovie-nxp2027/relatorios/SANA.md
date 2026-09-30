# SANA (Fortaleza): análise dos aftermovies e recaps no Instagram

*Análise feita para o Nerd Experience (NXP, BH) em 30/09/2026.*

## 0. Fontes, handle e limitações

- **Handle oficial:** o perfil indexado é **@sana_fcnb** (as URLs antigas `instagram.com/sana_fcnb/...` continuam valendo). O campo `owner` do embed de todos os posts baixados, porém, retorna **`sana.evento`**. Ou seja, a conta aparentemente foi renomeada para **@sana.evento**. A produção é da FCNB (Fundação Cultural Nipo-Brasileira). No perfil aparecem cerca de 218 mil seguidores (número tirado do snippet de busca).
- O perfil não pôde ser listado: o Instagram devolveu 429/401 e os mirrors estavam bloqueados. As URLs foram achadas com WebSearch restrito a `instagram.com` e validadas pelo `/embed`. Para datar cada post, decodifiquei o ID do shortcode.
- **YouTube bloqueado neste ambiente.** O yt-dlp lê os metadados, mas o googlevideo devolve 403 (o token fica preso a um IP diferente do da saída do proxy), e Piped e Invidious também falharam. Os aftermovies "longos" do YouTube entram só como **metadados**, na seção 5.
- **Não localizado no IG:** o aftermovie oficial do **SANA 2026 Parte 1**. No YouTube ele existe (21/02/2026, 1:53, 86,7 mil views), mas não achei o reel.
- **Localizado mas não baixável:** o aftermovie oficial do **SANA 2025 Parte 1** no IG (`DFkqeXwRdul`, 8.467 views). O embed é GraphVideo, mas vem sem `video_url`, provavelmente por música licenciada ou embed restrito. Em seu lugar analisei o recap oficial da mesma edição (`DFTzb78xv0-`).
- As métricas vêm do embed: `video_view_count` e nº de comentários.

## 1. Vídeos analisados

| # | Post | Edição | Data do post | Duração | Formato | Views (IG) | Coment. | Arquivo |
|---|---|---|---|---|---|---|---|---|
| V1 | https://www.instagram.com/reel/DNlOS9ERowb/ | **Aftermovie oficial** SANA 2025 Parte 2 (#Aftermovie) | 20/08/2025 | 2:08,5 | **16:9 horizontal** 1276×720, 30 fps | 24.883 | 56 | `v1_ig_aftermovie_2025p2.mp4` |
| V2 | https://www.instagram.com/reel/DFTzb78xv0-/ | Recap oficial SANA 2025 Parte 1 (25 anos) | 27/01/2025 (dia seguinte ao fim) | 1:25,7 | 9:16 (360×640 no embed) 24 fps | 15.522 | 163 | `v2_ig_recap_2025p1.mp4` |
| V3 | https://www.instagram.com/reel/DbWdJdulccu/ | Encerramento/save-the-date pós-SANA 2026 Parte 2, anunciando 2027 P1 | 28/07/2026 | 0:14,8 | 9:16 720×960 | 28.243 | **502** | `v3_ig_encerramento_2026p2.mp4` |
| V4 | https://www.instagram.com/reel/DMWfwdvxHv_/ | Recap oficial SANA 2025 Parte 2 | 21/07/2025 (dia seguinte ao fim) | 1:36,7 | 9:16 720×1280 24 fps | 8.246 | 133 | `v4_ig_recap_2025p2.mp4` |

Os dados técnicos brutos estão em `an_v*/summary.json`, `color.json` e `audio.json`, e as contact sheets em `an_v*/sheet_*.jpg`. Frames extras ficam em `xf/`.

### Métricas técnicas (analyze.py)

| | V1 Aftermovie 25P2 | V2 Recap 25P1 | V3 Save-the-date | V4 Recap 25P2 |
|---|---|---|---|---|
| Nº de planos | 149 | 33 | 1 (motion graphic) | 62 |
| Plano médio | **0,86 s** | 2,6 s | 14,8 s | 1,56 s |
| Ritmo por quinto (plano médio) | 0,46 / 0,69 / 1,17 / 0,83 / 0,92 | 1,9 / 3,4 / 1,7 / 1,7 / 5,7 | n/a | 1,07 / 1,29 / 2,76 / 1,29 / 1,76 |
| BPM | 129 | 129 | sem áudio no arquivo | 172 (≈86 half-time) |
| Cortes no beat | 37% | 22% | n/a | 43% |
| Saturação média | 0,42 | 0,36 | 0,81 (duotone) | 0,41 |
| Brilho médio | 0,43 | 0,43 | 0,39 | 0,40 |
| Temperatura (R-B) | +0,02 (neutro/levemente quente) | +0,03 | −0,27 (frio, teal/azul) | +0,03 |
| Silêncios | 45 s (respiro), 119–128 s (fade final) | 34–36 s (respiro), 77 s+ (cartela) | n/a | 96 s (fim) |

## 2. Análise por vídeo

### V1: Aftermovie oficial SANA 2025 Parte 2 (2:08, 16:9)
**Legenda:** "🎬✨ Que fim de semana inesquecível! ... Esse é só um pedacinho da energia ... 📅 O Sana 2026 Parte 1 acontece nos dias 30, 31 de janeiro e 1 de fevereiro de 2026 ... 🎟️ Ingressos já à venda no link da bio!" A legenda promete *memória e emoção* e carrega a **CTA de venda da próxima edição**. Esse CTA não aparece dentro do vídeo. O post saiu **1 mês depois** do evento (20/08). É a versão "cinema", a mesma do YouTube (lá com 676 views).

**Roteiro em blocos**

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:03,4 | **Hook** | Plano baixo de **ônibus escolar** chegando (tema GeekAção). Em seguida, uma **rajada de 12 cortes em ~0,1 s** (2,77→3,40), com cosplays, crianças e mascote. O **logo "PARTE 2 SANA 25" fica fixo no centro**, só a imagem troca por baixo (logo-stutter). |
| 0:03,6–0:14 | **Prova social + vozes** | Um **contador animado de público** sobe sobre planos de multidão: "MAIS DE 31 MIL" → "84 MIL" → "104 MIL PESSOAS" (5,3–6,5 s). Vêm então *vox pops* legendados, curtos e com rostos diversos: "É a minha primeira vez no Ceará", "Sou originalmente do Rio", "Meu primeiro Sana foi em 2012", "Eu sempre trago os meus filhos", "Esse é o meu neto já". Fecha com o **texto cinético** "EVENTO MAIS BONITO DO QUE O OUTRO" (13,4 s). |
| 0:14–0:45 | **Desenvolvimento: atrações** | Parede de escalada Fanta, **câmera 360/tiny planet** (15,4 s) e **POV GoPro na tirolesa** (15,6–16,1 s), arena Monster, autorama, simuladores, reações de torcida e o **painel Smallville** (Tom Welling e Erica Durance, 24–26 s, com lower-thirds). Seguem cenários instagramáveis ("Florescer Espiritual", navio One Piece), K-cover, cosplays em close e Harry Potter com mandrágora. Aos 17 s entra o texto cinético sincronizado com a fala: "1 DIA NUNCA É O SUFICIENTE". |
| 0:45 | **Respiro** | Queda de áudio (−51 dB) e partículas/bolhas no foyer. Marca a virada de tom. |
| 0:46–1:32 | **Bloco institucional (GeekAção/inclusão)** | Escolas na escada rolante, "16 MIL JOVENS" em tipografia, "IN-CLU-SÃO" em três linhas sobre um cadeirante, depoimentos de educadoras, robótica, VR e oficinas. Autoridades discursam no palco ("O Sana é responsável…", "artistas de fora, personagens, marcas"). **O ritmo desacelera para ~1,2 s por plano.** |
| 1:32–1:57 | **Clímax** | Coca-Cola, taekwondo, cosplays heroicos (Superman), shows com luz de palco, **fotos de grupo gigantes de cosplay** e vox pop "Pessoalmente, o Sana é meu favorito" / "Vou voltar nas outras edições". |
| 1:57,9 | **Frase-assinatura** | Convidado japonês diante do painel SANA 25 aponta para a câmera: "Me mostre seu coração valente! / Show me your brave heart!" (legenda bilíngue, citação de anisong de Digimon). |
| 1:59–2:08 | **Encerramento** | Foto de grupo do GeekAção com o texto "Reafirmamos que este é um espaço para sonhar, criar e compartilhar. Obrigado a todos que fazem parte dessa jornada." Fade out com **~9 s de silêncio**. **Não há cartela de data nem de ingresso.** |

**Tipos de plano:** aberto de multidão (alto, sem drone evidente), close de cosplay, reação de público (muita criança e família), palco e shows, painéis de convidados, estandes e ativações (Fanta, Coca-Cola, Monster, Claro), POV/GoPro, 360, handheld em movimento, whip/motion blur (5,3 s). Os closes de cosplay aparentam estar em slow motion. Não há time-lapse.

**Cor:** look natural e limpo, pretos densos, contraste médio-alto, saturação moderada (0,42) e leve calor. Não é LUT "cinema teal-orange". A cor vem da própria cenografia do evento (roxo, rosa e verde neon).

**Grafismo:** bug do logo "SANA 25" no canto o vídeo inteiro. A tipografia é pixel/bitmap (DNA gamer do logo), branca com sombra. Lower-thirds usam **mascote chibi + nome**. Legendas em todas as falas. Contador de público animado.

**VFX:** logo-stutter no hook, texto cinético, bolhas/partículas, 360. Sem glitch pesado e sem light leak evidente.

**Áudio:** trilha eletrônica/pop a ~129 BPM, 37% dos cortes no beat. Os vox pops ficam por cima da trilha como narração coletiva (sem voice-over de locutor). Há respiros de silêncio aos 45 s e no fim.

**Patrocínio:** orgânico, dentro das ativações: Fanta (escalada), Coca-Cola, Monster, Claro e backdrop de painel com logos. Não há cartela de patrocinadores.

### V2: Recap SANA 2025 Parte 1 (1:25, 9:16)
**Legenda:** "O Sana 2025 Parte 1 foi um verdadeiro espetáculo! Com **mais de 81 mil** apaixonados ... Nos dias 18, 19 e 20 de julho ... Parte 2 da celebração dos 25 anos ... uma grande surpresa está à espreita." Combina número de público, data da próxima edição e **teaser de mistério**. O post saiu no dia seguinte ao evento.

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:05 | **Hook** | Sai do preto para um cosplayer "mafioso" (chapéu), em *reveal* lento e olhar para a câmera. Depois, palhaço (It) na escada rolante. |
| 0:05–0:19 | Desfile de cosplays | Corredor cheio de cosplays, plano alto da multidão (12,7 s) e **painel "Programação Geral"** com a galera (16 s). |
| 0:20–0:31 | **Personagem 1** | Maria Lopes, lower-third "Caravana da Fadinha Azul": uma fã mais velha, em cosplay, falando para a câmera. |
| 0:31–0:37 | **Transição/respiro** | Um **anel roxo (íris/portal)** abre sobre o rosto dela (30,6 s) e o áudio cai (−40 dB). |
| 0:37–0:52 | **Personagem 2** | Daiane Pires, cosplayer de Alice jogando **PUBG Mobile no estande** (close de celular, macro), mais o estande Claro. É a história fã → marca. |
| 0:52–1:10 | Montagem | Cosplay fazendo careta para a câmera, **plano aéreo da entrada com ônibus escolares** (55,6 s, drone ou torre), jovens do GeekAção, autorama, show de rock e selfie em grupo de cosplays. |
| 1:10–1:17 | **Apresentador** | Host de camiseta do SANA na porta do pavilhão, falando para a câmera e apontando (convite). |
| 1:17–1:25 | **Cartela CTA** | Logo animado montado letra a letra ("SA" + "N"...), fundo roxo com padrão, raio laranja e rabisco: "SANA 25 PARTE 2 · Dias 18, 19 e 20 de julho de 2025 · **Vendas iniciadas · ticket360.com.br**". |

Ritmo mais lento, puxado pelo depoimento (2,6 s por plano, 22% no beat). Cor com saturação menor (0,36). **É o vídeo com mais comentários (163) entre os recaps.**

### V3: Save-the-date SANA 2027 Parte 1 (0:14,8, 9:16)
**Legenda:** "📅 Pode abrir o calendário e marcar: o Sana 2027 Parte 1 já tem data! 29, 30 e 31 de janeiro de 2027 ... **Qual desses três dias você já está contando?** Marque quem vai ... **#PartiuSana2027**."
- Um único motion graphic: foto de multidão em **duotone teal/azul-marinho** e desfocada, com "2027 PARTE 1" em tipografia grande, uma **barra de loading 02% → 15% → 30%...** e, no fim, "EM BREVE". Datas fixas: "No Centro de Eventos do Ceará · 29, 30 e 31 · Janeiro". A onda verde-água sobe na base.
- O arquivo baixado não tem faixa de áudio (−120 dB). Pode ser música licenciada removida no embed. Não dá para confirmar a trilha.
- **Com um vídeo de 15 s e uma pergunta de engajamento, é o post de maior alcance e conversa do lote: 28 mil views e 502 comentários.**

### V4: Recap SANA 2025 Parte 2 (1:36, 9:16)
**Legenda:** "O Sana 2025 Parte 2 foi INCRÍVEL!!!💥 ... Vem aí o Sana 2026 Parte 1 🗓️ 30, 31 de janeiro e 1 de fevereiro ... 🎟️ Ingressos já à venda no link da bio! Corre e garante o seu!"

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00–0:01,3 | **Hook** | Crianças acenando e gritando para a câmera na entrada (energia imediata). |
| 0:01–0:20 | Chegada e atrações | Mar de gente no pavilhão, **split-screen vertical em 3 faixas** (4,1 / 11,2 / 13,7 s), cosplay, pintura facial, gamers, palco com fumaça, Homem-Aranha, K-cover, Monster (17 s) e Fanta (19 s). |
| 0:20–0:37 | Convidados e reações | Tirolesa, **tríptico do painel Smallville** (22 s) com closes de Tom Welling e Erica Durance, fã de Supergirl, reações, **tríptico do painel de dubladores** (31 s) e cosplays em close. |
| 0:37–0:51 | **Host em plano longo** | Victor Marinho (lower-third com mascote chibi), de camisa SANA 25, fala/canta para a câmera andando pelo evento (13,8 s sem corte). É o fio condutor. |
| 0:51–1:25 | Montagem acelerada | Criança espantada, Power Ranger, show com fumaça, closes extremos de cosplay (olho, maquiagem), Miku, vox pops, whip-blur de multidão (1:10), Sana Games, futebol, autorama, robótica, dublagem ao vivo, **POV da tirolesa** (1:19) e foto do GeekAção. |
| 1:25–1:34 | Host volta | Fechamento falado para a câmera. |
| 1:34–1:36,7 | Assinatura + créditos | O mesmo "Me mostre seu coração valente!" e a **cartela branca de apoios**: Pro Gamers, Ceará, Governo do Ceará, FCNB, Mecenas do Ceará (lei de incentivo), Ministério da Cultura/Governo Federal. |

43% dos cortes caem no beat, com trilha rápida (~172/86 BPM). A cor é a mesma do V1 (mesma equipe/grade).

## 3. O que está no YouTube (não baixado, só metadados)

| Vídeo | Canal | Data | Duração | Views | Obs. |
|---|---|---|---|---|---|
| [SANA 2026 PARTE 1 - AFTERMOVIE](https://www.youtube.com/watch?v=6xL92hJajb4) | SANA oficial | 21/02/2026 | 1:53 | 86.687 | Legenda: "Ainda estamos tentando processar tudo... Conta pra gente nos comentários: qual foi o momento mais inesquecível?" |
| [Sana 2025 Parte 2: Aftermovie](https://www.youtube.com/watch?v=l-MoixOXKHQ) | SANA oficial | 18/09/2025 | 2:08 | 676 | Mesma peça do V1 |
| [Sana 2025 Parte 1: O Aftermovie](https://www.youtube.com/watch?v=NiC9NNlOZqE) | SANA oficial | 02/02/2025 | 1:32 | **401.853** | Mesma peça do IG `DFkqeXwRdul`. As views indicam **mídia paga** |
| [SANA 2024 Parte 2 - Aftermovie](https://www.youtube.com/watch?v=ifDjpR_EhvU) | SANA oficial | 30/07/2024 | 2:43 | **554.146** | Produzido pela **VNS Filmes** (Vinicius Shirahata), também provavelmente impulsionado |

**Leitura:** o SANA **impulsiona o aftermovie no YouTube como anúncio**, a ponto de 400–550 mil views contra menos de 25 mil no IG. No IG orgânico, **o que mais engaja é a peça curta com data e pergunta (V3) e o recap do dia seguinte (V2)**. O aftermovie "cinema" (V1) sai 1 mês depois e rende menos.

## 4. Padrões recorrentes do SANA

1. **Duas peças por edição.** Um *recap vertical* postado **no dia seguinte** (V2, V4), com host, vox pop e CTA da próxima data, e um *aftermovie* mais elaborado semanas depois (V1, 16:9, reaproveitado no YouTube com mídia paga). Depois vem um *save-the-date* curto (V3).
2. **Gente comum como protagonista.** Os vox pops legendados carregam a narrativa: primeira vez, veterano desde 2012, mãe com filho, avó com neto. Não há locutor.
3. **Mascote chibi nos lower-thirds** e tipografia pixel/bitmap coerente com o logo. É um sistema de identidade que se repete em todas as peças.
4. **Número de público como troféu:** contador animado no vídeo (31→84→104 mil) e "mais de 81 mil" na legenda.
5. **Bloco social/institucional** (GeekAção, escolas públicas, inclusão, lei de incentivo). Isso posiciona o evento como política cultural, o que justifica apoio do governo e de marcas.
6. **Ativação de marca filmada como atração** (escalada Fanta, arena Monster, PUBG/Claro), sem cartela de patrocínio no meio. A cartela de apoios aparece só no fim do recap.
7. **Frase-assinatura de convidado** fechando os vídeos ("Me mostre seu coração valente!").
8. **CTA na legenda** (data + "ingressos no link da bio") mais cartela final no recap (datas + site do ingresso).
9. **Cor natural**, sem LUT autoral, com a cenografia colorida fazendo o trabalho.

## 5. O que o SANA faz MUITO bem

- **Velocidade:** o recap está no ar em menos de 24 h, com CTA da próxima edição e ingresso já à venda. Aproveita o pico emocional para vender.
- **Hook de 3 s eficiente (V1):** logo fixo com 12 cortes-relâmpago de cosplay por baixo. Ao mesmo tempo é branding e amostra da variedade.
- **Diversidade de público na tela** (crianças, famílias, 40+, PCD, turistas de fora). Transmite "é pra todo mundo", o que amplia o mercado além do nicho otaku.
- **Narrativa com personagens** (Maria da Caravana da Fadinha Azul, Daiane cosplayer-gamer). Os mini-arcos rendem comentários (V2 com 163).
- **Prova social e tamanho** comunicados sem exagero: contador, planos altos, fotos de grupo gigantes de cosplay.
- **Legitimidade institucional** (GeekAção, 16 mil jovens, inclusão), usada como diferencial e para conseguir apoio público.
- **Save-the-date como jogo:** barra de loading, pergunta e hashtag. Muito engajamento com custo quase zero.

## 6. Pontos fracos e lacunas que o NXP pode explorar

- **O aftermovie principal não tem CTA nem data no vídeo** (V1 termina num fade de 9 s em silêncio). Em repost, story ou compartilhamento, a informação se perde.
- **O aftermovie "cinema" sai 1 mês depois, em 16:9**, dentro de um feed vertical. Perde área de tela e o timing emocional (V1 teve só 56 comentários).
- **Bloco institucional longo** (46 s a 92 s, quase 40% do V1) com discursos de autoridades. O ritmo cai e o vídeo vira relatório de prestação de contas.
- **Sem assinatura visual autoral:** cor neutra, poucos VFX, sem estética anime/manga na edição (speed lines, frames de mangá, onomatopeias). O SANA "documenta" mas não "estiliza".
- **Pouco som diegético e de palco:** a trilha domina. Faltam o grito da plateia, o drop do show ou a fala marcante do convidado como pico sonoro.
- **Pouca exploração de "você poderia estar aqui":** quase não há POV em primeira pessoa contínuo, nem cena de roteiro de visitante (chegada → compra → encontro com ídolo).
- **Qualidade irregular do vertical:** o recap de 2025 P1 está em 360×640 no embed, e os legendados pequenos quase não se leem no celular.

## 7. Técnicas "roubáveis" para o NXP (com exemplo)

| # | Técnica | Onde ver no SANA | Como aplicar no NXP |
|---|---|---|---|
| 1 | **Logo-stutter hook:** logo fixo no centro, 10–15 cortes de 2–3 frames por baixo | V1 0:02,7–0:03,4 | Abrir com "NXP 2026" fixo e 12 closes de cosplay, com o primeiro beat da trilha. |
| 2 | **Contador de público animado** sobre plano aberto | V1 0:05,3–0:06,5 (31→84→104 mil) | "MAIS DE XX MIL NERDS EM BH" sobre plano de multidão ou drone do Expominas. |
| 3 | **Texto cinético saído da fala do vox pop** | V1 0:13,4 ("EVENTO MAIS BONITO DO QUE O OUTRO"), 0:17 ("1 DIA NUNCA É O SUFICIENTE") | Palavras surgem no ritmo da voz, em fonte da marca. Converte depoimento em slogan. |
| 4 | **Lower-third com mascote chibi + nome** | V2 0:20, V4 0:39 | Criar um mascote NXP (vale um toque mineiro) para identificar fãs, hosts e convidados. |
| 5 | **Split-screen vertical em 3 faixas (tríptico)** | V4 0:04,1 / 0:22 / 0:31 | Painel de convidado: plano geral, close do ídolo e reação da plateia ao mesmo tempo. |
| 6 | **Host-fio condutor em plano longo andando pelo evento** | V4 0:37–0:51 e 1:25 | Um creator mineiro conduz o recap com sotaque e humor local, que o SANA não explora. |
| 7 | **POV da atração radical + câmera 360** | V1 0:15,4–0:16,1, V4 1:19 | GoPro na atração de maior impacto do NXP, com tiny-planet de transição. |
| 8 | **Save-the-date com barra de loading + pergunta + hashtag** | V3 inteiro (502 comentários) | "NXP 2027 carregando... 02% → 100%" e "Qual dia você já está contando?" + #PartiuNXP. |
| 9 (bônus) | **Cartela final com data + onde comprar**, que o SANA só faz no recap | V2 1:17–1:25 | Levar isso também ao aftermovie principal, e corrigir a lacuna do V1. |

**Recomendação de formato para o NXP:** usar o modelo de duas peças do SANA (recap vertical em menos de 24 h + aftermovie), mas com o **aftermovie nativo em 9:16** (e um corte 16:9 para o YouTube com mídia paga), CTA dentro do vídeo, bloco institucional de no máximo 10 s e uma camada de estilo anime/mangá na edição. É aí que o SANA não compete.
