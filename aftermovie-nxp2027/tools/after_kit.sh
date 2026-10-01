#!/bin/bash
cd /tmp/claude-0/-home-user-nerd-exp/5fc0b895-bc87-598f-81ab-980c65934114/scratchpad
until grep -q "KIT OK" out/capcut_kit.log; do
  if ! ps aux | grep -v grep | grep -q "tools/capcut_kit.py"; then echo "KIT MORREU"; exit 1; fi
  sleep 20
done
mkdir -p out/capcut_kit/video_envio
for v in out/capcut_kit/video/*.mp4; do
  ffmpeg -hide_banner -loglevel error -y -i "$v" -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p -movflags +faststart out/capcut_kit/video_envio/$(basename "$v")
done
python3 tools/capcut_draft.py
echo AFTER_DONE
