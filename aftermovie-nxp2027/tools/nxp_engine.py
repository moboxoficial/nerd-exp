"""Motor de composição do aftermovie NXP (9:16, 1080x1920, 30 fps).

Linha do tempo = lista de Clip (vídeo) + Gfx (grafismos) + Fx globais (flash, glitch) + áudio.
Cada Clip lê um intermediário já com cor (tools/fetch.py) e aplica, quadro a quadro:
speed ramp (com motion blur por acúmulo), crop 9:16 com centro ajustável, zoom com easing,
zoom-punch no beat, shake, split RGB/glitch. Grafismos em PIL/numpy com blend normal/screen.
"""
import math, os, subprocess, json, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
WW, WH = 1296, 2304                       # quadro de trabalho (20% de folga p/ zoom)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DISPLAY = os.path.expanduser("~/.fonts/Righteous.ttf")      # substituta livre de Genius Techno
FONT_BODY = os.path.expanduser("~/.fonts/LexendDeca.ttf")         # fonte oficial do KV
PAL = dict(dark="#291833", deep="#49236c", violet="#bd00fd", magenta="#da05e2", pink="#d352a6",
           cyan="#11fafe", green="#01ff9f", yellow="#f7f080", white="#f4f4f4")

def hex2rgb(h): h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255

# ---------------------------------------------------------------- easing
def ease_out(u): return 1 - (1 - u) ** 3
def ease_in(u): return u ** 3
def ease_io(u): return 3 * u * u - 2 * u * u * u
def back_out(u, s=1.7): u -= 1; return u * u * ((s + 1) * u + s) + 1
EASE = dict(lin=lambda u: u, out=ease_out, inn=ease_in, io=ease_io, back=back_out)

# ---------------------------------------------------------------- vídeo
class Reader:
    """Lê quadros sequenciais (RGB float32) de um intermediário, a partir de start_s."""
    def __init__(self, path, start_s, cx=0.5, cy=0.5, flip=False, lut=None, eq=""):
        info = subprocess.run(["ffmpeg", "-hide_banner", "-i", path], capture_output=True, text=True).stderr
        m = re.search(r"Video:.*?, (\d+)x(\d+).*?([\d.]+) fps", info)
        sw0, sh0, self.fps = int(m.group(1)), int(m.group(2)), float(m.group(3))
        k = max(WW / sw0, WH / sh0)                       # escala "cobrir" o quadro de trabalho
        self.sw, self.sh = max(WW, int(round(sw0 * k / 2) * 2)), max(WH, int(round(sh0 * k / 2) * 2))
        x = int(round((self.sw - WW) * min(max(cx, 0), 1))); y = int(round((self.sh - WH) * min(max(cy, 0), 1)))
        vf = (f"lut3d={ROOT}/luts/{lut}.cube:interp=tetrahedral," if lut else "") + (eq + "," if eq else "") + \
             f"scale={self.sw}:{self.sh}:flags=lanczos,crop={WW}:{WH}:{x}:{y}" + (",hflip" if flip else "")
        self.p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{start_s:.3f}",
                                   "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, bufsize=WW * WH * 3 * 4)
        self.idx = -1; self.cur = None; self.prev = None
    def frame_at_frac(self, kf):
        """índice fracionário: mistura os quadros floor(kf) e floor(kf)+1 (slow-motion suave)."""
        k0 = int(kf); f = kf - k0
        while self.idx < k0 + 1:
            buf = self.p.stdout.read(WW * WH * 3)
            if len(buf) < WW * WH * 3: break
            self.idx += 1; self.prev = self.cur
            self.cur = np.frombuffer(buf, np.uint8).reshape(WH, WW, 3)
        a = self.prev if (self.idx == k0 + 1 and self.prev is not None) else self.cur
        a = a.astype(np.float32) / 255.0
        if self.idx != k0 + 1 or f < 0.1: return a
        return a * (1 - f) + self.cur.astype(np.float32) / 255.0 * f
    def frame_at(self, k):
        """k = índice do quadro-fonte desejado (>= anterior). Faz média dos quadros pulados (motion blur)."""
        acc, n = None, 0
        while self.idx < k:
            buf = self.p.stdout.read(WW * WH * 3)
            if len(buf) < WW * WH * 3: break
            self.idx += 1
            f = np.frombuffer(buf, np.uint8).reshape(WH, WW, 3)
            if k - self.idx < 4:  # acumula até 4 quadros p/ blur
                acc = f.astype(np.float32) if acc is None else acc + f; n += 1
            self.prev = self.cur; self.cur = f
        if n > 1: return acc / (n * 255.0)
        return self.cur.astype(np.float32) / 255.0
    def close(self):
        try: self.p.kill()
        except Exception: pass

class Clip:
    def __init__(self, src, t, d, src_in=0.0, speed=1.0, zoom=(1.0, 1.06), ease="io", cx=0.5, cy=0.5,
                 pan=(0, 0), shake=0.0, punch=(), punch_amt=0.08, rgb=0.0, flip=False, rot=0.0,
                 audio_gain=None, name="", lut=None, eq="", anchor=None):
        self.anchor = anchor  # (ax, ay, escala) no quadro de trabalho -> vai p/ (W/2, 0.42H)
        self.src, self.t, self.d, self.src_in = src["arquivo"], t, d, src["offset"] + src_in
        self.lut, self.eq = lut if lut is not None else src.get("lut"), eq
        self.speed, self.zoom, self.ease, self.cx, self.cy, self.pan = speed, zoom, ease, cx, cy, pan
        self.shake, self.punch, self.punch_amt, self.rgb, self.flip, self.rot = shake, punch, punch_amt, rgb, flip, rot
        self.audio_gain, self.name, self.reader = audio_gain, name, None
        # tabela tempo-de-saída -> tempo-de-fonte (integral da velocidade)
        n = max(int(round(d * FPS)), 1)
        us = (np.arange(n) + 0.5) / n
        sp = np.array([self._speed(u) for u in us])
        self.src_times = np.concatenate([[0], np.cumsum(sp / FPS)])[:n]
        self.span = float(self.src_times[-1] + sp[-1] / FPS)
    def _speed(self, u):
        s = self.speed
        if callable(s): return s(u)
        if isinstance(s, (list, tuple)):  # [(u0,v0),(u1,v1),...] interpolação suave
            for (u0, v0), (u1, v1) in zip(s, s[1:]):
                if u0 <= u <= u1:
                    k = ease_io((u - u0) / max(u1 - u0, 1e-6)); return v0 + (v1 - v0) * k
            return s[-1][1]
        return float(s)
    def _slow(self):
        return self.span < self.d * 0.85
    def open(self):
        if self.reader is None: self.reader = Reader(self.src, self.src_in, self.cx, self.cy, self.flip, self.lut, self.eq)
    def close(self):
        if self.reader: self.reader.close(); self.reader = None
    def render(self, t):
        self.open()
        i = min(int((t - self.t) * FPS + 1e-6), len(self.src_times) - 1)
        kf = self.src_times[i] * self.reader.fps
        img = self.reader.frame_at_frac(kf) if self._slow() else self.reader.frame_at(int(kf + 1e-6))
        u = (t - self.t) / self.d
        z = self.zoom[0] + (self.zoom[1] - self.zoom[0]) * EASE[self.ease](min(max(u, 0), 1))
        for p in self.punch:  # zoom punch: sobe rápido e decai
            dt = t - (self.t + p)
            if 0 <= dt < 0.35: z *= 1 + self.punch_amt * math.exp(-dt * 14)
        sx = sy = 0.0
        if self.shake:
            sx = self.shake * (math.sin(t * 37.1) * 0.6 + math.sin(t * 91.7 + 1.3) * 0.4)
            sy = self.shake * (math.sin(t * 29.3 + 0.7) * 0.6 + math.sin(t * 77.9 + 2.1) * 0.4)
        px, py = self.pan[0] * u, self.pan[1] * u
        s = (W / WW) * z
        ang = self.rot * u + (self.shake * 0.02 * math.sin(t * 23) if self.shake else 0)
        M = cv2.getRotationMatrix2D((WW / 2, WH / 2), ang, s)
        if self.anchor:
            ax, ay, az = self.anchor
            s = max(az * z / self.zoom[0], W / WW * 1.001, H / WH * 1.001)   # nunca menor que "cobrir"
            tx = min(max(W / 2 - ax * s, W - WW * s), 0.0)                    # sem borda aparecendo
            ty = min(max(H * 0.42 - ay * s, H - WH * s), 0.0)
            M = np.array([[s, 0, tx + sx * 0], [0, s, ty]], np.float64)
            ang = 0.0
        else:
            M[0, 2] += W / 2 - WW / 2 + sx + px; M[1, 2] += H / 2 - WH / 2 + sy + py
        out = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if self.rgb: out = rgb_split(out, self.rgb)
        return out

def rgb_split(img, amt):
    o = img.copy(); d = int(amt)
    if d:
        o[:, d:, 0] = img[:, :-d, 0]; o[:, :-d, 2] = img[:, d:, 2]
    return o

def glitch(img, t, amt=1.0, seed=0):
    """Glitch digital: fatias deslocadas + split RGB + blocos em cores do KV."""
    rng = np.random.default_rng(int(t * 1000) + seed)
    o = rgb_split(img, 10 * amt)
    for _ in range(int(6 * amt)):
        y = rng.integers(0, H - 60); h = rng.integers(8, 90); dx = int(rng.integers(-120, 120) * amt)
        o[y:y + h] = np.roll(o[y:y + h], dx, axis=1)
    if amt > 0.6:
        for _ in range(2):
            y = rng.integers(0, H - 40); x = rng.integers(0, W - 300)
            c = hex2rgb([PAL["cyan"], PAL["magenta"], PAL["green"]][rng.integers(0, 3)])
            o[y:y + rng.integers(6, 30), x:x + rng.integers(80, 400)] = c
    return o

# ---------------------------------------------------------------- grafismos
_font_cache = {}
def font(path, size):
    k = (path, size)
    if k not in _font_cache: _font_cache[k] = ImageFont.truetype(path, size)
    return _font_cache[k]

def gradient(w, h, colors, vertical=False):
    cols = [hex2rgb(c) for c in colors]
    n = h if vertical else w
    xs = np.linspace(0, 1, n); seg = len(cols) - 1
    arr = np.zeros((n, 3), np.float32)
    for i, x in enumerate(xs):
        j = min(int(x * seg), seg - 1); f = x * seg - j
        arr[i] = cols[j] * (1 - f) + cols[j + 1] * f
    g = arr[:, None, :].repeat(w, 1) if vertical else arr[None, :, :].repeat(h, 0)
    return (g * 255).astype(np.uint8)

def text_image(txt, size, fill=("#f4f4f4",), fontp=None, stroke=0, stroke_fill="#291833", glow=None,
               tracking=0, vertical_grad=False, pad=40, line_gap=0.95, align="center"):
    """Renderiza texto (multi-linha) em RGBA com preenchimento sólido ou gradiente + glow opcional."""
    f = font(fontp or FONT_DISPLAY, size)
    lines = txt.split("\n")
    widths = []
    for ln in lines:
        wsum = sum(f.getlength(ch) + tracking for ch in ln) - tracking if tracking else f.getlength(ln)
        widths.append(int(wsum))
    asc, desc = f.getmetrics(); lh = int((asc + desc) * line_gap)
    tw, th = max(widths) + 2 * pad, lh * len(lines) + 2 * pad + desc
    mask = Image.new("L", (tw, th), 0); md = ImageDraw.Draw(mask)
    smask = Image.new("L", (tw, th), 0); sd = ImageDraw.Draw(smask)
    for i, ln in enumerate(lines):
        x = pad + (max(widths) - widths[i]) // 2 if align == "center" else pad
        y = pad + i * lh
        if tracking:
            for ch in ln:
                md.text((x, y), ch, font=f, fill=255)
                if stroke: sd.text((x, y), ch, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
                x += f.getlength(ch) + tracking
        else:
            md.text((x, y), ln, font=f, fill=255)
            if stroke: sd.text((x, y), ln, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    if len(fill) == 1:
        col = Image.new("RGB", (tw, th), fill[0])
    else:
        col = Image.fromarray(gradient(tw, th, fill, vertical_grad))
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", (tw, th), glow); gm = mask.filter(ImageFilter.GaussianBlur(size * 0.12))
        g.putalpha(gm.point(lambda v: min(255, int(v * 1.6)))); out = Image.alpha_composite(out, g)
    if stroke:
        s = Image.new("RGBA", (tw, th), stroke_fill); s.putalpha(smask); out = Image.alpha_composite(out, s)
    c = col.convert("RGBA"); c.putalpha(mask); out = Image.alpha_composite(out, c)
    return out

def to_np(img):  # PIL RGBA -> float32 (h,w,4) premultiplicado
    a = np.asarray(img.convert("RGBA")).astype(np.float32) / 255
    a[..., :3] *= a[..., 3:4]
    return a

def composite(dst, src_pm, x, y, alpha=1.0, mode="normal"):
    """Compõe src (premultiplicado) em dst (RGB float) com canto sup-esq em (x,y)."""
    h, w = src_pm.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    s = src_pm[y0 - y:y1 - y, x0 - x:x1 - x] * alpha
    d = dst[y0:y1, x0:x1]
    if mode == "screen":
        d[:] = 1 - (1 - d) * (1 - s[..., :3])
    elif mode == "add":
        d[:] = np.minimum(d + s[..., :3], 1)
    else:
        d[:] = s[..., :3] + d * (1 - s[..., 3:4])

def transform(pm, scale=1.0, rot=0.0):
    if scale == 1.0 and rot == 0.0: return pm
    h, w = pm.shape[:2]
    nw, nh = max(int(w * scale), 1), max(int(h * scale), 1)
    if rot == 0.0:
        return cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA)
    side = int(math.hypot(nw, nh)) + 2
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
    M[0, 2] += side / 2 - w / 2; M[1, 2] += side / 2 - h / 2
    return cv2.warpAffine(pm, M, (side, side), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))

class Gfx:
    """Elemento gráfico. img: PIL RGBA. anim: dict de keyframes simples.
    pos = centro (cx, cy) em px. inn/out = tipos de entrada/saída: fade|pop|slide_up|glitch|wipe|zoom_through"""
    def __init__(self, img, t0, t1, pos=(W / 2, H / 2), scale=1.0, inn="pop", out="fade", tin=0.25, tout=0.2,
                 mode="normal", alpha=1.0, drift=(0, 0), grow=0.0, spin=0.0, flicker=0.0, name=""):
        self.pm = to_np(img) if isinstance(img, Image.Image) else img
        self.t0, self.t1, self.pos, self.scale, self.inn, self.out = t0, t1, pos, scale, inn, out
        self.tin, self.tout, self.mode, self.alpha, self.drift, self.grow, self.spin = tin, tout, mode, alpha, drift, grow, spin
        self.flicker, self.name = flicker, name
    def draw(self, frame, t):
        if not (self.t0 <= t < self.t1): return
        u = (t - self.t0) / max(self.t1 - self.t0, 1e-6)
        a, sc, dx, dy, gl = self.alpha, self.scale * (1 + self.grow * u), self.drift[0] * u, self.drift[1] * u, 0
        ei = (t - self.t0) / self.tin if self.tin else 1
        eo = (self.t1 - t) / self.tout if self.tout else 1
        if ei < 1:
            if self.inn == "fade": a *= ease_out(ei)
            elif self.inn == "pop": sc *= 0.6 + 0.4 * back_out(ei, 2.2); a *= min(1, ei * 2.5)
            elif self.inn == "slide_up": dy += 80 * (1 - ease_out(ei)); a *= ease_out(ei)
            elif self.inn == "glitch": gl = 1 - ei; a *= 1 if int(ei * 12) % 2 else 0.4
            elif self.inn == "zoom_in": sc *= 3.0 - 2.0 * ease_out(ei); a *= ease_out(ei)
            elif self.inn == "slam": sc *= 1.6 - 0.6 * ease_out(ei); a *= min(1, ei * 3)
        if eo < 1:
            if self.out == "fade": a *= max(eo, 0)
            elif self.out == "pop": sc *= 0.7 + 0.3 * eo; a *= eo
            elif self.out == "glitch": gl = 1 - eo; a *= 1 if int(eo * 12) % 2 else 0.3
            elif self.out == "zoom_through": sc *= 1 + 4 * ease_in(1 - eo); a *= eo ** 0.5
        if self.flicker and np.random.rand() < self.flicker: a *= 0.55
        pm = transform(self.pm, sc, self.spin * (t - self.t0))
        if gl > 0:
            pm = pm.copy(); d = int(18 * gl)
            if d: pm[:, d:, 0] = pm[:, :-d, 0]; pm[:, :-d, 2] = pm[:, d:, 2]
        h, w = pm.shape[:2]
        composite(frame, pm, int(self.pos[0] + dx - w / 2), int(self.pos[1] + dy - h / 2), a, self.mode)

class Strike:
    """Risco animado (marcador) sobre um trecho — p/ 'DE MINAS' -> 'DA GALÁXIA'."""
    def __init__(self, t0, t1, x0, x1, y, thick=16, color=PAL["magenta"], dur=0.18):
        self.t0, self.t1, self.x0, self.x1, self.y, self.th, self.c, self.dur = t0, t1, x0, x1, y, thick, hex2rgb(color), dur
    def draw(self, frame, t):
        if not (self.t0 <= t < self.t1): return
        u = min((t - self.t0) / self.dur, 1); xe = int(self.x0 + (self.x1 - self.x0) * ease_out(u))
        cv2.line(frame, (self.x0, self.y), (xe, self.y + 6), tuple(float(v) for v in self.c), self.th, cv2.LINE_AA)

class Counter:
    """Contador animado (ex.: +15 MIL) com easing."""
    def __init__(self, t0, t1, v0, v1, fmt, size, pos, fill=(PAL["cyan"], PAL["green"]), glow=PAL["violet"]):
        self.t0, self.t1, self.v0, self.v1, self.fmt, self.size, self.pos, self.fill, self.glow = t0, t1, v0, v1, fmt, size, pos, fill, glow
        self.cache = {}
    def draw(self, frame, t):
        if not (self.t0 <= t < self.t1): return
        u = min((t - self.t0) / max((self.t1 - self.t0) * 0.6, 1e-6), 1)
        v = int(self.v0 + (self.v1 - self.v0) * ease_out(u))
        if v not in self.cache:
            self.cache[v] = to_np(text_image(self.fmt.format(v), self.size, self.fill, glow=self.glow))
        pm = self.cache[v]; h, w = pm.shape[:2]
        a = min(1, (t - self.t0) / 0.15) * min(1, (self.t1 - t) / 0.15)
        composite(frame, pm, int(self.pos[0] - w / 2), int(self.pos[1] - h / 2), a)

class Hud:
    """Overlay HUD sci-fi (cantoneiras, scanlines, rótulo, coordenadas) — linguagem 'portal instável'."""
    def __init__(self, t0, t1, label="", sub="", color=PAL["cyan"]):
        self.t0, self.t1, self.c = t0, t1, tuple(float(v) for v in hex2rgb(color))
        self.lab = to_np(text_image(label, 44, (color,), fontp=FONT_BODY, tracking=6)) if label else None
        self.sub = to_np(text_image(sub, 30, (PAL["white"],), fontp=FONT_BODY, tracking=3)) if sub else None
        sl = np.zeros((H, W, 4), np.float32); sl[::6, :, :] = [0.02, 0.05, 0.06, 0.10]; self.scan = sl
    def draw(self, frame, t):
        if not (self.t0 <= t < self.t1): return
        a = min(1, (t - self.t0) / 0.12) * min(1, (self.t1 - t) / 0.12)
        m, L, th = 70, 90, 5
        for (x, y, sx, sy) in [(m, m + 120, 1, 1), (W - m, m + 120, -1, 1), (m, H - m - 180, 1, -1), (W - m, H - m - 180, -1, -1)]:
            cv2.line(frame, (x, y), (x + sx * L, y), self.c, th, cv2.LINE_AA)
            cv2.line(frame, (x, y), (x, y + sy * L), self.c, th, cv2.LINE_AA)
        composite(frame, self.scan, 0, 0, a)
        if self.lab is not None and int(t * 6) % 7 != 0:
            composite(frame, self.lab, m - 30, m + 150, a)
        if self.sub is not None:
            composite(frame, self.sub, m - 30, H - m - 290, a)
        if int(t * 2) % 2 == 0:  # "REC" piscando
            cv2.circle(frame, (W - m - 20, m + 180), 12, (1.0, 0.1, 0.3), -1, cv2.LINE_AA)

class Flash:
    def __init__(self, t, d=0.12, color=PAL["white"], peak=0.9, mode="screen"):
        self.t, self.d, self.c, self.peak, self.mode = t, d, hex2rgb(color), peak, mode
    def draw(self, frame, t):
        dt = t - self.t
        if 0 <= dt < self.d:
            a = self.peak * (1 - dt / self.d) ** 1.5
            frame[:] = 1 - (1 - frame) * (1 - self.c * a) if self.mode == "screen" else frame * (1 - a) + self.c * a

class GlitchFx:
    def __init__(self, t0, t1, amt=1.0): self.t0, self.t1, self.amt = t0, t1, amt
    def draw(self, frame, t):
        if self.t0 <= t < self.t1: frame[:] = glitch(frame, t, self.amt)

class Fill:
    """Tela sólida (ex.: preto/roxo do KV) — p/ respiros e cartelas."""
    def __init__(self, t0, t1, color=PAL["dark"], alpha=1.0, fade=0.0, grad=None):
        self.t0, self.t1, self.alpha, self.fade = t0, t1, alpha, fade
        if grad:
            self.img = gradient(W, H, grad, vertical=True).astype(np.float32) / 255
        else:
            self.img = np.ones((H, W, 3), np.float32) * hex2rgb(color)
    def draw(self, frame, t):
        if not (self.t0 <= t < self.t1): return
        a = self.alpha
        if self.fade: a *= min(1, (t - self.t0) / self.fade, (self.t1 - t) / self.fade)
        frame[:] = frame * (1 - a) + self.img * a

class LightLeak:
    """Vazamento de luz animado em cores do KV (blend screen) — transição entre blocos."""
    def __init__(self, t0, d=0.6, colors=(PAL["magenta"], PAL["violet"], PAL["cyan"]), side="left", peak=0.85):
        self.t0, self.d, self.peak, self.side = t0, d, peak, side
        yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
        self.base = []
        for i, c in enumerate(colors):
            cx = (0.1 + 0.4 * i) * W / 4; cy = (0.2 + 0.3 * i) * H / 4
            g = np.exp(-(((xx - cx) / (W / 7)) ** 2 + ((yy - cy) / (H / 6)) ** 2))
            self.base.append((g, hex2rgb(c)))
    def draw(self, frame, t):
        dt = t - self.t0
        if not (0 <= dt < self.d): return
        u = dt / self.d; a = self.peak * math.sin(math.pi * u)
        acc = np.zeros((H // 4, W // 4, 3), np.float32)
        shift = int((u - 0.5) * W / 4 * (1 if self.side == "left" else -1))
        for g, c in self.base: acc += np.roll(g, shift, axis=1)[..., None] * c
        acc = cv2.resize(np.clip(acc * a, 0, 1), (W, H), interpolation=cv2.INTER_LINEAR)
        frame[:] = 1 - (1 - frame) * (1 - acc)

class PortalWipe:
    """Transição 'portal': um anel (asset do KV) cresce do centro; dentro dele aparece o clipe B."""
    def __init__(self, t0, d, ring_img, center=(W / 2, H / 2), spin=90):
        self.t0, self.d, self.c, self.spin = t0, d, center, spin
        self.ring = to_np(ring_img)
    def radius(self, t):
        u = min(max((t - self.t0) / self.d, 0), 1)
        return ease_in(u) * math.hypot(W, H) * 0.75
    def mix(self, a, b, t):
        r = self.radius(t)
        yy, xx = np.ogrid[0:H, 0:W]
        m = np.clip((r - np.sqrt((xx - self.c[0]) ** 2 + (yy - self.c[1]) ** 2)) / 25, 0, 1).astype(np.float32)[..., None]
        out = b * m + a * (1 - m)
        if r > 5:
            rh = self.ring.shape[0]; sc = (2.5 * r) / rh
            pm = transform(self.ring, sc, self.spin * (t - self.t0))
            h, w = pm.shape[:2]
            composite(out, pm, int(self.c[0] - w / 2), int(self.c[1] - h / 2), 1.0, "screen")
        return out

# ---------------------------------------------------------------- pós global
class Finish:
    def __init__(self, grain=0.035, vignette=0.35, seed=1):
        rng = np.random.default_rng(seed)
        self.noise = [rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(8)]
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        v = 1 - vignette * np.clip(r - 0.55, 0, 1) ** 1.6
        tint = hex2rgb(PAL["dark"])
        self.vig = v[..., None]; self.vtint = (1 - v)[..., None] * tint * 0.6
        self.grain = grain
    def apply(self, frame, i):
        frame[:] = frame * self.vig + self.vtint
        n = cv2.resize(self.noise[i % 8], (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
        l = frame.mean(-1, keepdims=True)
        frame[:] = frame + n * self.grain * (0.4 + 0.6 * (1 - np.abs(l - 0.5) * 2))

# ---------------------------------------------------------------- render
def render(timeline, out_path, dur, transitions=(), finish=None, start=0.0, end=None, preview=False):
    """timeline: dict(clips=[Clip], layers=[objetos com draw(frame,t)] em ordem)."""
    clips = sorted(timeline["clips"], key=lambda c: c.t)
    layers = timeline.get("layers", [])
    end = dur if end is None else end
    n0, n1 = int(start * FPS), int(end * FPS)
    ow, oh = (W // 2, H // 2) if preview else (W, H)
    enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "23" if preview else "15", "-preset", "fast" if preview else "slow",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    trans = list(transitions)
    for i in range(n0, n1):
        t = i / FPS
        act = [c for c in clips if c.t <= t < c.t + c.d]
        for c in clips:
            if c.reader and not (c.t <= t < c.t + c.d): c.close()
        if not act:
            frame = np.zeros((H, W, 3), np.float32) + hex2rgb(PAL["dark"])
        elif len(act) == 1:
            frame = act[0].render(t)
        else:
            a, b = act[0], act[1]
            fa, fb = a.render(t), b.render(t)
            tr = next((x for x in trans if x.t0 <= t < x.t0 + x.d), None)
            frame = tr.mix(fa, fb, t) if tr else fb
        for L in layers: L.draw(frame, t)
        if finish: finish.apply(frame, i)
        f8 = (np.clip(frame, 0, 1) * 255).astype(np.uint8)
        if preview: f8 = cv2.resize(f8, (ow, oh), interpolation=cv2.INTER_AREA)
        enc.stdin.write(f8.tobytes())
        if i % 150 == 0: print(f"  frame {i}/{n1}", flush=True)
    enc.stdin.close(); enc.wait()
    for c in clips: c.close()

# ---------------------------------------------------------------- áudio
def mix_audio(out_wav, dur, music=None, sfx=(), nat=(), lufs=-14.0):
    """music: dict(file, in_s, gain_db, fade_in, fade_out). sfx: [(file, at_s, gain_db)].
    nat: [(file, src_in_s, at_s, dur_s, gain_db)] som direto dos clipes."""
    ins, filt, labels = [], [], []
    k = 0
    if music:
        ins += ["-ss", f"{music['in_s']:.3f}", "-t", f"{dur + 0.5:.3f}", "-i", music["file"]]
        fo = music.get("fade_out", 1.5)
        filt.append(f"[{k}:a]aresample=48000,volume={music.get('gain_db', 0)}dB,afade=t=in:d={music.get('fade_in', 0.05)},"
                    f"afade=t=out:st={dur - fo:.3f}:d={fo}[m]"); labels.append("[m]"); k += 1
    for j, (f, at, g) in enumerate(sfx):
        ins += ["-i", f]
        filt.append(f"[{k}:a]aresample=48000,volume={g}dB,adelay={int(at * 1000)}|{int(at * 1000)}[s{j}]"); labels.append(f"[s{j}]"); k += 1
    for j, (f, sin, at, d, g) in enumerate(nat):
        ins += ["-ss", f"{sin:.3f}", "-t", f"{d:.3f}", "-i", f]
        filt.append(f"[{k}:a]aresample=48000,volume={g}dB,afade=t=in:d=0.03,afade=t=out:st={max(d - 0.08, 0):.3f}:d=0.08,"
                    f"adelay={int(at * 1000)}|{int(at * 1000)}[n{j}]"); labels.append(f"[n{j}]"); k += 1
    filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,"
                f"atrim=0:{dur},alimiter=limit=0.95,loudnorm=I={lufs}:TP=-1.0:LRA=9[out]")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + ins + ["-filter_complex", ";".join(filt),
           "-map", "[out]", "-ar", "48000", "-ac", "2", out_wav]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-1500:])

def mux(video, audio, out):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-i", audio, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)

# ---------------------------------------------------------------- rosto (alinhamento da cascata)
_yunet = None
def find_face(src, t_in, cx=0.5, lut=None):
    """Detecta o maior rosto no quadro de trabalho em t_in. Retorna (olho_x, olho_y, largura_rosto) ou None."""
    global _yunet
    r = Reader(src["arquivo"], src["offset"] + t_in, cx, 0.5, False, lut if lut is not None else src.get("lut"))
    f = (r.frame_at(0) * 255).astype(np.uint8); r.close()
    if _yunet is None:
        _yunet = cv2.FaceDetectorYN.create(f"{ROOT}/models/yunet.onnx", "", (WW, WH), 0.6)
    _yunet.setInputSize((WW, WH))
    _, faces = _yunet.detect(cv2.cvtColor(f, cv2.COLOR_RGB2BGR))
    if faces is None or len(faces) == 0: return None
    fc = max(faces, key=lambda a: a[2] * a[3])
    ex = (fc[4] + fc[6]) / 2; ey = (fc[5] + fc[7]) / 2
    return float(ex), float(ey), float(fc[2])
