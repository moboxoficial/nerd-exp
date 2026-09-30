"""AFTERMOVIE NXP 2027 — corte de 30 s para anúncio pago (9:16).
Trilha: Hitman (K. MacLeod), edição 30 s — drop em ~18,41 s.
 A 0–3,1 hook · B 3,1–7,6 escala + mundos relâmpago · C 7,6–14,4 emoção · D 14,4–18,41 cascata
 E 18,41–25,2 clímax · F 25,2–29,75 payoff + CTA"""
import sys, os, json, argparse, glob as _g
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nxp_engine import *

ap = argparse.ArgumentParser(); ap.add_argument("--preview", action="store_true")
ap.add_argument("--out", default=f"{ROOT}/out/nxp_aftermovie_30s_v1"); ap.add_argument("--novideo", action="store_true")
A = ap.parse_args()
DUR = 29.75
IDX = json.load(open(f"{ROOT}/raw/player/index.json"))
BEATS = json.load(open(f"{ROOT}/audio/musica/hitman_EDIT_30s_emenda.beats.json"))["beats"]
def b(i): return BEATS[i]
def src(code): d = IDX[code]; return dict(arquivo=d["arquivo"], offset=0.0, lut=d["lut"], code=code)
SFX, KV = f"{ROOT}/audio/sfx", f"{ROOT}/kv"
clips, layers, sfx, nat = [], [], [], []
def C(code, t, d, tin, **kw): c = Clip(src(code), t, d, tin, name=code, **kw); clips.append(c); return c
def S(name, at, g=-6): sfx.append((sorted(_g.glob(f"{SFX}/{name}*.wav"))[0], at, g))
def T(txt, t0, t1, y, size=110, fill=(PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="pop", out="fade", fontp=None, tracking=0, **kw):
    g = Gfx(text_image(txt, size, fill, glow=glow, fontp=fontp, tracking=tracking), t0, t1, (W / 2, y), inn=inn, out=out, **kw); layers.append(g); return g
def IMG(path, t0, t1, pos, scale=1.0, **kw):
    g = Gfx(Image.open(path).convert("RGBA"), t0, t1, pos, scale=scale, **kw); layers.append(g); return g

# A · HOOK
C("2025log-0214", 0.0, b(1), 0.0, zoom=(1.2, 1.34), ease="out", cy=0.45)
C("2025log-0215", b(1), b(3) - b(1), 5.0, zoom=(1.25, 1.4), rgb=6, cy=0.4)
C("2026pix-0542", b(3), b(5) - b(3), 1.0, zoom=(1.0, 1.12), shake=5, punch=[0.0])
layers += [Hud(0, b(5), "ALERTA: PORTAL INSTÁVEL", "COORD -19.92 / -43.94 · EXPOMINAS"), GlitchFx(b(1) - 0.06, b(1) + 0.08, 1.0),
           Flash(b(3), 0.1, PAL["magenta"], 0.6)]
layers.append(Fill(b(5), b(6), PAL["dark"]))
IMG(f"{KV}/portal_2.png", b(5), b(6) + 0.1, (W / 2, H / 2), scale=1.0, inn="zoom_in", tin=0.2, out="zoom_through", tout=0.2, mode="screen", spin=60)
T("OS PORTAIS\nESTÃO ABRINDO", b(5) + 0.02, b(6), H / 2, 100, (PAL["white"],), glow=PAL["cyan"], inn="glitch", tin=0.15, out="glitch", tout=0.1)
layers.append(Flash(b(6), 0.14, PAL["white"], 0.95))
S("sub_01", 0, -4); S("glitch_01", b(1) - 0.06, -6); S("impacto_01", b(3), -5); S("portal_01", b(5), -6); S("whoosh_02", b(6) - 0.1, -5)
# B · ESCALA + MUNDOS RELÂMPAGO
C("2025log-0595", b(6), b(8) - b(6), 1.0, zoom=(1.0, 1.1), cx=0.55, speed=1.3)
C("2025log-0304", b(8), b(10) - b(8), 1.0, zoom=(1.08, 1.2), punch=[0.0])
layers.append(Counter(b(6), b(10), 0, 10, "+{} MIL", 180, (W / 2, 820)))
T("NERDS EM 2025", b(7), b(10), 1000, 70, (PAL["white"],), glow=PAL["violet"], inn="slide_up", fontp=FONT_BODY, tracking=6)
rel = [("2025log-0063", 2.5, "LÓTUS", (PAL["magenta"], PAL["pink"])), ("2024bru-0295", 3.0, None, None),
       ("2025log-0383", 2.5, "NEXUS", (PAL["cyan"], PAL["violet"])), ("2026pix-0183", 3.5, None, None),
       ("2025log-0535", 0.3, "ELDARION", (PAL["yellow"], PAL["green"])), ("2026pix-0543", 0.5, None, None),
       ("2026pix-0062", 0.5, "PIXEL", (PAL["green"], PAL["cyan"])), ("2025log-0570", 7.0, None, None)]
k = 10
for code, tin, nome, cores in rel:
    t0 = b(k); t1 = b(k + 1) if k + 1 < 18 else 7.6
    C(code, t0, t1 - t0, tin, zoom=(1.08, 1.16), punch=[0.0])
    if nome:
        T(nome, t0, b(k + 2) if k + 2 <= 18 else 7.6, 780, 190, cores, glow=PAL["violet"], inn="slam", tin=0.1, out="glitch", tout=0.1, tracking=6)
        S("impacto_04", t0, -9)
    else:
        S("whoosh_04", t0 - 0.05, -13)
    k += 1
C("2024bru-0070", b(18), 7.6 - b(18), 0.5, zoom=(1.08, 1.16))
# C · EMOÇÃO (7,6 – 14,4)
t = 7.6
for code, tin, d, sp in [("2025log-0448", 1.0, 2.2, 0.6), ("2025log-0489", 0.5, 2.3, 0.5), ("2026pix-0267", 0.3, 2.3, 0.7)]:
    C(code, t, d, tin, speed=sp, zoom=(1.05, 1.14), ease="lin"); t += d
T("AQUI, TODO FÃ", 7.8, 12.0, 1450, 96, (PAL["white"],), glow=PAL["violet"], inn="fade", tin=0.4)
T("ENCONTRA SEU LUGAR", 9.0, 14.2, 1570, 74, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up", tin=0.4)
S("reverse_02", 7.3, -9)
# D · CASCATA (14,4 – 18,41)
drop = b(44)
ret = [("2025log-0216", 0.3), ("2025log-0213", 1.0), ("2025log-0221", 1.0), ("2025log-0218", 0.8), ("2025log-0225", 1.0), ("2025log-0019", 8.0),
       ("2025log-0016", 0.5), ("2025log-0222", 0.5), ("2025log-0217", 1.0), ("2025log-0020", 1.5), ("2025log-0226", 2.0), ("2025gav-0024", 1.3),
       ("2024bru-0123", 0.3), ("2025log-0212", 0.2), ("2025log-0018", 0.2), ("2025log-0214", 0.5)]
w = np.linspace(1.0, 0.18, len(ret)); w = w / w.sum() * (drop - t); tt = t
for (code, tin), d in zip(ret, w):
    f = find_face(src(code), tin); anc = (f[0], f[1], 0.36 * W / max(f[2], 40)) if f else None
    C(code, tt, float(d), tin, zoom=(1.0, 1.04), anchor=anc); S("camera_01", tt, -16); tt += float(d)
S("riser_01", drop - 7.8, -6)
layers.append(Gfx(text_image("QUAL É O SEU\nPERSONAGEM?", 64, (PAL["white"],), glow=PAL["violet"], fontp=FONT_BODY), t + 0.1, drop - 0.3, (W / 2, 1640), inn="fade", out="fade"))
# E · CLÍMAX (drop – 25,2)
layers += [Flash(drop, 0.22, PAL["white"], 1.0), GlitchFx(drop - 0.05, drop + 0.08, 1.0)]
S("sub_02", drop, -2); S("impacto_01", drop, -3); S("plateia_02", drop + 0.1, -13)
seq = [("2024bru-0471", 4.7, 2), ("2025log-0415", 3.3, 1), ("2026pix-0139", 0.3, 2), ("2025log-0471", 0.3, 2), ("2024bru-0452", 9.7, 2),
       ("2024bru-0240", 4.0, 2), ("2025log-0454", 3.0, 1), ("2026pix-0554", 1.0, 2), ("2024bru-0444", 12.0, 2), ("2025gav-0280", 0.0, 1)]
k = 44
for i, (code, tin, nb) in enumerate(seq):
    t0 = b(k); t1 = b(k + nb) if i < len(seq) - 1 else 25.2
    C(code, t0, t1 - t0, tin, zoom=(1.08, 1.2), punch=[0.0], shake=4 if i % 3 == 0 else 0)
    if i % 2 == 0: layers.append(Flash(t0, 0.07, [PAL["cyan"], PAL["magenta"], PAL["white"]][i % 3], 0.35))
    S("whoosh_02", t0 - 0.06, -14); k += nb
for (pal, t0), cc in zip([("COSPLAY", b(45)), ("PALCOS", b(49)), ("GAMES", b(53)), ("DUBLAGEM", b(57))],
                         [(PAL["magenta"], PAL["pink"]), (PAL["cyan"], PAL["green"]), (PAL["green"], PAL["yellow"]), (PAL["violet"], PAL["cyan"])]):
    T(pal, t0, t0 + 1.3, 1480, 170, cc, glow=PAL["dark"], inn="slam", tin=0.12, out="pop", tout=0.15); S("impacto_04", t0, -10)
# F · PAYOFF + CTA (25,2 – 29,75)
C("2025log-0594", 25.2, DUR - 25.2, 184.6, zoom=(1.1, 1.2), ease="lin", speed=0.6)
layers += [Fill(25.2, DUR, PAL["dark"], alpha=0.72), Flash(25.2, 0.2, PAL["white"], 1.0)]
IMG(f"{KV}/portal_1.png", 25.2, DUR, (W / 2, 1040), scale=3.4, inn="zoom_in", tin=0.5, mode="screen", spin=25, alpha=0.55)
IMG(f"{KV}/logo_nerdxp_A.png", 25.3, DUR, (W / 2, 420), scale=1.55, inn="pop", tin=0.3)
T("O MAIOR EVENTO NERD", 25.5, 27.2, 820, 88, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
T("DE MINAS", 25.6, 27.2, 930, 88, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
layers.append(Strike(26.1, 27.2, W // 2 - 230, W // 2 + 230, 930, 20, PAL["magenta"], 0.14))
T("DA GALÁXIA", 26.3, 27.2, 1090, 176, (PAL["violet"], PAL["magenta"], PAL["cyan"]), glow=PAL["magenta"], inn="slam", tin=0.12, out="glitch")
layers.append(GlitchFx(26.28, 26.4, 0.9))
IMG(f"{KV}/alem_do_portal.png", 27.25, DUR, (W / 2, 800), scale=1.25, inn="pop", tin=0.25)
T("27 E 28 FEV 2027", 27.4, DUR, 1010, 118, (PAL["green"], PAL["cyan"]), glow=PAL["deep"], inn="slam", tin=0.12)
T("EXPOMINAS · BELO HORIZONTE", 27.55, DUR, 1130, 48, (PAL["white"],), glow=None, inn="slide_up", fontp=FONT_BODY, tracking=5)
cta = Image.new("RGBA", (760, 150), (0, 0, 0, 0)); dr = ImageDraw.Draw(cta); dr.rounded_rectangle((0, 0, 759, 149), 75, fill=(1, 255, 159, 255))
fo = font(FONT_DISPLAY, 66); dr.text(((760 - fo.getlength("COMENTA INGRESSO")) / 2, 34), "COMENTA INGRESSO", font=fo, fill=(41, 24, 51, 255))
layers.append(Gfx(cta, 28.0, DUR, (W / 2, 1480), inn="pop", tin=0.25))
S("marcador_riscando", 26.05, -6); S("impacto_02", 26.3, -3); S("ui_02", 27.4, -10); S("ui_04", 28.0, -10); S("impacto_03", 25.2, -6)

if not A.novideo:
    render(dict(clips=clips, layers=layers), A.out + "_video.mp4", DUR, finish=Finish(), preview=A.preview)
mix_audio(A.out + "_audio.wav", DUR, music=dict(file=f"{ROOT}/audio/musica/hitman_EDIT_30s_emenda.wav", in_s=0.0, fade_out=0.5), sfx=sfx, nat=nat)
if not A.novideo: mux(A.out + "_video.mp4", A.out + "_audio.wav", A.out + ".mp4")
print("OK", len(clips), "planos", len(sfx), "sfx")
