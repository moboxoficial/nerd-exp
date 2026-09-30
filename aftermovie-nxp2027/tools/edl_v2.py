"""AFTERMOVIE NXP 2027 — 'Além do Portal' — Reel 9:16, 60 s.  EDL v2 (ajustes do cliente).
Mudanças vs v1: fonte real do KV (Genius Techno, exportada do Canva) · drone Expominas (slot) ·
bloco novo pós-drone: palco cheio + atração no palco + ativação, cortes por beat e trilha contínua ·
NEXOS · sem planos de ginásio/teto/chão, crops com foco (premium) · clímax com atração no palco, sem Cineart.
Trilha: Hitman (K. MacLeod) — edição v2: orig 0–5,4 | 12,0–27,2 | 120,7–127,9 | 42,8–75,2  (drop 37,02 s)
 A 0–2,95 HOOK · B 2,95–5,41 portal · C 5,41–8,68 drone Expominas · D 8,68–15,28 palco/atração/ativação
 E 15,28–27,70 os 4 mundos · F 27,70–37,02 emoção + cascata · G 37,02–52,5 clímax · H 52,5–60 CTA"""
import sys, os, json, argparse, glob as _g
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nxp_engine import *

ap = argparse.ArgumentParser(); ap.add_argument("--preview", action="store_true")
ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float, default=60)
ap.add_argument("--out", default=f"{ROOT}/out/nxp_aftermovie_v2"); ap.add_argument("--noaudio", action="store_true")
ap.add_argument("--novideo", action="store_true"); ap.add_argument("--stills", action="store_true")
ap.add_argument("--drone", default="", help="arquivo do drone do Expominas (quando houver); vazio = plano provisório")
A = ap.parse_args()
DUR = 60.0
IDX = json.load(open(f"{ROOT}/raw/player/index.json"))
ORIG = json.load(open(f"{ROOT}/raw/orig/index.json")) if os.path.exists(f"{ROOT}/raw/orig/index.json") else {}
BEATS = json.load(open(f"{ROOT}/audio/musica/hitman_EDIT_60s_v2.beats.json"))["beats"]
def b(i): return BEATS[i]
def src(code):
    if code in ORIG and "arquivo" in ORIG[code]:
        o = ORIG[code]; return dict(arquivo=o["arquivo"], offset=o["offset"], lut=IDX[code]["lut"], code=code)
    d = IDX[code]; return dict(arquivo=d["arquivo"], offset=0.0, lut=d["lut"], code=code)
SFX, KV = f"{ROOT}/audio/sfx", f"{ROOT}/kv"
clips, layers, sfx, nat = [], [], [], []
def C(code, t, d, tin, **kw):
    c = Clip(src(code), t, d, tin, name=code, **kw); clips.append(c); return c
def S(name, at, g=-6):
    m = sorted(_g.glob(f"{SFX}/{name}*.wav")); assert m, name; sfx.append((m[0], at, g))
def K(txt, t0, t1, y, size=110, fill=(PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="pop", out="fade", x=W / 2, **kw):
    g = Gfx(kv_text(txt, size, fill, glow=glow), t0, t1, (x, y), inn=inn, out=out, **kw); layers.append(g); return g
def B(txt, t0, t1, y, size=40, fill=(PAL["white"],), tracking=6, **kw):  # corpo em Lexend Deca (fonte oficial do KV)
    g = Gfx(text_image(txt, size, fill, fontp=FONT_BODY, tracking=tracking), t0, t1, (W / 2, y), **kw); layers.append(g); return g
def IMG(path, t0, t1, pos, scale=1.0, **kw):
    g = Gfx(Image.open(path).convert("RGBA"), t0, t1, pos, scale=scale, **kw); layers.append(g); return g

# ============ A · HOOK (0 – 2,95)
C("2025log-0214", 0.0, b(3), 0.0, zoom=(1.18, 1.34), ease="out", focus=(0.5, 0.42))
C("2025log-0215", b(3), b(5) - b(3), 5.0, zoom=(1.25, 1.4), rgb=6, focus=(0.5, 0.38))
C("2026pix-0542", b(5), 2.95 - b(5), 1.0, zoom=(1.05, 1.15), shake=5, punch=[0.0], focus=(0.5, 0.35))
layers += [Hud(0.0, 2.95, "ALERTA: PORTAL INSTÁVEL", "COORD -19.93 / -43.97 · EXPOMINAS"),
           GlitchFx(b(3) - 0.07, b(3) + 0.1, 1.0), GlitchFx(b(5) - 0.05, b(5) + 0.08, 0.8), Flash(b(5), 0.1, PAL["magenta"], 0.6)]
S("sub_01", 0.0, -4); S("ui_03", 0.15, -10); S("glitch_01", b(3) - 0.07, -6); S("impacto_01", b(5), -5)

# ============ B · PORTAL (2,95 – 5,41) — respiro da trilha
layers.append(Fill(2.95, b(13), PAL["dark"]))
IMG(f"{KV}/portal_2.png", 2.95, b(13) + 0.05, (W / 2, H / 2), scale=0.9, inn="zoom_in", tin=0.5, out="zoom_through", tout=0.45, mode="screen", grow=0.6, spin=40)
K("os portais\nestão abrindo", 3.25, 5.05, H / 2, 112, (PAL["white"],), glow=PAL["cyan"], inn="glitch", tin=0.35, out="glitch", tout=0.25)
K("de novo.", 4.1, 5.05, H / 2 + 200, 84, (PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="slide_up")
layers.append(Flash(b(13), 0.16, PAL["white"], 0.95))
S("portal_01", 2.95, -5); S("texto_02", 3.25, -12); S("riser_02", 1.6, -12); S("reverse_01", 4.8, -6); S("whoosh_02", b(13) - 0.12, -5)

# ============ C · DRONE EXPOMINAS (5,41 – 8,68)
if A.drone:
    d = dict(arquivo=A.drone, offset=0.0, lut=None, code="drone_expominas")
    clips.append(Clip(d, b(13), b(21) - b(13), 0.0, zoom=(1.0, 1.12), ease="lin", name="drone_expominas"))
else:  # provisório: voo sobre BH (sem o Minas Shopping), até chegar o drone do Expominas
    C("2025log-0594", b(13), b(21) - b(13), 4.0, zoom=(1.05, 1.18), ease="lin", speed=1.2, focus=(0.5, 0.55))
K("agora no expominas", b(14), b(21) - 0.05, 860, 84, (PAL["cyan"], PAL["green"]), glow=PAL["violet"], inn="slam", tin=0.15, out="glitch", tout=0.15)
B("O MAIOR CENTRO DE EVENTOS DE MINAS", b(15), b(21) - 0.05, 990, 38, inn="slide_up", out="fade")
S("impacto_03", b(13), -6); S("whoosh_03", b(13) - 0.2, -10)

# ============ D · PALCO + ATRAÇÃO + ATIVAÇÃO (8,68 – 15,28) — cortes no beat
seqD = [  # (código, in, beats, foco)
    ("2025log-0449", 0.5, 1, (0.5, 0.55)), ("2025log-0484", 0.5, 2, (0.45, 0.5)), ("2025log-0496", 2.0, 1, (0.42, 0.5)),
    ("2025log-0481", 2.0, 2, (0.5, 0.52)), ("2025log-0574", 1.0, 1, (0.55, 0.5)), ("2024bru-0135", 2.0, 1, (0.45, 0.55)),
    ("2025log-0501", 1.0, 1, (0.38, 0.45)), ("2025log-0472", 1.0, 1, (0.5, 0.62)), ("2025log-0577", 3.0, 2, (0.55, 0.5)),
    ("2025log-0123", 8.0, 1, (0.5, 0.5)), ("2025log-0487", 1.0, 1, (0.45, 0.45)), ("2025log-0446", 12.0, 2, (0.5, 0.5))]
k = 21
for i, (code, tin, nb, foc) in enumerate(seqD):
    t0, t1 = b(k), b(k + nb)
    C(code, t0, t1 - t0, tin, zoom=(1.22, 1.32), punch=[0.0], focus=foc, shake=3 if i % 3 == 2 else 0)
    S("whoosh_04" if i % 2 else "whoosh_01", t0 - 0.06, -12)
    if i % 3 == 0: layers.append(Flash(t0, 0.06, [PAL["cyan"], PAL["magenta"], PAL["green"]][(i // 3) % 3], 0.3))
    k += nb
K("+10 mil nerds", b(21) + 0.03, b(24), 1480, 118, (PAL["cyan"], PAL["green"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
K("palco", b(24) + 0.03, b(27), 1480, 150, (PAL["magenta"], PAL["pink"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
K("atrações", b(27) + 0.03, b(30), 1480, 150, (PAL["yellow"], PAL["green"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
K("ativações", b(30) + 0.03, b(34), 1480, 150, (PAL["violet"], PAL["cyan"]), glow=PAL["dark"], inn="slam", tin=0.1, out="pop", tout=0.1)
for bb in (21, 24, 27, 30, 34): S("impacto_04", b(bb), -9)
S("plateia_02", b(21), -16); S("riser_02", b(37) - 4.0, -13)

# ============ E · OS 4 MUNDOS (15,28 – 27,70) — 8 beats cada, 4 planos
MUNDOS = [
    ("lótus", "cultura asiática · anime · k-pop", (PAL["magenta"], PAL["pink"], PAL["yellow"]), "mundo 1/4",
     [("2025log-0063", 2.5, (0.42, 0.5)), ("2025log-0226", 0.5, (0.45, 0.45)), ("2024bru-0295", 3.0, (0.5, 0.45)), ("2025log-0546", 1.0, (0.5, 0.5))]),
    ("nexos", "cultura pop · cinema · séries", (PAL["cyan"], PAL["violet"]), "mundo 2/4",
     [("2025log-0383", 2.5, (0.5, 0.58)), ("2025log-0211", 3.0, (0.5, 0.45)), ("2025log-0260", 34.5, (0.5, 0.5)), ("2025log-0019", 4.0, (0.5, 0.45))]),
    ("eldarion", "medieval · rpg · jogos de mesa", (PAL["yellow"], PAL["green"]), "mundo 3/4",
     [("2025log-0535", 0.3, (0.5, 0.5)), ("2026pix-0543", 0.5, (0.5, 0.4)), ("2025log-0100", 1.0, (0.45, 0.45)), ("2025log-0535", 12.0, (0.5, 0.5))]),
    ("pixel", "games · e-sports · tecnologia", (PAL["green"], PAL["cyan"]), "mundo 4/4",
     [("2026pix-0062", 0.5, (0.5, 0.5)), ("2025log-0578", 5.0, (0.55, 0.5)), ("2024bru-0070", 0.5, (0.5, 0.55)), ("2026pix-0098", 0.5, (0.5, 0.5))]),
]
bi = 37
for mi, (nome, sub, cores, tag, planos) in enumerate(MUNDOS):
    t0 = b(bi); kk = bi
    for code, tin, foc in planos:
        C(code, b(kk), b(kk + 2) - b(kk), tin, zoom=(1.1, 1.2), punch=[0.0], focus=foc)
        S("whoosh_04" if (kk % 4) else "whoosh_01", b(kk) - 0.08, -12); kk += 2
    t1 = b(bi + 8)
    K(nome, t0 + 0.05, t0 + 1.9, 760, 210, cores, glow=PAL["violet"], inn="slam", tin=0.18, out="glitch", tout=0.2)
    B(sub.upper(), t0 + 0.25, t0 + 1.9, 905, 40, inn="slide_up", tracking=4)
    K(tag, t0 + 0.05, t1 - 0.05, 300, 50, (PAL["white"],), glow=None, inn="fade", alpha=0.85)
    layers += [LightLeak(t0 - 0.2, 0.45, side="left" if mi % 2 else "right", peak=0.5), GlitchFx(t0 - 0.04, t0 + 0.06, 0.7)]
    S("impacto_02", t0, -7); S("glitch_03", t0 - 0.04, -10)
    bi += 8

# ============ F · EMOÇÃO (27,70 – 33,5) + CASCATA (33,5 – 37,02)
drop = 37.02
t = b(69)
for code, tin, d, sp, foc in [("2025log-0489", 0.5, 1.95, 0.5, (0.55, 0.45)), ("2025log-0427", 3.0, 1.9, 0.6, (0.5, 0.5)),
                              ("2025log-0448", 1.0, 1.95, 0.6, (0.5, 0.45))]:
    C(code, t, d, tin, speed=sp, zoom=(1.12, 1.2), ease="lin", focus=foc); t += d
K("aqui, todo fã", b(69) + 0.2, b(69) + 3.2, 1440, 104, (PAL["white"],), glow=PAL["violet"], inn="fade", tin=0.4)
K("encontra seu lugar", b(69) + 1.4, t - 0.05, 1570, 88, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up", tin=0.4)
S("reverse_02", b(69) - 0.3, -9)
cas_start = t
retratos = [("2025log-0216", 0.3), ("2025log-0213", 1.0), ("2025log-0221", 1.0), ("2025log-0218", 0.8), ("2025log-0225", 1.0),
            ("2025log-0019", 8.0), ("2025log-0016", 0.5), ("2025log-0222", 0.5), ("2025log-0217", 1.0), ("2025log-0020", 1.5),
            ("2025log-0226", 2.0), ("2025gav-0024", 1.3), ("2024bru-0123", 0.3), ("2025log-0212", 0.2), ("2025log-0018", 0.2), ("2025log-0214", 0.5)]
w = np.linspace(1.0, 0.18, len(retratos)); w = w / w.sum() * (drop - cas_start); tt = cas_start
for (code, tin), d in zip(retratos, w):
    f = find_face(src(code), tin); anc = (f[0], f[1], 0.36 * W / max(f[2], 40)) if f else None
    C(code, tt, float(d), tin, zoom=(1.0, 1.04), anchor=anc); S("camera_01", tt, -16); tt += float(d)
S("riser_01", drop - 7.8, -6)
K("qual é o seu\npersonagem?", cas_start + 0.1, drop - 0.25, 1620, 80, (PAL["white"],), glow=PAL["violet"], inn="fade", out="fade")

# ============ G · DROP / CLÍMAX (37,02 – 52,5) — com atração no palco, sem Cineart/ginásio
layers += [Flash(drop, 0.22, PAL["white"], 1.0), GlitchFx(drop - 0.05, drop + 0.08, 1.0)]
S("sub_02", drop, -2); S("impacto_01", drop, -3); S("plateia_02", drop + 0.1, -13)
seq = [("2024bru-0471", 4.7, (0.5, 0.5)), ("2025log-0415", 3.3, (0.5, 0.55)), ("2026pix-0139", 0.3, (0.5, 0.45)), ("2025log-0471", 0.3, (0.5, 0.62)),
       ("2025log-0484", 1.5, (0.45, 0.5)), ("2025log-0438", 1.0, (0.5, 0.55)), ("2024bru-0452", 9.7, (0.5, 0.72)), ("2025log-0501", 3.0, (0.47, 0.38)),
       ("2024bru-0240", 4.0, (0.5, 0.45)), ("2025log-0454", 3.0, (0.5, 0.5)), ("2025log-0202", 5.0, (0.5, 0.55)), ("2025log-0481", 9.0, (0.5, 0.55)),
       ("2025log-0415", 20.1, (0.5, 0.5)), ("2024bru-0444", 12.0, (0.5, 0.5)), ("2025log-0496", 6.0, (0.45, 0.45)), ("2025log-0213", 12.0, (0.5, 0.4)),
       ("2025log-0357", 1.0, (0.5, 0.55)), ("2024bru-0295", 4.5, (0.5, 0.45)), ("2024bru-0328", 9.0, (0.5, 0.5)), ("2025gav-0280", 0.0, (0.5, 0.45)),
       ("2024bru-0471", 91.8, (0.5, 0.5))]
nbs = [2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 3]
bounds = [drop]; k = 94  # b(94)=37,69 é o 1º beat após o drop
for nb in nbs[:-1]:
    bounds.append(b(k)); k += nb
bounds.append(52.5)
for i, ((code, tin, foc), (t0, t1)) in enumerate(zip(seq, zip(bounds, bounds[1:]))):
    mid = [b(kk) - t0 for kk in range(len(BEATS)) if t0 + 0.2 < b(kk) < t1 - 0.2][:1]
    zz = (1.35, 1.45) if code == '2024bru-0452' else (1.12, 1.24)
    C(code, t0, t1 - t0, tin, zoom=zz, punch=[0.0] + mid, focus=foc,
      shake=4 if i % 3 == 0 else 0, rgb=3 if i % 4 == 1 else 0)
    if i % 2 == 0: layers.append(Flash(t0, 0.07, [PAL["cyan"], PAL["magenta"], PAL["white"]][i % 3], 0.35))
    S("whoosh_03" if i % 2 else "whoosh_02", t0 - 0.06, -14)
for (pal, t0), cc in zip([("cosplay", b(94)), ("palcos", b(102)), ("games", b(110)), ("dublagem", b(118)), ("experiências", b(126))],
                         [(PAL["magenta"], PAL["pink"]), (PAL["cyan"], PAL["green"]), (PAL["green"], PAL["yellow"]), (PAL["violet"], PAL["cyan"]), (PAL["yellow"], PAL["magenta"])]):
    K(pal, t0, t0 + 1.5, 1480, 180 if len(pal) < 9 else 116, cc, glow=PAL["dark"], inn="slam", tin=0.12, out="pop", tout=0.15)
    S("impacto_04", t0, -10)

# ============ H · PAYOFF + CTA (52,5 – 60)
C("2025log-0449", 52.5, DUR - 52.5, 1.0, zoom=(1.15, 1.25), ease="lin", speed=0.5, focus=(0.5, 0.55))
layers += [Fill(52.5, DUR, PAL["dark"], alpha=0.74), Flash(52.5, 0.25, PAL["white"], 1.0)]
IMG(f"{KV}/portal_1.png", 52.5, DUR, (W / 2, 1040), scale=3.4, inn="zoom_in", tin=0.6, out="fade", mode="screen", spin=25, alpha=0.5)
IMG(f"{KV}/logo_nerdxp_A.png", 52.6, DUR, (W / 2, 420), scale=1.55, inn="pop", tin=0.35, out="fade")
K("o maior evento nerd", 53.1, 56.1, 820, 92, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
K("de minas", 53.35, 56.1, 935, 92, (PAL["white"],), glow=PAL["violet"], inn="slide_up", out="glitch")
layers.append(Strike(54.4, 56.1, W // 2 - 220, W // 2 + 220, 935, 20, PAL["magenta"], 0.16))
K("da galáxia", 54.65, 56.1, 1100, 180, (PAL["violet"], PAL["magenta"], PAL["cyan"]), glow=PAL["magenta"], inn="slam", tin=0.14, out="glitch")
layers += [GlitchFx(54.63, 54.75, 0.9), Flash(54.65, 0.12, PAL["magenta"], 0.5)]
S("marcador_riscando", 54.35, -6); S("impacto_02", 54.65, -3); S("glitch_04", 56.05, -8)
IMG(f"{KV}/alem_do_portal.png", 56.15, DUR, (W / 2, 780), scale=1.25, inn="pop", tin=0.3, out="fade")
K("27 e 28", 56.4, DUR, 990, 170, (PAL["yellow"], PAL["green"]), glow=PAL["deep"], inn="slam", tin=0.15)
K("fev de 2027", 56.55, DUR, 1130, 84, (PAL["white"],), glow=None, inn="slide_up")
K("no expominas", 56.7, DUR, 1235, 70, (PAL["cyan"], PAL["green"]), glow=PAL["deep"], inn="slide_up")
K("feh dubs", 57.3, DUR, 1345, 54, (PAL["yellow"],), glow=PAL["dark"], inn="fade")
K("anderson gaveta", 57.4, DUR, 1405, 54, (PAL["yellow"],), glow=PAL["dark"], inn="fade")
K("já confirmados", 57.5, DUR, 1465, 38, (PAL["white"],), glow=None, inn="fade", alpha=0.85)
pill = Image.new("RGBA", (780, 150), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, 779, 149), 75, fill=(1, 255, 159, 255))
ct = kv_text("comenta ingresso", 64, ("#291833",)); pill.alpha_composite(ct, ((780 - ct.width) // 2, (150 - ct.height) // 2))
layers.append(Gfx(pill, 58.0, DUR, (W / 2, 1610), inn="pop", tin=0.3, out="fade"))
K("e recebe o link do lote", 58.2, DUR, 1725, 46, (PAL["white"],), glow=None, inn="fade")
S("impacto_03", 52.5, -6); S("portal_02", 52.5, -10); S("ui_02", 56.4, -10); S("ui_04", 58.0, -10)

if A.stills:  # 1 frame por plano (meio do plano), com grafismos, para revisar crops
    thumbs = []
    for c in sorted(clips, key=lambda c: c.t):
        tm = c.t + c.d * 0.5; fr = c.render(tm); c.close()
        for L in layers: L.draw(fr, tm)
        im = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((216, 384))
        ImageDraw.Draw(im).text((4, 4), f"{tm:.1f}s {c.name}", fill=(255, 255, 0))
        thumbs.append(im)
    for p0 in range(0, len(thumbs), 30):
        g = Image.new("RGB", (216 * 10, 384 * 3))
        for i, im in enumerate(thumbs[p0:p0 + 30]): g.paste(im, ((i % 10) * 216, (i // 10) * 384))
        g.save(f"{A.out}_stills_{p0 // 30}.jpg", quality=80)
    sys.exit(0)
if not A.novideo:
    render(dict(clips=clips, layers=layers), A.out + "_video.mp4", DUR, finish=Finish(), start=A.start, end=A.end, preview=A.preview)
if not A.noaudio:
    mix_audio(A.out + "_audio.wav", DUR, music=dict(file=f"{ROOT}/audio/musica/hitman_EDIT_60s_v2.wav", in_s=0.0, gain_db=0, fade_out=0.8), sfx=sfx, nat=nat)
if not A.novideo and not A.noaudio and A.start == 0 and A.end == DUR:
    mux(A.out + "_video.mp4", A.out + "_audio.wav", A.out + ".mp4")
json.dump(dict(clips=[dict(code=c.name, t=round(c.t, 3), d=round(c.d, 3), src_in=round(c.src_in, 3)) for c in clips],
               sfx=[(os.path.basename(a), round(t, 3), g) for a, t, g in sfx]), open(A.out + "_edl.json", "w"), indent=1)
print("OK", len(clips), "planos", len(sfx), "sfx")
