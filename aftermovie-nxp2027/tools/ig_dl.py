#!/usr/bin/env python3
"""Baixa um post/reel público do Instagram via página /embed (não exige login).
Uso: ig_dl.py <url_ou_shortcode> <saida.mp4>
Imprime JSON com legenda, autor e duração quando disponível."""
import json, re, subprocess, sys

src, out = sys.argv[1], sys.argv[2]
m = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", src)
code = m.group(1) if m else src
url = f"https://www.instagram.com/p/{code}/embed/captioned/"
html = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
vm = re.search(r'video_url\\":\\"(.*?)\\"', html)
if not vm:
    print(json.dumps({"code": code, "error": "sem video_url (post é foto, privado ou bloqueado)"}))
    sys.exit(1)
vurl = vm.group(1).replace("\\\\/", "/").replace("\\/", "/")
vurl = vurl.encode().decode("unicode_escape")
subprocess.run(["curl", "-sS", "-L", "-A", "Mozilla/5.0", "-o", out, vurl], check=True)
cap = re.search(r'class="Caption"[^>]*>(.*?)</div>', html, re.S)
caption = re.sub(r"<[^>]+>", " ", cap.group(1)).strip() if cap else ""
owner = re.search(r'"username\\":\\"(.*?)\\"', html)
print(json.dumps({"code": code, "file": out, "owner": owner.group(1) if owner else None,
                  "caption": caption[:1500]}, ensure_ascii=False))
