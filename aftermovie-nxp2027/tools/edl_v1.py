"""AFTERMOVIE NXP 2027 — 'Além do Portal' — Reel 9:16, 60 s.  EDL v1.
Estrutura amarrada à trilha (Hitman, K. MacLeod, edição 60 s; drop em 37,08 s):
 A 0–2,95 HOOK · B 2,95–5,5 silêncio/portal · C 5,5–9,1 escala · D 9,1–12,4 grito real
 E 12,4–26,3 os 4 mundos · F 26,3–37,1 emoção + cascata de retratos · G 37,1–52,3 DROP/clímax
 H 52,3–60 payoff + CTA
Uso: python3 edl_v1.py [--preview] [--start s --end s] [--out arquivo]"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nxp_engine import *

ap = argparse.ArgumentParser(); ap.add_argument("--preview", action="store_true")
ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float, default=60)
ap.add_argument("--out", default=f"{ROOT}/out/nxp_aftermovie_v1"); ap.add_argument("--noaudio", action="store_true")
ap.add_argument("--novideo", action="store_true")
A = ap.parse_args()
os.makedirs(os.path.dirname(A.out), exist_ok=True)
DUR = 60.0
IDX = json.load(open(f"{ROOT}/raw/player/index.json"))
ORIG = json.load(open(f"{ROOT}/raw/orig/index.json")) if os.path.exists(f"{ROOT}/raw/orig/index.json") else {}
BEATS = json.load(open(f"{ROOT}/audio/musica/hitman_EDIT_60s_emenda.beats.json"))["beats"]
def b(i): return BEATS[i]
def src(code):
    if code in ORIG and "arquivo" in ORIG[code]:
        o = ORIG[code]; return dict(arquivo=o["arquivo"], offset=o["offset"], lut=IDX[code]["lut"], code=code)
    d = IDX[code]; return dict(arquivo=d["arquivo"], offset=0.0, lut=d["lut"], code=code)
SFX = f"{ROOT}/audio/sfx"
KV = f"{ROOT}/kv"

clips, layers, sfx, nat = [], [], [], []
def C(code, t, d, tin, **kw):
    c = Clip(src(code), t, d, tin, name=code, **kw); clips.append(c); return c
import glob as _g
def S(name, at, g=-6):
    m = sorted(_g.glob(f"{SFX}/{name}*.wav")); assert m, name
    sfx.append((m[0], at, g))
def N(code, tin, at, d, g=-8):  # som direto
    if IDX[code].get("audio"): nat.append((src(code)["arquivo"], src(code)["offset"] + tin, at, d, g))
def T(txt, t0, t1, y, size=110, fill=(PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="pop", out="fade", x=W / 2, fontp=None, tracking=0, **kw):
    g = Gfx(text_image(txt, size, fill, glow=glow, fontp=fontp, tracking=tracking), t0, t1, (x, y), inn=inn, out=out, **kw)
    layers.append(g); return g
def IMG(path, t0, t1, pos, scale=1.0, **kw):
    im = Image.open(path).convert("RGBA")
    g = Gfx(im, t0, t1, pos, scale=scale, **kw); layers.append(g); return g

# ============ A · HOOK (0 – 2,95) — o elmo do Guts "acorda", glitch, Motoqueiro Fantasma
C("2025log-0214", 0.0, b(3), 0.0, zoom=(1.18, 1.34), ease="out", cy=0.45)
C("2025log-0215", b(3), b(5) - b(3), 5.0, zoom=(1.25, 1.4), rgb=6, cy=0.4)          # olhos vermelhos
C("2026pix-0542", b(5), 2.95 - b(5), 1.0, zoom=(1.0, 1.12), shake=5, punch=[0.0])
layers += [Hud(0.0, 2.95, "ALERTA: PORTAL INSTÁVEL", "COORD -19.92 / -43.94 · EXPOMINAS"),
           GlitchFx(b(3) - 0.07, b(3) + 0.1, 1.0), GlitchFx(b(5) - 0.05, b(5) + 0.08, 0.8), Flash(b(5), 0.1, PAL["magenta"], 0.6)]
S("sub_01", 0.0, -4); S("ui_03", 0.15, -10); S("glitch_01", b(3) - 0.07, -6); S("impacto_01", b(5), -5)

# ============ B · SILÊNCIO / PORTAL (2,95 – 5,5)
layers.append(Fill(2.95, 5.5, PAL["dark"]))
portal = IMG(f"{KV}/portal_2.png", 2.95, 5.55, (W / 2, H / 2), scale=0.9, inn="zoom_in", tin=0.5, out="zoom_through", tout=0.45,
             mode="screen", grow=0.6, spin=40)
T("OS PORTAIS\nESTÃO ABRINDO", 3.25, 5.1, H / 2, 104, (PAL["white"],), glow=PAL["cyan"], inn="glitch", tin=0.35, out="glitch", tout=0.25)
T("DE NOVO.", 4.1, 5.1, H / 2 + 190, 64, (PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="slide_up", fontp=FONT_BODY, tracking=10)
layers.append(Flash(5.5, 0.16, PAL["white"], 0.95))
S("portal_01", 2.95, -5); S("texto_02", 3.25, -12); S("riser_02", 1.6, -12); S("reverse_01", 4.9, -6); S("whoosh_02", 5.35, -5)

# ============ C · ESCALA (5,5 – 9,1)
C("2025log-0595", 5.5, b(19) - 5.5, 1.0, zoom=(1.0, 1.12), ease="lin", cx=0.55, speed=1.3)
C("2025log-0026", b(19), b(22) - b(19), 2.0, zoom=(1.05, 1.15), punch=[0.0])
C("2025log-0304", b(22), 9.1 - b(22), 1.0, zoom=(1.08, 1.2), punch=[0.0])
layers.append(Gfx(text_image("BELO HORIZONTE · MG", 40, (PAL["white"],), fontp=FONT_BODY, tracking=8), 5.6, b(19), (W / 2, 1640), inn="fade", out="fade"))
layers.append(Counter(b(19), 9.1, 0, 10, "+{} MIL", 190, (W / 2, 820)))
T("NERDS EM 2025", b(20), 9.1, 1000, 72, (PAL["white"],), glow=PAL["violet"], inn="slide_up", fontp=FONT_BODY, tracking=6)
S("whoosh_01", b(19) - 0.1, -8); S("impacto_03", b(22), -8); S("ui_01", b(19), -12)

# ============ D · O GRITO (9,1 – 12,4) — som direto da plateia no respiro da trilha
C("2025log-0454", 9.1, 1.65, 1.0, zoom=(1.1, 1.22), shake=3)
C("2024bru-0444", 10.75, b(30) - 10.75, 51.0, zoom=(1.0, 1.1), shake=3)
N("2025log-0454", 1.0, 9.1, 1.65, -3); N("2024bru-0444", 51.0, 10.75, b(30) - 10.75, -3)
S("plateia_01", 9.1, -12); S("riser_01", b(30) - 4.2, -9)
layers.append(Gfx(text_image("NXP 2025 · 12ª EDIÇÃO", 34, (PAL["white"],), fontp=FONT_BODY, tracking=6), 9.2, 12.2, (W / 2, 1700), inn="fade", out="fade", alpha=0.85))

# ============ E · OS 4 MUNDOS (12,4 – 26,3) — 9 beats por mundo, 4 planos cada
MUNDOS = [
    ("LÓTUS", "cultura asiática · anime · k-pop", (PAL["magenta"], PAL["pink"], PAL["yellow"]), "nuvem.png",
     [("2025log-0063", 2.5, 0.5), ("2025log-0226", 0.5, 0.45), ("2024bru-0295", 3.0, 0.5), ("2026pix-0133", 4.0, 0.5)]),
    ("NEXUS", "cultura pop · cinema · séries", (PAL["cyan"], PAL["violet"]), "sparkle.png",
     [("2025log-0383", 2.5, 0.5), ("2025log-0211", 3.0, 0.5), ("2026pix-0183", 3.5, 0.5), ("2025log-0260", 34.5, 0.6)]),
    ("ELDARION", "medieval · RPG · jogos de mesa", (PAL["yellow"], PAL["green"]), None,
     [("2025log-0535", 0.3, 0.5), ("2026pix-0543", 0.5, 0.5), ("2025log-0100", 1.0, 0.5), ("2025log-0092", 4.0, 0.5)]),
    ("PIXEL", "games · e-sports · tecnologia", (PAL["green"], PAL["cyan"]), None,
     [("2026pix-0062", 0.5, 0.5), ("2026pix-0098", 0.5, 0.5), ("2025log-0570", 7.0, 0.5), ("2024bru-0070", 0.5, 0.5)]),
]
bi = 30
for mi, (nome, sub, cores, icone, planos) in enumerate(MUNDOS):
    t0 = b(bi); lens = [2, 2, 2, 3]
    k = bi
    for (code, tin, cx), n in zip(planos, lens):
        C(code, b(k), b(k + n) - b(k), tin, zoom=(1.06, 1.16), punch=[0.0], cx=cx)
        S("whoosh_04" if (k % 2) else "whoosh_01", b(k) - 0.08, -12)
        k += n
    t1 = b(bi + 9)
    T(nome, t0 + 0.05, t0 + 1.9, 760, 200, cores, glow=PAL["violet"], inn="slam", tin=0.18, out="glitch", tout=0.2, tracking=6)
    T(sub, t0 + 0.25, t0 + 1.9, 905, 46, (PAL["white"],), glow=None, inn="slide_up", fontp=FONT_BODY)
    T(f"MUNDO {mi + 1}/4", t0 + 0.05, t1 - 0.05, 300, 36, (PAL["white"],), glow=None, inn="fade", fontp=FONT_BODY, tracking=10, alpha=0.8)
    layers += [LightLeak(t0 - 0.2, 0.45, side="left" if mi % 2 else "right", peak=0.5), GlitchFx(t0 - 0.04, t0 + 0.06, 0.7)]
    S("impacto_02", t0, -7); S("glitch_03", t0 - 0.04, -10)
    bi += 9
# bi == 66 -> ~26,3 s

# ============ F · EMOÇÃO (26,3 – 33,6) + CASCATA DE RETRATOS (33,6 – 37,08)
t = b(66)
for code, tin, d, sp, cx in [("2025log-0448", 1.0, 1.6, 0.6, 0.5), ("2025log-0489", 0.5, 1.6, 0.5, 0.55),
                              ("2026pix-0267", 0.3, 1.5, 0.7, 0.5), ("2024bru-0453", 1.0, 1.4, 0.8, 0.5), ("2025log-0427", 3.0, 1.2, 0.6, 0.5)]:
    C(code, t, d, tin, speed=sp, zoom=(1.05, 1.14), ease="lin", cx=cx); t += d
T("AQUI, TODO FÃ", b(66) + 0.2, b(66) + 3.1, 1450, 96, (PAL["white"],), glow=PAL["violet"], inn="fade", tin=0.4)
T("ENCONTRA SEU LUGAR", b(66) + 1.4, b(66) + 4.6, 1570, 74, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up", tin=0.4)
S("reverse_02", b(66) - 0.3, -9)
cas_start = t; drop = b(92)  # 37,08
retratos = [("2025log-0216", 0.3), ("2025log-0213", 1.0), ("2025log-0221", 1.0), ("2025log-0218", 0.8), ("2025log-0225", 1.0),
            ("2025log-0019", 8.0), ("2025log-0016", 0.5), ("2025log-0222", 0.5), ("2025log-0217", 1.0), ("2025log-0020", 1.5),
            ("2025log-0226", 2.0), ("2025gav-0024", 1.3), ("2024bru-0123", 0.3), ("2025log-0212", 0.2), ("2025log-0018", 0.2), ("2025log-0214", 0.5)]
n = len(retratos); tot = drop - cas_start
w = np.linspace(1.0, 0.18, n); w = w / w.sum() * tot
tt = cas_start
for (code, tin), d in zip(retratos, w):
    anc = None
    try:
        f = find_face(src(code), tin)
        if f: anc = (f[0], f[1], 0.36 * W / max(f[2], 40))
    except Exception:
        anc = None
    C(code, tt, float(d), tin, zoom=(1.0, 1.04), anchor=anc)
    S("camera_01", tt, -16); tt += float(d)
S("riser_01", drop - 7.8, -6); S("texto_02", cas_start, -14)
layers.append(Gfx(text_image("QUAL É O SEU\nPERSONAGEM?", 64, (PAL["white"],), glow=PAL["violet"], fontp=FONT_BODY), cas_start + 0.1, drop - 0.3, (W / 2, 1640), inn="fade", out="fade", alpha=0.95))

# ============ G · DROP / CLÍMAX (37,08 – 52,3)
layers += [Flash(drop, 0.22, PAL["white"], 1.0), GlitchFx(drop - 0.05, drop + 0.08, 1.0)]
S("sub_02", drop, -2); S("impacto_01", drop, -3); S("plateia_02", drop + 0.1, -13)
seq = [("2024bru-0471", 4.7, 2), ("2025log-0415", 3.3, 1), ("2026pix-0139", 0.3, 2), ("2025log-0471", 0.3, 2), ("2025log-0438", 1.0, 2),
       ("2024bru-0452", 9.7, 2), ("2024bru-0240", 4.0, 2), ("2024bru-0053", 1.5, 2), ("2025log-0454", 3.0, 1), ("2025log-0202", 5.0, 2),
       ("2026pix-0554", 1.0, 2), ("2025log-0415", 16.7, 2), ("2024bru-0444", 12.0, 2), ("2025log-0357", 1.0, 2), ("2025log-0213", 12.0, 1),
       ("2026pix-0185", 3.0, 1), ("2025log-0020", 7.0, 2), ("2024bru-0328", 9.0, 2), ("2025gav-0280", 0.0, 2), ("2024bru-0471", 91.8, 3)]
k = 92
for i, (code, tin, nb) in enumerate(seq):
    t0, t1 = b(k), b(min(k + nb, len(BEATS) - 1))
    if code == "2024bru-0471" and i: t1 = 52.3
    C(code, t0, t1 - t0, tin, zoom=(1.08, 1.2), punch=[0.0] + ([b(k + 1) - t0] if nb > 1 else []), shake=4 if i % 3 == 0 else 0,
      rgb=3 if i % 4 == 1 else 0)
    if i % 2 == 0: layers.append(Flash(t0, 0.07, [PAL["cyan"], PAL["magenta"], PAL["white"]][i % 3], 0.35))
    S("whoosh_03" if i % 2 else "whoosh_02", t0 - 0.06, -14)
    k += nb
PALAVRAS = [("COSPLAY", b(93)), ("PALCOS", b(101)), ("GAMES", b(109)), ("DUBLAGEM", b(117)), ("EXPERIÊNCIAS", b(125))]
cols = [(PAL["magenta"], PAL["pink"]), (PAL["cyan"], PAL["green"]), (PAL["green"], PAL["yellow"]), (PAL["violet"], PAL["cyan"]), (PAL["yellow"], PAL["magenta"])]
for (pal, t0), cc in zip(PALAVRAS, cols):
    T(pal, t0, t0 + 1.5, 1480, 170 if len(pal) < 9 else 132, cc, glow=PAL["dark"], inn="slam", tin=0.12, out="pop", tout=0.15)
    S("impacto_04", t0, -10)
layers.append(Hud(b(125) + 1.6, 52.3, "", "SINAL DO NERDVERSO: 100%"))

# ============ H · PAYOFF + CTA (52,3 – 60)
C("2025log-0594", 52.3, DUR - 52.3, 184.6, zoom=(1.1, 1.25), ease="lin", speed=0.6, cx=0.5)
layers.append(Fill(52.3, DUR, PAL["dark"], alpha=0.72))
layers.append(Flash(52.3, 0.25, PAL["white"], 1.0))
IMG(f"{KV}/portal_1.png", 52.3, DUR, (W / 2, 1040), scale=3.4, inn="zoom_in", tin=0.6, out="fade", mode="screen", spin=25, alpha=0.55)
IMG(f"{KV}/logo_nerdxp_A.png", 52.45, DUR, (W / 2, 420), scale=1.55, inn="pop", tin=0.35, out="fade")
T("O MAIOR EVENTO NERD", 53.0, 56.1, 820, 88, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
g_minas = T("DE MINAS", 53.25, 56.1, 930, 88, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
layers.append(Strike(54.35, 56.1, W // 2 - 230, W // 2 + 230, 930, 20, PAL["magenta"], 0.16))
T("DA GALÁXIA", 54.6, 56.1, 1090, 176, (PAL["violet"], PAL["magenta"], PAL["cyan"]), glow=PAL["magenta"], inn="slam", tin=0.14, out="glitch")
layers += [GlitchFx(54.58, 54.7, 0.9), Flash(54.6, 0.12, PAL["magenta"], 0.5)]
S("marcador_riscando", 54.3, -6); S("impacto_02", 54.6, -3); S("glitch_04", 56.05, -8)
IMG(f"{KV}/alem_do_portal.png", 56.15, DUR, (W / 2, 800), scale=1.25, inn="pop", tin=0.3, out="fade")
T("27 E 28 FEV 2027", 56.4, DUR, 1010, 118, (PAL["green"], PAL["cyan"]), glow=PAL["deep"], inn="slam", tin=0.15)
T("EXPOMINAS · BELO HORIZONTE", 56.6, DUR, 1130, 48, (PAL["white"],), glow=None, inn="slide_up", fontp=FONT_BODY, tracking=5)
T("FEH DUBS  ·  ANDERSON GAVETA", 57.3, DUR, 1290, 50, (PAL["yellow"],), glow=PAL["dark"], inn="fade", fontp=FONT_BODY, tracking=3)
T("JÁ CONFIRMADOS", 57.4, DUR, 1350, 34, (PAL["white"],), glow=None, inn="fade", fontp=FONT_BODY, tracking=10, alpha=0.85)
cta = Image.new("RGBA", (760, 150), (0, 0, 0, 0)); dr = ImageDraw.Draw(cta)
dr.rounded_rectangle((0, 0, 759, 149), 75, fill=(1, 255, 159, 255))
f = font(FONT_DISPLAY, 66); tw = f.getlength("COMENTA INGRESSO"); dr.text(((760 - tw) / 2, 34), "COMENTA INGRESSO", font=f, fill=(41, 24, 51, 255))
layers.append(Gfx(cta, 58.0, DUR, (W / 2, 1560), inn="pop", tin=0.3, out="fade"))
T("e recebe o link do lote", 58.2, DUR, 1680, 40, (PAL["white"],), glow=None, inn="fade", fontp=FONT_BODY)
S("impacto_03", 52.3, -6); S("portal_02", 52.3, -10); S("ui_02", 56.4, -10); S("ui_04", 58.0, -10)

# ---------------------------------------------------------------- render
if not A.novideo:
    render(dict(clips=clips, layers=layers), A.out + "_video.mp4", DUR, finish=Finish(), start=A.start, end=A.end, preview=A.preview)
if not A.noaudio:
    mix_audio(A.out + "_audio.wav", DUR, music=dict(file=f"{ROOT}/audio/musica/hitman_EDIT_60s_emenda.wav", in_s=0.0, gain_db=0, fade_out=0.8),
              sfx=sfx, nat=nat)
if not A.novideo and not A.noaudio and A.start == 0 and A.end == DUR:
    mux(A.out + "_video.mp4", A.out + "_audio.wav", A.out + ".mp4")
json.dump(dict(clips=[dict(code=c.name, t=round(c.t, 3), d=round(c.d, 3), src_in=round(c.src_in, 3)) for c in clips],
               sfx=[(os.path.basename(a), round(t, 3), g) for a, t, g in sfx]), open(A.out + "_edl.json", "w"), indent=1)
print("OK", len(clips), "planos", len(sfx), "sfx", len(nat), "som direto")
