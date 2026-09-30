import json, subprocess, sys, time, os
S=os.environ.get('NXP_WORK', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
idx=json.load(open(f'{S}/raw/player/index.json'))
oi=f'{S}/raw/orig/index.json'; done=json.load(open(oi)) if os.path.exists(oi) else {}
for code in sys.argv[1:]:
    if code in done and 'arquivo' in done[code]: continue
    v=idx[code]
    r=subprocess.run(['python3',f'{S}/tools/fetch.py',v['id'],'0',str(v['dur']),'none',f'{S}/raw/orig/{code}.mp4'],capture_output=True,text=True)
    try: info=json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: info={'erro':r.stderr[-200:]}
    done[code]=info; json.dump(done,open(oi,'w'),indent=1)
    print(code, 'OK' if 'arquivo' in info else 'ERRO', flush=True); time.sleep(15)
print('FIM')
