# Aftermovie de venda do NXP 2027 · "Além do Portal"

Reel **9:16, 1080×1920, 30 fps, 60 s** (+ corte de 30 s), para vender o **Nerd XP Pop Festival 2027**, **27 e 28 de fevereiro de 2027, Expominas (BH)**.
Feito com os brutos do Drive (NXP 2024, 2025 e Pixel 2026), a ID visual do Canva ("NXP 2027") e uma trilha e SFX com licença livre.

- `ANALISE_CONCORRENCIA.md`: o que CCXP, BGS, SANA e o próprio NXP fazem nos aftermovies do Instagram, e o que aproveitamos.
- `relatorios/`: relatórios completos por evento (tabelas, timestamps e métricas).
- `ROTEIRO.md`: roteiro/EDL segundo a segundo (planos, grafismos, VFX e SFX).
- `tools/`: pipeline que gera o vídeo (reprodutível).
- `LICENCAS.md`: trilha e SFX, com licença e crédito exigido.

## Pipeline

1. **Inventário do Drive.** As pastas são públicas por link. `drive_crawl.py` varreu as 18 pastas e achou 10.691 arquivos, 5.557 deles vídeos.
2. **Triagem visual.** `thumbs.py` + `sheets.py` baixaram 2.381 miniaturas (2024, 2025 e 2026) sem gastar cota de download. Três agentes leram as 63 pranchas e escolheram 172 candidatos, 136 com nota ≥ 4.
3. **Download.** `fetch_player.py` baixou os 74 escolhidos pelo stream do player do Drive (até 1080p). O download direto dos originais esbarra na cota anônima do Drive ("Quota exceeded").
4. **Escolha fina.** `clip_sheet.py` gera tiras de frames a cada 0,5 s com nitidez e movimento, e os pontos de entrada foram escolhidos a partir delas.
5. **Cor.** A câmera principal de 2025 é uma **Sony A6400 em S-Log3 / S-Gamut3.Cine** (lido no XML do arquivo). Usamos a LUT oficial da Sony que estava na pasta `_LUTs` da equipe (SLog3SGamut3.Cine → LC-709TypeA), composta com o look NXP (`make_luts.py`):
   - contraste S suave;
   - vibrance;
   - sombras puxadas para o roxo do KV (#291833 / #49236c);
   - altas levemente ciano (#11fafe);
   - pretos matte roxos;
   - roll-off de altas.
6. **Composição.** `nxp_engine.py` + `edl_v1.py` fazem toda a composição em Python/OpenCV:
   - crop 9:16 com folga de 20%, zoom com easing, zoom-punch no beat, shake;
   - speed ramp com interpolação;
   - glitch e split RGB, light leaks nas cores do KV, flashes;
   - HUD sci-fi, portal do KV em blend screen, contador animado, risco de marcador;
   - cascata de retratos com **olhos alinhados por detecção de rosto (YuNet)**;
   - grão e vinheta roxa.
7. **Áudio.** `mix_audio` junta trilha, 92 SFX posicionados na timeline e som direto da plateia, e normaliza para −14 LUFS / −1 dBTP, o padrão do Instagram.

Para regenerar: `python3 tools/edl_v1.py` (60 s) e `python3 tools/edl_30s.py` (30 s), com `--preview` para meia resolução. Renderizar 60 s leva cerca de 35 min em 4 núcleos.

## Entregas (fora do git: `entrega/*.mp4` está no .gitignore)

| Arquivo | Uso |
|---|---|
| `NXP2027_aftermovie_60s_master.mp4` | master 1080×1920, ~14 Mbps, −13,7 LUFS: subir no Reels |
| `NXP2027_aftermovie_60s.mp4` | 27 MB (2 passes, 3,5 Mbps): envio/WhatsApp/aprovação |
| `NXP2027_aftermovie_30s_master.mp4` / `_30s.mp4` | corte de anúncio: master e versão de 25 MB |

## Pendências antes de subir como anúncio

- [ ] **Confirmar os números e nomes na tela**:
  - "+10 MIL NERDS EM 2025" (fonte: imprensa, ~10 mil na 12ª edição);
  - "NXP 2025 · 12ª EDIÇÃO";
  - "FEH DUBS · ANDERSON GAVETA JÁ CONFIRMADOS" (fonte: carrossel do Canva).
- [ ] **Fontes:** no vídeo, a Genius Techno do KV foi substituída pela Righteous (livre). A Genius Techno é demo "personal use"; para usar a original é preciso licença comercial. A Lexend Deca é a oficial.
- [ ] **Resolução:** o material vem do stream 1080p do Drive, e o crop 9:16 de plano horizontal amplia ~1,8×. Para a versão final, rodar de novo `fetch.py` nos originais 4K quando a cota do Drive liberar, ou baixar pelo Drive com login. Nenhuma edição muda, só a fonte.
- [ ] **Crédito da trilha na legenda do post:** "Hitman" – Kevin MacLeod (incompetech.com), licença CC BY 4.0. Ver `LICENCAS.md`.
- [ ] **Autorização de imagem:** os cosplayers e o público em close aparecem em material do próprio NXP; conferir o termo de uso de imagem do credenciamento.
