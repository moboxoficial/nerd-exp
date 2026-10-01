"""Kit de edição para CapCut a partir da EDL v2 (60 s).
Gera em out/capcut_kit/:
  video/NN_<inicio>s_<bloco>_<codigo>.mp4 — cada plano já com cor (LUT NXP), crop 9:16, foco, zoom/punch/shake e
      velocidade aplicados, sem textos. Colocados lado a lado na trilha principal, reproduzem o corte.
      O trecho do portal (2,95–5,41 s) e a cascata de retratos (16 planos) saem como um arquivo cada.
  audio/trilha_hitman_v2.wav, audio/sfx_posicionados.wav (todos os SFX já no tempo certo, começando em 0)
  textos/*.png — títulos na Genius Techno (fonte do KV) com degradê/glow, PNG transparente 1080 de largura máx.
  MONTAGEM.md — tabela de montagem (arquivo, entra em, dura) + textos (arquivo, entra em, sai em, posição Y)."""
import sys, os, json, shutil, subprocess, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nxp_engine import *

OUT = f"{ROOT}/out/capcut_kit"
for d in ("video", "audio", "textos"): os.makedirs(f"{OUT}/{d}", exist_ok=True)

# carrega a EDL v2 sem renderizar (usa --novideo --noaudio)
sys.argv = ["edl_v2.py", "--novideo", "--noaudio", "--out", f"{ROOT}/out/_kit_tmp"]
spec = importlib.util.spec_from_file_location("edl", f"{HERE}/edl_v2.py"); E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)
clips = sorted(E.clips, key=lambda c: c.t)

def bloco(t):
    for lim, nome in [(2.95, "hook"), (5.41, "portal"), (8.68, "expominas"), (15.28, "palco_ativacao"), (27.70, "mundos"),
                      (E.cas_start, "emocao"), (37.02, "cascata"), (52.5, "climax"), (99, "cta")]:
        if t < lim - 1e-3: return nome

def render_range(t0, t1, path, layers=()):
    """renderiza [t0,t1) só com os clipes (e camadas opcionais), com o acabamento (grão/vinheta)."""
    n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    fin = Finish()
    for i in range(n0, n1):
        t = i / FPS
        act = [c for c in clips if c.t <= t < c.t + c.d]
        frame = act[-1].render(t) if act else np.zeros((H, W, 3), np.float32) + hex2rgb(PAL["dark"])
        for L in layers: L.draw(frame, t)
        fin.apply(frame, i)
        enc.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    for c in clips: c.close()

rows = []; n = 1
# 1) hook (3 planos individuais)
groups = []
cas = [c for c in clips if E.cas_start - 1e-3 <= c.t < 37.02 - 1e-3]
for c in clips:
    if c in cas: continue
    groups.append((c.t, c.t + c.d, c.name))
groups.append((2.95, 5.41, "portal_kv"))
groups.append((E.cas_start, 37.02, "cascata_16_retratos"))
groups.sort()
for t0, t1, name in groups:
    fn = f"{n:02d}_{t0:05.2f}s_{bloco(t0)}_{name}.mp4"
    lay = [L for L in E.layers if (isinstance(L, Fill) and abs(L.t0 - 2.95) < 0.01) or (isinstance(L, Gfx) and L.mode == "screen" and abs(L.t0 - 2.95) < 0.01)] if name == "portal_kv" else []
    render_range(t0, t1, f"{OUT}/video/{fn}", lay)
    rows.append((fn, t0, t1 - t0)); n += 1
    print(fn, flush=True)

# 2) áudio
shutil.copy(f"{ROOT}/audio/musica/hitman_EDIT_60s_v2.wav", f"{OUT}/audio/trilha_hitman_v2.wav")
mix_audio(f"{OUT}/audio/sfx_posicionados.wav", 60.0, music=None, sfx=E.sfx, nat=[], lufs=-16)

# 3) textos (as camadas Gfx com texto, na ordem; posições em px do quadro 1080x1920)
txt = []
for k, L in enumerate([L for L in E.layers if isinstance(L, Gfx)]):
    a = (np.clip(L.pm, 0, 1) * 255).astype(np.uint8)
    rgb = a[..., :3].astype(np.float32); al = a[..., 3:4].astype(np.float32) / 255
    rgb = np.where(al > 0, rgb / np.maximum(al, 1e-3), 0).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(np.concatenate([rgb, a[..., 3:4]], -1), "RGBA")
    if L.scale != 1.0: im = im.resize((max(1, int(im.width * L.scale)), max(1, int(im.height * L.scale))), Image.LANCZOS)
    fn = f"T{k + 1:02d}_{L.t0:05.2f}s.png"; im.save(f"{OUT}/textos/{fn}")
    txt.append((fn, L.t0, L.t1, int(L.pos[1]), L.inn, L.mode))

with open(f"{OUT}/MONTAGEM.md", "w") as f:
    f.write("# Kit CapCut · Aftermovie NXP 2027 (60 s, 1080x1920, 30 fps)\n\n")
    f.write("1. Novo projeto 9:16 1080x1920 30 fps.\n2. Trilha principal: arraste TODOS os arquivos de `video/` em ordem (01, 02, 03…), sem espaço entre eles — os tempos já batem com a trilha.\n")
    f.write("3. Áudio: `audio/trilha_hitman_v2.wav` em 0:00 e `audio/sfx_posicionados.wav` em 0:00 (todos os efeitos já estão no tempo).\n")
    f.write("4. Textos: sobreposições com os PNG de `textos/`, centralizados na horizontal, no Y indicado (0 = topo do quadro de 1920). Animação de entrada sugerida na coluna 'entrada' (pop = 'zoom in' / slam = 'zoom out rápido' / glitch / slide_up = 'subir' / fade).\n")
    f.write("5. Efeitos do CapCut que reproduzem o corte: 'Glitch' nos cortes de mundo e no drop (37,02 s), 'Flash' branco em 5,41 s / 37,02 s / 52,5 s, 'Shake' leve nos planos de palco.\n\n")
    f.write("Crédito obrigatório na legenda: \"Hitman\" – Kevin MacLeod (incompetech.com), CC BY 4.0.\n\n")
    f.write("## Vídeo (trilha principal)\n| arquivo | entra em (s) | dura (s) |\n|---|---|---|\n")
    for fn, t0, d in rows: f.write(f"| {fn} | {t0:.2f} | {d:.2f} |\n")
    f.write("\n## Textos (sobreposição)\n| arquivo | entra (s) | sai (s) | centro Y (px) | entrada | blend |\n|---|---|---|---|---|---|\n")
    for fn, t0, t1, y, inn, mode in txt: f.write(f"| {fn} | {t0:.2f} | {t1:.2f} | {y} | {inn} | {'tela (screen)' if mode == 'screen' else 'normal'} |\n")
print("KIT OK", len(rows), "vídeos", len(txt), "textos")
