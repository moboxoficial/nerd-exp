#!/bin/bash
# troca os frames [162,261) [1440,1515) [1575,1800) do v2 pelos trechos corrigidos
cd ${NXP_WORK:-$(dirname $0)/..}/out
M=NXP2027_aftermovie_60s_v2_video.mp4
ffmpeg -hide_banner -loglevel error -y -i $M -i v2fix_A_video.mp4 -i v2fix_B2_video.mp4 -i v2fix_C_video.mp4 -filter_complex \
"[0:v]trim=start_frame=0:end_frame=162,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];\
[0:v]trim=start_frame=261:end_frame=1440,setpts=PTS-STARTPTS[c];[2:v]setpts=PTS-STARTPTS[d];\
[3:v]setpts=PTS-STARTPTS[f];\
[a][b][c][d][f]concat=n=5:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 15 -preset slow -pix_fmt yuv420p -r 30 NXP2027_aftermovie_60s_v2b_video.mp4
ffmpeg -hide_banner -loglevel error -y -i NXP2027_aftermovie_60s_v2b_video.mp4 -i v2fix_audio.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart NXP2027_aftermovie_60s_v2b.mp4
ffmpeg -hide_banner -i NXP2027_aftermovie_60s_v2b.mp4 2>&1 | grep Duration
echo SPLICED
