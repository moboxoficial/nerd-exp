"""AFTERMOVIE NXP 2027 — corte de 30 s para anúncio (v2, com os ajustes do cliente).
Trilha: Hitman (K. MacLeod), edição 30 s — energia 0–7,6 · respiro 7,6–18,4 · drop 18,41.
 A 0–1,86 hook · B 1,86–3,51 drone Expominas · C 3,51–7,62 palco/atração/ativação (1 beat/plano)
 D 7,62–14,4 mundos relâmpago + emoção · E 14,4–18,41 cascata · F 18,41–25,2 clímax · G 25,2–29,75 CTA"""
import sys, os, json, argparse, glob as _g
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nxp_engine import *

ap = argparse.ArgumentParser(); ap.add_argument("--out", default=f"{ROOT}/out/NXP2027_aftermovie_30s_v2")
ap.add_argument("--drone", default=""); ap.add_argument("--novideo", action="store_true")
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
def K(txt, t0, t1, y, size=110, fill=(PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="pop", out="fade", x=W / 2, **kw):
    g = Gfx(kv_text(txt, size, fill, glow=glow), t0, t1, (x, y), inn=inn, out=out, **kw); layers.append(g); return g
def B(txt, t0, t1, y, size=40, **kw):
    g = Gfx(text_image(txt, size, (PAL["white"],), fontp=FONT_BODY, tracking=5), t0, t1, (W / 2, y), **kw); layers.append(g); return g
def IMG(path, t0, t1, pos, scale=1.0, **kw):
    g = Gfx(Image.open(path).convert("RGBA"), t0, t1, pos, scale=scale, **kw); layers.append(g); return g

# A · HOOK
C("2025log-0214", 0.0, b(1), 0.0, zoom=(1.2, 1.34), ease="out", focus=(0.5, 0.42))
C("2025log-0215", b(1), b(3) - b(1), 5.0, zoom=(1.25, 1.4), rgb=6, focus=(0.5, 0.38))
layers += [Hud(0, b(3), "ALERTA: PORTAL INSTÁVEL", "COORD -19.93 / -43.97 · EXPOMINAS"), GlitchFx(b(1) - 0.06, b(1) + 0.08, 1.0),
           Flash(b(3), 0.14, PAL["white"], 0.9)]
S("sub_01", 0, -4); S("glitch_01", b(1) - 0.06, -6); S("whoosh_02", b(3) - 0.1, -5)
# B · DRONE EXPOMINAS
if A.drone:
    clips.append(Clip(dict(arquivo=A.drone, offset=0.0, lut=None), b(3), b(7) - b(3), 0.0, zoom=(1.0, 1.1), ease="lin", name="drone"))
else:
    C("2025log-0594", b(3), b(7) - b(3), 4.0, zoom=(1.05, 1.18), ease="lin", speed=1.2, focus=(0.5, 0.55))
K("agora no expominas", b(3) + 0.05, b(7) - 0.05, 860, 84, (PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="slam", tin=0.12, out="glitch", tout=0.1)
S("impacto_03", b(3), -6)
# C · PALCO / ATRAÇÃO / ATIVAÇÃO — 1 beat por plano
seqC = [("2025log-0449", 0.5, (0.5, 0.55)), ("2025log-0484", 0.5, (0.45, 0.5)), ("2025log-0496", 2.0, (0.42, 0.5)), ("2025log-0481", 2.0, (0.5, 0.52)),
        ("2025log-0574", 1.0, (0.55, 0.5)), ("2024bru-0135", 2.0, (0.45, 0.55)), ("2025log-0487", 1.0, (0.45, 0.45)), ("2025log-0472", 1.0, (0.5, 0.62)),
        ("2025log-0577", 3.0, (0.55, 0.5)), ("2025log-0123", 8.0, (0.5, 0.5))]
for i, (code, tin, foc) in enumerate(seqC):
    t0, t1 = b(7 + i), (b(8 + i) if i < len(seqC) - 1 else 7.62)
    C(code, t0, t1 - t0, tin, zoom=(1.22, 1.3), punch=[0.0], focus=foc); S("whoosh_04", t0 - 0.05, -13)
K("+10 mil nerds", b(7) + 0.03, b(9), 1480, 118, (PAL["cyan"], PAL["green"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
K("atrações", b(9) + 0.03, b(12), 1480, 150, (PAL["yellow"], PAL["green"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
K("ativações", b(12) + 0.03, 7.6, 1480, 150, (PAL["violet"], PAL["cyan"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
for bb in (7, 9, 12): S("impacto_04", b(bb), -9)
# D · MUNDOS RELÂMPAGO + EMOÇÃO (7,62 – 14,4)
mund = [("2025log-0063", 2.5, "lótus", (PAL["magenta"], PAL["pink"], PAL["yellow"])), ("2025log-0383", 2.5, "nexos", (PAL["cyan"], PAL["violet"])),
        ("2025log-0535", 0.3, "eldarion", (PAL["yellow"], PAL["green"])), ("2026pix-0062", 0.5, "pixel", (PAL["green"], PAL["cyan"]))]
t = 7.62
for code, tin, nome, cores in mund:
    C(code, t, 0.8, tin, zoom=(1.12, 1.2), punch=[0.0], focus=(0.5, 0.5))
    K(nome, t, t + 0.8, 780, 200, cores, glow=PAL["violet"], inn="slam", tin=0.08, out="glitch", tout=0.08); S("impacto_02", t, -9); t += 0.8
for code, tin, d, sp, foc in [("2025log-0489", 0.5, 1.7, 0.5, (0.55, 0.45)), ("2025log-0427", 3.0, 1.58, 0.6, (0.5, 0.5))]:
    C(code, t, d, tin, speed=sp, zoom=(1.12, 1.2), ease="lin", focus=foc); t += d
K("aqui, todo fã", 10.9, 14.3, 1440, 104, (PAL["white"],), glow=PAL["violet"], inn="fade", tin=0.3)
K("encontra seu lugar", 11.6, 14.3, 1570, 88, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up", tin=0.3)
S("reverse_02", 10.6, -9)
# E · CASCATA (t – drop)
drop = b(44)
ret = [("2025log-0216", 0.3), ("2025log-0213", 1.0), ("2025log-0221", 1.0), ("2025log-0218", 0.8), ("2025log-0225", 1.0), ("2025log-0019", 8.0),
       ("2025log-0016", 0.5), ("2025log-0222", 0.5), ("2025log-0217", 1.0), ("2025log-0020", 1.5), ("2025log-0226", 2.0), ("2025gav-0024", 1.3),
       ("2024bru-0123", 0.3), ("2025log-0212", 0.2), ("2025log-0018", 0.2), ("2025log-0214", 0.5)]
w = np.linspace(1.0, 0.18, len(ret)); w = w / w.sum() * (drop - t); tt = t
for (code, tin), d in zip(ret, w):
    f = find_face(src(code), tin); anc = (f[0], f[1], 0.36 * W / max(f[2], 40)) if f else None
    C(code, tt, float(d), tin, zoom=(1.0, 1.04), anchor=anc); S("camera_01", tt, -16); tt += float(d)
S("riser_01", drop - 7.8, -6)
K("qual é o seu\npersonagem?", t + 0.1, drop - 0.25, 1620, 80, (PAL["white"],), glow=PAL["violet"], inn="fade", out="fade")
# F · CLÍMAX (drop – 25,2)
layers += [Flash(drop, 0.22, PAL["white"], 1.0), GlitchFx(drop - 0.05, drop + 0.08, 1.0)]
S("sub_02", drop, -2); S("impacto_01", drop, -3); S("plateia_02", drop + 0.1, -13)
seq = [("2024bru-0471", 4.7, 2, (0.5, 0.5)), ("2025log-0415", 3.3, 1, (0.5, 0.55)), ("2026pix-0139", 0.3, 2, (0.5, 0.45)), ("2025log-0484", 1.5, 2, (0.45, 0.5)),
       ("2025log-0471", 0.3, 2, (0.5, 0.62)), ("2025log-0501", 3.0, 1, (0.47, 0.38)), ("2024bru-0240", 4.0, 2, (0.5, 0.45)), ("2025log-0454", 3.0, 1, (0.5, 0.5)),
       ("2024bru-0444", 12.0, 2, (0.5, 0.5)), ("2025gav-0280", 0.0, 1, (0.5, 0.45))]
k = 44
for i, (code, tin, nb, foc) in enumerate(seq):
    t0 = b(k); t1 = b(k + nb) if i < len(seq) - 1 else 25.2
    C(code, t0, t1 - t0, tin, zoom=(1.12, 1.24), punch=[0.0], focus=foc, shake=4 if i % 3 == 0 else 0)
    if i % 2 == 0: layers.append(Flash(t0, 0.07, [PAL["cyan"], PAL["magenta"], PAL["white"]][i % 3], 0.35))
    S("whoosh_02", t0 - 0.06, -14); k += nb
for (pal, t0), cc in zip([("cosplay", b(45)), ("palcos", b(49)), ("games", b(53)), ("dublagem", b(57))],
                         [(PAL["magenta"], PAL["pink"]), (PAL["cyan"], PAL["green"]), (PAL["green"], PAL["yellow"]), (PAL["violet"], PAL["cyan"])]):
    K(pal, t0, t0 + 1.3, 1480, 180, cc, glow=PAL["dark"], inn="slam", tin=0.12, out="pop", tout=0.15); S("impacto_04", t0, -10)
# G · PAYOFF + CTA (25,2 – 29,75)
C("2025log-0449", 25.2, DUR - 25.2, 1.0, zoom=(1.15, 1.22), ease="lin", speed=0.5, focus=(0.5, 0.55))
layers += [Fill(25.2, DUR, PAL["dark"], alpha=0.74), Flash(25.2, 0.2, PAL["white"], 1.0)]
IMG(f"{KV}/portal_1.png", 25.2, DUR, (W / 2, 1040), scale=3.4, inn="zoom_in", tin=0.5, mode="screen", spin=25, alpha=0.5)
IMG(f"{KV}/logo_nerdxp_A.png", 25.3, DUR, (W / 2, 420), scale=1.55, inn="pop", tin=0.3)
K("o maior evento nerd", 25.5, 27.2, 820, 92, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
K("de minas", 25.6, 27.2, 935, 92, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
layers.append(Strike(26.1, 27.2, W // 2 - 220, W // 2 + 220, 935, 20, PAL["magenta"], 0.14))
K("da galáxia", 26.3, 27.2, 1100, 180, (PAL["violet"], PAL["magenta"], PAL["cyan"]), glow=PAL["magenta"], inn="slam", tin=0.12, out="glitch")
layers.append(GlitchFx(26.28, 26.4, 0.9))
IMG(f"{KV}/alem_do_portal.png", 27.25, DUR, (W / 2, 780), scale=1.25, inn="pop", tin=0.25)
K("27 e 28", 27.4, DUR, 990, 170, (PAL["yellow"], PAL["green"]), glow=PAL["deep"], inn="slam", tin=0.12)
K("fev de 2027", 27.5, DUR, 1130, 84, (PAL["white"],), glow=None, inn="slide_up")
K("no expominas", 27.6, DUR, 1235, 70, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up")
pill = Image.new("RGBA", (780, 150), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, 779, 149), 75, fill=(1, 255, 159, 255))
ct = kv_text("comenta ingresso", 64, ("#291833",)); pill.alpha_composite(ct, ((780 - ct.width) // 2, (150 - ct.height) // 2))
layers.append(Gfx(pill, 28.0, DUR, (W / 2, 1480), inn="pop", tin=0.25))
S("marcador_riscando", 26.05, -6); S("impacto_02", 26.3, -3); S("ui_02", 27.4, -10); S("ui_04", 28.0, -10); S("impacto_03", 25.2, -6)

if not A.novideo:
    render(dict(clips=clips, layers=layers), A.out + "_video.mp4", DUR, finish=Finish())
mix_audio(A.out + "_audio.wav", DUR, music=dict(file=f"{ROOT}/audio/musica/hitman_EDIT_30s_emenda.wav", in_s=0.0, fade_out=0.5), sfx=sfx, nat=nat)
if not A.novideo: mux(A.out + "_video.mp4", A.out + "_audio.wav", A.out + ".mp4")
print("OK", len(clips), "planos", len(sfx), "sfx")
