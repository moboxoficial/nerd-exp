#!/usr/bin/env python3
"""Análise técnica de um vídeo (aftermovie).
Uso: analyze.py <video.mp4> <pasta_saida>
Gera em <pasta_saida>:
  cuts.json      - timestamps de cortes (detecção de cena), duração média de plano por trecho
  sheet_XX.jpg   - contact sheets (1 frame por plano, com timestamp) para leitura visual
  color.json     - brilho/saturação/temperatura média e paleta dominante por trecho
  audio.json     - BPM, curva de loudness (RMS por segundo), picos/drops
  summary.json   - resumo de tudo
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
FF = "ffmpeg"

def run(args):
    return subprocess.run(args, capture_output=True, text=True)

info = run([FF, "-hide_banner", "-i", video]).stderr
dur_m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
duration = int(dur_m.group(1)) * 3600 + int(dur_m.group(2)) * 60 + float(dur_m.group(3))
res_m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", info)
w, h = (int(res_m.group(1)), int(res_m.group(2))) if res_m else (0, 0)
fps_m = re.search(r"([\d.]+) fps", info)

# 1) cortes
r = run([FF, "-hide_banner", "-i", video, "-vf", "select='gt(scene,0.30)',showinfo", "-an", "-f", "null", "-"])
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
bounds = [0.0] + cuts + [duration]
shots = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1) if bounds[i + 1] - bounds[i] > 0.04]
lens = [b - a for a, b in shots]
seg = max(duration / 5, 1)
pacing = []
for i in range(5):
    s, e = i * seg, (i + 1) * seg
    n = sum(1 for c in cuts if s <= c < e)
    pacing.append({"de": round(s, 1), "ate": round(e, 1), "cortes": n,
                   "plano_medio_s": round(seg / (n + 1), 2)})

# 2) frames representativos (meio de cada plano), contact sheets
frames_dir = os.path.join(out, "frames"); os.makedirs(frames_dir, exist_ok=True)
mids = [(a + b) / 2 for a, b in shots]
if len(mids) > 120:  # limita
    idx = np.linspace(0, len(mids) - 1, 120).astype(int); mids = [mids[i] for i in idx]
thumbs = []
for i, t in enumerate(mids):
    fp = os.path.join(frames_dir, f"f{i:03d}.jpg")
    run([FF, "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", "-vf", "scale=240:-2", "-q:v", "4", fp])
    if os.path.exists(fp): thumbs.append((t, fp))
per = 30
for s in range(0, len(thumbs), per):
    chunk = thumbs[s:s + per]
    ims = [Image.open(p).convert("RGB") for _, p in chunk]
    tw, th = ims[0].size; cols = 6; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 16)), "black"); d = ImageDraw.Draw(sheet)
    for k, (im, (t, _)) in enumerate(zip(ims, chunk)):
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        sheet.paste(im, (x, y + 16)); d.text((x + 3, y + 2), f"{int(t//60)}:{t%60:05.2f}", fill="yellow")
    sheet.save(os.path.join(out, f"sheet_{s // per:02d}.jpg"), quality=80)

# 3) cor
def stats(p):
    im = Image.open(p).convert("RGB").resize((64, 64)); a = np.asarray(im).astype(float) / 255
    hsv = np.asarray(im.convert("HSV")).astype(float) / 255
    return a[..., 0].mean() - a[..., 2].mean(), hsv[..., 1].mean(), hsv[..., 2].mean(), a.reshape(-1, 3)
col = []
allpx = []
for t, p in thumbs:
    warm, sat, val, px = stats(p); col.append((t, warm, sat, val)); allpx.append(px)
allpx = np.concatenate(allpx) if allpx else np.zeros((1, 3))
q = (allpx * 5).round().astype(int); keys, cnt = np.unique(q, axis=0, return_counts=True)
top = keys[np.argsort(-cnt)[:8]] / 5
palette = ["#%02x%02x%02x" % tuple((c * 255).astype(int)) for c in top]
color = {"saturacao_media": round(float(np.mean([c[2] for c in col])), 3) if col else None,
         "brilho_medio": round(float(np.mean([c[3] for c in col])), 3) if col else None,
         "temperatura_(R-B)": round(float(np.mean([c[1] for c in col])), 3) if col else None,
         "paleta_dominante": palette}
json.dump(color, open(os.path.join(out, "color.json"), "w"), indent=1)

# 4) áudio
audio = {}
wav = os.path.join(out, "a.wav")
run([FF, "-y", "-i", video, "-vn", "-ac", "1", "-ar", "22050", wav])
if os.path.exists(wav) and os.path.getsize(wav) > 1000:
    import librosa
    y, sr = librosa.load(wav, sr=22050)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    rms = librosa.feature.rms(y=y, hop_length=sr)[0]
    db = 20 * np.log10(rms + 1e-6)
    beat_t = librosa.frames_to_time(beats, sr=sr)
    on_beat = sum(1 for c in cuts if len(beat_t) and np.min(np.abs(beat_t - c)) < 0.08)
    drops = [int(i) for i in np.where(np.diff(db) > 6)[0]]
    silences = [int(i) for i in np.where(db < db.max() - 25)[0]]
    audio = {"bpm": round(float(np.atleast_1d(tempo)[0]), 1),
             "cortes_no_beat_pct": round(100 * on_beat / max(len(cuts), 1), 1),
             "loudness_db_por_segundo": [round(float(x), 1) for x in db],
             "subidas_bruscas_s(drops)": drops, "quedas/silencios_s": silences}
    os.remove(wav)
json.dump(audio, open(os.path.join(out, "audio.json"), "w"), indent=1)

summary = {"arquivo": video, "duracao_s": round(duration, 2), "resolucao": f"{w}x{h}",
           "aspecto": "vertical 9:16" if h > w else ("horizontal" if w > h else "quadrado"),
           "fps": fps_m.group(1) if fps_m else None, "n_planos": len(shots),
           "plano_medio_s": round(float(np.mean(lens)), 2) if lens else None,
           "plano_mais_longo_s": round(float(max(lens)), 2) if lens else None,
           "ritmo_por_quinto": pacing, "cortes_s": [round(c, 2) for c in cuts],
           "cor": color, "audio": {k: v for k, v in audio.items() if k != "loudness_db_por_segundo"}}
json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in summary.items() if k != "cortes_s"}, ensure_ascii=False, indent=1))
