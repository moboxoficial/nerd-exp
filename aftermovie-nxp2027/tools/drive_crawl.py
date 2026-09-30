#!/usr/bin/env python3
"""Varre recursivamente pastas PÚBLICAS do Google Drive via embeddedfolderview.
Uso: drive_crawl.py <saida.jsonl> <rotulo>=<folder_id> [...]
Cada linha: {rotulo, path, id, name, kind(file|folder), mtime}"""
import html, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ENTRY = re.compile(
    r'<div class="flip-entry" id="entry-([^"]+)".*?<a href="([^"]+)".*?flip-entry-title">([^<]*)<.*?flip-entry-last-modified"><div>([^<]*)<',
    re.S)

def list_folder(fid):
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60",
                        f"https://drive.google.com/embeddedfolderview?id={fid}"],
                       capture_output=True, text=True)
    out = []
    for eid, href, name, mtime in ENTRY.findall(r.stdout):
        kind = "folder" if "/folders/" in href else "file"
        out.append({"id": eid, "name": html.unescape(name), "kind": kind, "mtime": mtime})
    return out

def crawl(label, fid, path, fh):
    items = list_folder(fid)
    subs = []
    for it in items:
        it.update({"rotulo": label, "path": path})
        fh.write(json.dumps(it, ensure_ascii=False) + "\n"); fh.flush()
        if it["kind"] == "folder":
            subs.append(it)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda s: crawl(label, s["id"], f'{path}/{s["name"]}', fh), subs))

if __name__ == "__main__":
    out = open(sys.argv[1], "w")
    for arg in sys.argv[2:]:
        label, fid = arg.split("=", 1)
        crawl(label, fid, label, out)
