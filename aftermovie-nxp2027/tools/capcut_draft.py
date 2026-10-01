"""Gera um RASCUNHO do CapCut (projeto editável) do aftermovie NXP 2027 a partir do kit.
Timeline: trilha principal com os 59 planos · camadas de texto (PNG tela-cheia 1080x1920, com animação de entrada)
· trilha + SFX posicionados (flash/glitch/HUD/portal já vêm embutidos nos planos).
Saída: out/capcut_draft/{win,mac}/NXP2027_Aftermovie/ + mídia em NXP2027_capcut/ (caminho fixo por SO)."""
import os, json, re, shutil, glob, subprocess
import numpy as np
from PIL import Image
import pycapcut as cc

S = "/tmp/claude-0/-home-user-nerd-exp/5fc0b895-bc87-598f-81ab-980c65934114/scratchpad"
KIT = f"{S}/out/capcut_kit"
BUILD = f"{S}/out/capcut_draft"; MEDIA = f"{BUILD}/NXP2027_capcut"; DRAFTS = f"{BUILD}/_drafts"
shutil.rmtree(BUILD, ignore_errors=True)
for d in ("video", "audio", "textos"): os.makedirs(f"{MEDIA}/{d}")
os.makedirs(DRAFTS)
US = 1_000_000
def tr(t, d): return cc.Timerange(int(round(t * US)), int(round(d * US)))
def frames(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-map", "0:v:0", "-f", "null", "-"], capture_output=True, text=True).stderr
    return int(re.findall(r"frame=\s*(\d+)", e)[-1])

# mídia
vids = sorted(glob.glob(f"{KIT}/video_envio/*.mp4"))
for v in vids: shutil.copy(v, f"{MEDIA}/video/")
for a in glob.glob(f"{KIT}/audio/*.wav"): shutil.copy(a, f"{MEDIA}/audio/")

# textos: tabela da MONTAGEM.md -> PNG tela-cheia com o texto já na posição
rows = [l.split("|")[1:-1] for l in open(f"{KIT}/MONTAGEM.md") if l.startswith("| T")]
texts = []
for r in rows:
    fn, t0, t1, y, inn, mode = [x.strip() for x in r]
    im = Image.open(f"{KIT}/textos/{fn}").convert("RGBA")
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    x0, y0 = 540 - im.width // 2, int(y) - im.height // 2
    canvas.paste(im, (x0, y0), im)  # PIL recorta o que passar da borda
    out = f"{MEDIA}/textos/{fn}"; canvas.save(out)
    texts.append((out, float(t0), float(t1), inn))

script = cc.DraftFolder(DRAFTS).create_draft("NXP2027_Aftermovie", 1080, 1920, 30, allow_replace=True)
script.add_track(cc.TrackType.video, "PLANOS")
t = 0.0
for v in sorted(glob.glob(f"{MEDIA}/video/*.mp4")):
    d = frames(v) / 30.0
    script.add_segment(cc.VideoSegment(v, tr(t, d)), "PLANOS"); t += d
print("video total", round(t, 3))

# camadas de texto: distribui em trilhas sem sobreposição
ANIM = {"pop": "放大", "slam": "动感缩小", "slide_up": "向上滑动", "fade": "渐显", "glitch": "故障开场", "zoom_in": "放大"}
lanes = []
for path, t0, t1, inn in sorted(texts, key=lambda x: x[1]):
    k = next((i for i, end in enumerate(lanes) if end <= t0 + 1e-6), None)
    if k is None:
        lanes.append(0.0); k = len(lanes) - 1
        script.add_track(cc.TrackType.video, f"TEXTO_{k + 1}", relative_index=k + 1)
    lanes[k] = t1
    seg = cc.VideoSegment(path, tr(t0, t1 - t0))
    try: seg.add_animation(getattr(cc.IntroType, ANIM.get(inn, "渐显")), "0.25s")
    except Exception: pass
    script.add_segment(seg, f"TEXTO_{k + 1}")
print("trilhas de texto", len(lanes))

# áudio
script.add_track(cc.TrackType.audio, "TRILHA"); script.add_track(cc.TrackType.audio, "SFX")
script.add_segment(cc.AudioSegment(f"{MEDIA}/audio/trilha_hitman_v2.wav", tr(0, 60.0)), "TRILHA")
script.add_segment(cc.AudioSegment(f"{MEDIA}/audio/sfx_posicionados.wav", tr(0, 60.0)), "SFX")

# flashes/glitches/HUD/portal já estão embutidos nos planos (capcut_kit.py), sem trilha de efeitos extra
script.save()

# duas versões de caminho (sem depender do nome de usuário)
src = f"{DRAFTS}/NXP2027_Aftermovie"
for osn, base in [("win", "C:\\NXP2027_capcut"), ("mac", "/Users/Shared/NXP2027_capcut")]:
    dst = f"{BUILD}/{osn}/NXP2027_Aftermovie"; shutil.copytree(src, dst)
    for jf in ("draft_content.json",):
        p = f"{dst}/{jf}"; s = open(p).read()
        rep = base.replace("\\", "\\\\") if osn == "win" else base
        s = s.replace(MEDIA, rep)
        if osn == "win": s = re.sub(r'(C:\\\\NXP2027_capcut[^"]*)', lambda m: m.group(1).replace("/", "\\\\"), s)
        open(p, "w").write(s)
shutil.rmtree(DRAFTS)
print("OK")
