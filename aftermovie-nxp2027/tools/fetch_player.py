"""Baixa o stream do player do Drive (transcode até 1080p, não consome a cota de download)
para cada clipe da seleção. Saída: raw/player/<code>.mp4 + raw/player/index.json"""
import json, subprocess, sys, os, re
S = os.environ.get('NXP_WORK', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sel=json.load(open(sys.argv[1])); os.makedirs(f'{S}/raw/player', exist_ok=True)
out=f'{S}/raw/player/index.json'
done=json.load(open(out)) if os.path.exists(out) else {}
for o in sel:
    if o['code'] in done and 'erro' not in done[o['code']]: continue
    f=f"{S}/raw/player/{o['code']}.mp4"
    r=subprocess.run(['yt-dlp','-q','--no-warnings','-f','37/137+140/22/136+140/best','--merge-output-format','mp4',
                      '-o',f,f"https://drive.google.com/file/d/{o['id']}/view"],capture_output=True,text=True,timeout=900)
    info={'code':o['code'],'role':o['role'],'lut':o['lut'],'id':o['id']}
    if os.path.exists(f) and ' Duration:' in subprocess.run(['ffmpeg','-hide_banner','-i',f],capture_output=True,text=True).stderr and 'Video:' in subprocess.run(['ffmpeg','-hide_banner','-i',f],capture_output=True,text=True).stderr:
        e=subprocess.run(['ffmpeg','-hide_banner','-i',f],capture_output=True,text=True).stderr
        m=re.search(r"Duration: (\d+):(\d+):([\d.]+)",e); v=re.search(r"Video:.*?, (\d+)x(\d+)",e)
        info.update(arquivo=f, dur=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3)), w=int(v.group(1)), h=int(v.group(2)), audio=' Audio:' in e)
    else:
        info['erro']=(r.stderr or r.stdout)[-300:]
    done[o['code']]=info; json.dump(done,open(out,'w'),indent=1)
    print(o['code'], info.get('w'), info.get('h'), info.get('dur'), info.get('erro','')[:100], flush=True)
print('FIM')
