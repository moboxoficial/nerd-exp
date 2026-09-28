# 11 — Vídeo, reels e motion

## Especificações

| Peça | Medida | Duração | Obs. |
|---|---|---|---|
| Reels / TikTok / Shorts | 1080×1920, 30 fps (60 para games) | 7–30 s (venda), 30–60 s (conteúdo), 60–90 s (aftermovie curto) | H.264, AAC 48 kHz, ≤ 15 Mbps |
| Capa de reels | 1080×1920 (crop do perfil 1080×1350 central) | — | Título em Genius Techo dentro da faixa central |
| Story animado | 1080×1920 | até 15 s por frame | Texto dentro da zona segura |
| Feed vídeo | 1080×1350 | até 60 s | — |
| Telão/KV animado | 1920×1080 | loop 10–20 s | Portal girando + logo |

## Linguagem de motion NXP

- **Portal**: rotação lenta contínua (8–12 s por volta) + pulso de brilho; na revelação, *zoom-in* atravessando o portal (transição para o próximo plano).
- **Blobs**: deriva lenta (flutuação 2–4% de escala) e morphing; nunca parados em peças animadas.
- **Texto**: entrada por *glitch* rápido (2–4 frames de RGB split) ou *pop* com leve overshoot; palavras destacadas entram por último.
- **Teasers**: interferência/estática, "ERRO 404", cortes secos, som de rádio/falha.
- **Faixas marquee**: rolagem contínua horizontal.
- **Ritmo**: cortes a cada 0,5–1,5 s em reels de hype; 2–4 s em conteúdo explicativo.
- **Legendas queimadas**: Genius Techo ou Lexend Deca Bold, branco com palavra-chave ciano/verde, 2 linhas no máximo, centralizadas no terço inferior (acima de 340 px da base).
- **Encerramento (end card, 1,5–2,5 s)**: logo NERD:XP + além do portal + "27 e 28 | FEV 2027 | EXPOMINAS" + "link na bio".

## Estruturas de roteiro

**Hype de venda (15 s)**: 0–1,5 s gancho visual (portal abrindo / cosplay impactante) + texto "VOCÊ NÃO VAI FICAR DE FORA, NÉ?" → 1,5–10 s montagem rápida (shows, cosplay, arena, K-pop, público) com textos de 2–3 palavras → 10–13 s oferta ("2º LOTE DISPONÍVEL") → 13–15 s end card.

**Revelação de atração (20–30 s)**: interferência + pistas em 3 frases ("Dá vida a personagens…", "Transforma palavras em emoção…") → silêncio/respiro → corte seco para a atração + "ATRAÇÃO CONFIRMADA" → dia + CTA.

**Conteúdo explicativo (30–45 s)**: pergunta na tela ("O QUE É O NEXT LEVEL?") → 3–5 benefícios, um por plano, com ícone → prova (foto do kit) → CTA.

**POV/Trend**: siga o áudio em alta, mas mantenha end card e paleta.

## Receitas técnicas (Mac: `brew install ffmpeg imagemagick`)

Fatiar carrossel panorâmico em slides 1080×1350:
```bash
magick carrossel.png -crop 1080x1350 +repage slide_%02d.png
```

Converter vídeo horizontal em 9:16 com fundo desfocado:
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:a copy out_9x16.mp4
```

Aplicar end card (PNG 1080×1920) nos últimos 2 s:
```bash
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 in.mp4)
ffmpeg -i in.mp4 -i endcard.png -filter_complex "[0][1]overlay=0:0:enable='gte(t,$(echo "$D-2"|bc))'" -c:a copy out.mp4
```

Queimar legendas (SRT) com a fonte da marca:
```bash
ffmpeg -i in.mp4 -vf "subtitles=legenda.srt:force_style='FontName=Lexend Deca,FontSize=14,Bold=1,PrimaryColour=&H00F4F4F4,OutlineColour=&H00331829,Outline=2,Alignment=2,MarginV=180'" out.mp4
```

Exportar para Instagram (compatibilidade máxima):
```bash
ffmpeg -i in.mov -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -b:v 12M -maxrate 15M -bufsize 30M -c:a aac -b:a 192k -ar 48000 -movflags +faststart reels.mp4
```

GIF/loop do portal para stories: exportar do Canva como MP4/GIF (o design suporta mp4 e gif) ou gerar com `ffmpeg -i portal.mp4 -vf "fps=15,scale=540:-1" portal.gif`.

## Ferramentas

- **Canva** (edição rápida, animações de página, export MP4/GIF) — fonte da verdade da identidade.
- **CapCut / Premiere / DaVinci Resolve** para montagem; **After Effects** para portal/glitch mais elaborados.
- Banco de imagens: fotos próprias das edições anteriores (priorizar público real e cosplay).
