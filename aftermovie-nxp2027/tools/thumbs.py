import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
v = json.load(open('videos.json'))
prefs = sys.argv[1:]
todo = [d for d in v if any(d['path'].startswith(p) for p in prefs) and not os.path.exists(f"thumbs/{d['id']}.jpg")]
print(len(todo), flush=True)
def get(d):
    subprocess.run(["curl", "-sS", "-L", "--max-time", "40", "-o", f"thumbs/{d['id']}.jpg",
                    f"https://drive.google.com/thumbnail?id={d['id']}&sz=w400"], capture_output=True)
with ThreadPoolExecutor(6) as ex: list(ex.map(get, todo))
print("ok")
