# Aftermovies de CCXP, BGS, SANA e NXP: análise comparativa

Objetivo: entender o que os concorrentes fazem nos aftermovies do Instagram e aplicar isso ao aftermovie de venda do **NXP 2027 · Além do Portal** (27 e 28 fev 2027, Expominas).

Método: 4 agentes baixaram os reels públicos via embed do Instagram (18 vídeos no total) e rodaram `tools/analyze.py`, que mede cortes, duração média de plano, ritmo por trecho, cor, BPM, cortes no beat e loudness. Depois leram os contact sheets quadro a quadro. Os relatórios completos, com tabelas e timestamps, estão em `relatorios/`.

> **Limitações:** o Instagram não deixa listar perfis a partir da nuvem (erros 429/login), então os vídeos vieram de busca na web. O YouTube bloqueou todos os downloads (403/bot-check); os aftermovies longos de lá entraram só com metadados. Nenhum áudio foi *ouvido*: a análise de trilha é por BPM e curva de energia.

---

## 1. Resumo por evento

| | **CCXP** (@ccxpoficial) | **BGS** (@brasilgameshow) | **SANA** (@sana.evento) | **NXP** (@nerdexperience) |
|---|---|---|---|---|
| Vídeos analisados | 6 (aftermovie 24, "Anatomia", encerramento 25, MX ×2, teaser 26) | 4 (recaps diários BGS25, Kojima, 15 anos) | 4 (aftermovie 25-P2, recaps 25-P1/P2, save-the-date 27) | 30 baixados, 9 com evento real (aftermovie 12ª ed., teaser MS, retrospectiva) |
| Formato principal | 16:9 · 2:35 no Reels (!) + recap vertical de 22 s | 9:16 · ~45 s, feito **no mesmo dia** (agência Whido) | Recap 9:16 em até 24 h + aftermovie 16:9 um mês depois | 9:16 · ~60–70 s |
| Plano médio | 0,62–0,64 s nos trechos rápidos | 0,31–0,77 s | 0,46–1,17 s | lento, só 17% dos cortes no beat |
| Trilha | épica ~99 BPM, 45% dos cortes no beat | ~129 BPM, 23–50% no beat | ~129 BPM, 22–43% no beat | — |
| Hook (0–2 s) | FPV com boneco do Goku "voando" | drone sobre a multidão + logo no 1º frame | logo fixo + 12 cortes-relâmpago de cosplay | **letreiros** (fraco) |
| Narrativa | "multiverso / portal / nossos mundos vão se encontrar" + narrador | energia pura, depoimento "volto ano que vem" | depoimentos legendados (1ª vez, veterano, mãe e filho) | arco painel → show |
| Números na tela | só no MX ("40.000 m² de fandom") | nenhum | contador animado 31 → 104 mil | nenhum |
| CTA final | data + site, cartela de 5–10 s | **nenhum** na tela (só na legenda) | nenhum no aftermovie principal (fade de 9 s mudo) | 12 s de cartela "CONHEÇA", sem data nem ingresso |
| Marcas | cenário (BR) · "Banamex presenta" (MX) | ~15 marcas como atração | Fanta, Monster, Claro como atração | Fanta, Claro, PUC (pouco) |

## 2. O que todos fazem bem, e o NXP também precisa ter

1. **Hook visual sem texto em menos de 2 s.** FPV (CCXP), drone (BGS), rajada de cortes (SANA).
2. **O rosto do público como conteúdo.** Destaque para a "cascata de retratos" da CCXP (≈55 retratos de 2 frames, olhos alinhados, entrando no drop), o post de maior engajamento analisado (68 mil plays, 886 comentários).
3. **Uma palavra gigante por plano, no beat**, dizendo o que o evento é (CCXP "Anatomia": FILME / SÉRIE / ANIME / COSPLAY).
4. **Aceleração até ~60% do vídeo e respiro emocional no fim.**
5. **Mesmo mote em todas as peças.** Na CCXP, "portal/multiverso", que é justamente o território do KV do NXP ("Além do Portal").

## 3. As lacunas que o NXP pode ocupar

| Lacuna dos concorrentes | Como o aftermovie NXP responde |
|---|---|
| Ninguém fecha o aftermovie com **data + local + CTA de ingresso na tela** | Cartela final com **27 e 28 FEV 2027 · Expominas · "COMENTA INGRESSO"** (mecânica que o NXP já usa no feed) |
| Aftermovies longos em 16:9, ruins no Reels | **9:16 nativo, 60 s + corte de 30 s** para anúncio |
| Quase nenhum número de escala no Brasil | Contador animado "+10 MIL NERDS" |
| Pouca identidade de marca na edição (BGS/SANA usam look genérico) | Look e grafismos 100% do KV: roxo #291833, neon ciano/verde/magenta, portal, HUD "portal instável" |
| Tom só épico | Mistura de épico com humor (o "DE ~~MINAS~~ DA GALÁXIA" do storyboard da campanha) |
| Som ambiente sufocado pela trilha (SANA) | Respiro da trilha preenchido com o **grito real da plateia** (som direto) |
| Estrela no centro (CCXP depende de celebridades) | O **fã e o cosplayer** como protagonistas: cascata de retratos + os 4 mundos |

## 4. Técnicas roubadas e onde entram no nosso corte

| Técnica | Referência | No aftermovie NXP |
|---|---|---|
| Hook sem texto com personagem forte | CCXP24 0:00 (FPV Goku) | 0:00: elmo do Guts (Berserk) "acorda", olhos vermelhos, glitch |
| Portal como transição de mundo | CCXP24 0:13 e 2:25 | 0:03: portal do KV cresce e engole a tela ("OS PORTAIS ESTÃO ABRINDO") |
| Drone de escala + contador | BGS Dia 1 0:00 · SANA V1 0:05 | 0:05: drone Minas Shopping lotado → "+10 MIL NERDS" |
| Som direto no respiro | lacuna do SANA | 0:09: grito real da grade do palco |
| Blocos temáticos no beat | CCXP "Anatomia" | 0:12: LÓTUS / NEXUS / ELDARION / PIXEL, 4 planos cada |
| Cascata de retratos alinhados | CCXP25 encerramento 0:05–0:15 | 0:33: 16 retratos com olhos alinhados por detecção de rosto, acelerando até o drop |
| Palavra gigante por beat | CCXP "Anatomia" 0:46 | 0:37: COSPLAY / PALCOS / GAMES / DUBLAGEM / EXPERIÊNCIAS |
| Logo da edição → próxima + data | CCXP25 0:16 | 0:52: NERD XP → "o maior evento nerd de ~~Minas~~ DA GALÁXIA" → Além do Portal · 27 e 28 fev 2027 |
| Save-the-date barato | SANA V3 | corte de 30 s + cartela reaproveitável |

## 5. Crítica dos aftermovies antigos do próprio NXP

- **12ª edição (2025):** tem a melhor captação do acervo, mas abre com letreiros em vez de emoção, perde energia entre 31 e 46 s, não mostra escala (nem drone, nem número) e termina com 12 s de cartela muda sem data.
- **Retrospectiva 2018–22:** o melhor roteiro ("vocês estavam lá!" + data no fim), mas legendas cobrem quase todos os planos.
- **Teaser Minas Shopping:** o melhor modelo de venda que o NXP já fez: cortes rápidos, cartelas de atração e "save the date".
- **Feed 2026/27:** quase só estúdio. O que vende é o evento real e o público, e é isso que este aftermovie coloca de volta.
