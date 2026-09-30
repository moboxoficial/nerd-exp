"""Para cada clipe baixado: frames a cada 'step' s (com LUT de preview) + métricas de nitidez e movimento.
Gera raw/sheets/<code>.jpg (tira com timestamps) e raw/metrics.json."""
import json, os, subprocess, sys, glob
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
S = os.environ.get('NXP_WORK', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
idx = json.load(open(f'{S}/raw/player/index.json'))
os.makedirs(f'{S}/raw/sheets', exist_ok=True)
F = ImageFont.truetype(os.path.expanduser('~/.fonts/LexendDeca.ttf'), 14)
mpath = f'{S}/raw/metrics.json'
metrics = json.load(open(mpath)) if os.path.exists(mpath) else {}
codes = sys.argv[1:] or list(idx)
for code in codes:
    d = idx.get(code)
    if not d or 'arquivo' not in d or code in metrics: continue
    dur = d['dur']; step = 0.5 if dur <= 12 else (1.0 if dur <= 40 else dur / 40)
    lut = d['lut']
    vf = (f"lut3d={S}/luts/{lut}.cube," if lut else "") + f"fps={1/step},scale=-2:180"
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', d['arquivo'], '-vf', vf,
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    ww = int(round(180 * d['w'] / d['h'] / 2) * 2)
    n = len(p.stdout) // (ww * 180 * 3)
    if n == 0: continue
    fr = np.frombuffer(p.stdout[:n * ww * 180 * 3], np.uint8).reshape(n, 180, ww, 3)
    sharp = [float(cv2.Laplacian(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var()) for f in fr]
    mot = [0.0] + [float(np.abs(fr[i].astype(int) - fr[i - 1].astype(int)).mean()) for i in range(1, n)]
    metrics[code] = dict(step=step, sharp=sharp, motion=mot, dur=dur)
    cols = min(n, 12); rows = (n + cols - 1) // cols
    sh = Image.new('RGB', (cols * ww, rows * 200), 'black'); dr = ImageDraw.Draw(sh)
    for i, f in enumerate(fr):
        x, y = (i % cols) * ww, (i // cols) * 200
        sh.paste(Image.fromarray(f), (x, y)); dr.text((x + 3, y + 182), f"{i*step:.1f}s s{int(sharp[i])} m{mot[i]:.0f}", fill='yellow', font=F)
    dr.text((4, 4), code, fill='white', font=F)
    sh.save(f'{S}/raw/sheets/{code}.jpg', quality=75)
    json.dump(metrics, open(mpath, 'w'))
    print(code, n, flush=True)
