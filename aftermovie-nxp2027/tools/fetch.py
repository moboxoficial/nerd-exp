#!/usr/bin/env python3
"""Busca um trecho de um vídeo do Drive (via relay local) e gera um intermediário já com cor:
 - aplica LUT (nxp_slog3 / nxp_dlogm / nxp_rec709 / none)
 - escala para "cobrir" 2304 px na menor dimensão útil do 9:16 (altura 2304 p/ horizontal)
 - H.264 CRF 14 + AAC, com 1 s de margem antes/depois
Uso: fetch.py <drive_id> <in_s> <dur_s> <lut> <saida.mp4> [rot]
Imprime JSON: arquivo, offset (onde o 'in' pedido começa dentro do intermediário), fps, w, h."""
import json, re, subprocess, sys, os

fid, tin, dur, lut, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
LUTS = os.path.join(os.path.dirname(__file__), "..", "luts")
url = f"http://127.0.0.1:8765/{fid}"
pre = min(1.0, tin)
vf = []
if lut != "none":
    vf.append(f"lut3d={LUTS}/{lut}.cube:interp=tetrahedral")
# cobre um quadro de trabalho 1296x2304 (9:16 com 20% de folga p/ zoom)
vf.append("scale='if(gt(a,1296/2304),-2,1296)':'if(gt(a,1296/2304),2304,-2)':flags=lanczos")
vf.append("format=yuv420p")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-rw_timeout", "60000000",
       "-ss", f"{tin - pre:.3f}", "-i", url, "-t", f"{dur + pre + 1.0:.3f}",
       "-map", "0:v:0", "-map", "0:a:0?", "-vf", ",".join(vf),
       "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0 or not os.path.exists(out):
    print(json.dumps({"erro": r.stderr[-500:]})); sys.exit(1)
info = subprocess.run(["ffmpeg", "-hide_banner", "-i", out], capture_output=True, text=True).stderr
m = re.search(r"Video:.*?, (\d+)x(\d+).*?([\d.]+) fps", info)
print(json.dumps({"arquivo": out, "offset": pre, "w": int(m.group(1)), "h": int(m.group(2)),
                  "fps": float(m.group(3))}))
