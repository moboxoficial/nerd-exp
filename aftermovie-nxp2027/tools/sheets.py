import json, os
from PIL import Image, ImageDraw, ImageFont
v = json.load(open('videos.json'))
F = ImageFont.truetype(os.path.expanduser('~/.fonts/LexendDeca.ttf'), 13)
groups = {}
for d in v:
    if os.path.exists(f"thumbs/{d['id']}.jpg"):
        top = d['path'].split('/')[0]
        groups.setdefault(top, []).append(d)
os.makedirs('sheets', exist_ok=True)
index = {}
for g, items in groups.items():
    items.sort(key=lambda d: (d['path'], d['name']))
    for s in range(0, len(items), 40):
        chunk = items[s:s+40]; cols = 8; tw, th = 230, 190
        sheet = Image.new('RGB', (cols*tw, ((len(chunk)+cols-1)//cols)*th), 'black'); dr = ImageDraw.Draw(sheet)
        for k, d in enumerate(chunk):
            code = f"{g[:4]}{g.split('_',1)[1][:3] if '_' in g else ''}-{s+k:04d}"
            index[code] = d
            try:
                im = Image.open(f"thumbs/{d['id']}.jpg").convert('RGB'); im.thumbnail((tw-6, th-38))
            except Exception:
                continue
            x, y = (k % cols)*tw, (k//cols)*th
            sheet.paste(im, (x+3, y+3))
            sub = d['path'].split('/')[-1][:24]
            dr.text((x+3, y+th-34), code, fill='yellow', font=F)
            dr.text((x+3, y+th-18), f"{sub}", fill='white', font=F)
        sheet.save(f"sheets/{g}_{s//40:02d}.jpg", quality=78)
json.dump(index, open('sheets/index.json', 'w'), ensure_ascii=False)
print(len(index)); print(sorted(os.listdir('sheets'))[:5], len(os.listdir('sheets')))
