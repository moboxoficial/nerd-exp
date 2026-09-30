#!/usr/bin/env python3
"""Gera LUTs 3D (33^3) "NXP look" já compostas com a conversão de cada câmera.
Saída em luts/: nxp_slog3.cube (Sony S-Log3 SGamut3.Cine), nxp_dlogm.cube (DJI D-Log M),
nxp_rec709.cube (celular/Rec709). Look: contraste S, saturação/vibrance, sombras roxas
(cor base do KV #291833 / #49236c) e altas levemente ciano (#11fafe), pretos 'matte' roxos."""
import numpy as np, os, sys

D = os.path.join(os.path.dirname(__file__), "..", "luts")
N = 33

def read_cube(p):
    size, rows = None, []
    for line in open(p, errors="ignore"):
        s = line.strip()
        if not s or s[0] == "#" or s.startswith("TITLE") or s.startswith("DOMAIN"):
            continue
        if s.startswith("LUT_3D_SIZE"):
            size = int(s.split()[1]); continue
        if s.startswith("LUT_1D_SIZE"):
            raise ValueError("1D LUT")
        parts = s.split()
        if len(parts) == 3:
            try: rows.append([float(x) for x in parts])
            except ValueError: pass
    a = np.array(rows, dtype=np.float64)
    return a.reshape(size, size, size, 3)  # indexado [b][g][r] (r varia mais rápido)

def apply_cube(lut, rgb):
    """trilinear; rgb (...,3) em [0,1]"""
    n = lut.shape[0]
    p = np.clip(rgb, 0, 1) * (n - 1)
    i0 = np.floor(p).astype(int); i1 = np.minimum(i0 + 1, n - 1); f = p - i0
    r0, g0, b0 = i0[..., 0], i0[..., 1], i0[..., 2]
    r1, g1, b1 = i1[..., 0], i1[..., 1], i1[..., 2]
    fr, fg, fb = f[..., 0:1], f[..., 1:2], f[..., 2:3]
    def L(b, g, r): return lut[b, g, r]
    c00 = L(b0, g0, r0) * (1 - fr) + L(b0, g0, r1) * fr
    c01 = L(b0, g1, r0) * (1 - fr) + L(b0, g1, r1) * fr
    c10 = L(b1, g0, r0) * (1 - fr) + L(b1, g0, r1) * fr
    c11 = L(b1, g1, r0) * (1 - fr) + L(b1, g1, r1) * fr
    c0 = c00 * (1 - fg) + c01 * fg; c1 = c10 * (1 - fg) + c11 * fg
    return c0 * (1 - fb) + c1 * fb

def look(rgb, exposure=0.0):
    x = np.clip(rgb * (2 ** exposure), 0, 1)
    l = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    # contraste S (sigmoide suave em torno de 0.45)
    k = 1.18
    def s(v): return 0.5 + (v - 0.5) * k - 0.5 * (k - 1) * (v - 0.5) * np.abs(v - 0.5) * 2 * 0.9
    x = np.clip(s(x), 0, 1)
    l = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    # vibrance: satura mais o que é pouco saturado
    mx = x.max(-1, keepdims=True); mn = x.min(-1, keepdims=True); sat = mx - mn
    amt = 1.22 + 0.25 * (1 - np.clip(sat * 2, 0, 1))
    x = l + (x - l) * amt
    # split-tone
    sh = (1 - l) ** 2.2; hi = l ** 2.5
    x = x + sh * np.array([0.030, -0.012, 0.055]) * 0.8 + hi * np.array([-0.015, 0.008, 0.022])
    # pretos matte roxos (piso ~ #140a1c)
    floor = np.array([0.035, 0.014, 0.050])
    x = floor + x * (1 - floor * 0.9)
    # roll-off de altas (evita estouro de janela)
    kn = 0.82
    x = np.where(x > kn, kn + (1 - kn) * np.tanh((x - kn) / (1 - kn)), x)
    return np.clip(x, 0, 1)

def write_cube(p, fn, title):
    g = np.linspace(0, 1, N)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([r, gg, b], -1)  # [b][g][r]
    out = fn(rgb)
    with open(p, "w") as f:
        f.write(f'TITLE "{title}"\nLUT_3D_SIZE {N}\n')
        for v in out.reshape(-1, 3):
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

slog3 = read_cube(os.path.join(D, "slog3_to_lc709typeA.cube"))
dji = read_cube(os.path.join(D, "dji_dlogm_to_709.cube"))
write_cube(os.path.join(D, "nxp_slog3.cube"), lambda c: look(apply_cube(slog3, c), 0.0), "NXP look S-Log3")
write_cube(os.path.join(D, "nxp_dlogm.cube"), lambda c: look(apply_cube(dji, c), 0.0), "NXP look D-Log M")
write_cube(os.path.join(D, "nxp_rec709.cube"), lambda c: look(c * 0.97 + 0.0, -0.05), "NXP look Rec709")
# versão só-conversão (para comparar antes/depois)
write_cube(os.path.join(D, "conv_slog3.cube"), lambda c: apply_cube(slog3, c), "Sony LC709TypeA")
print("ok")
