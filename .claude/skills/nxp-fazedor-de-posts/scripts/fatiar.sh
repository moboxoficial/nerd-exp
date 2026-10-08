#!/usr/bin/env bash
# Baixa o PNG exportado do Canva, fatia em slides 1080x1350 e gera imagens de QA.
#
# Uso: fatiar.sh "<url do export-design>" <pasta de entregas> [pasta de QA]
#   - grava slide-1.png ... slide-N.png na pasta de entregas
#   - grava preview.png (tira reduzida) e divisa-K.png (zoom em cada divisa) na pasta de QA
set -euo pipefail

url="$1"
dest="$2"
qa="${3:-$dest/.qa}"

mkdir -p "$dest" "$qa"
full="$qa/full.png"

curl -sSf -o "$full" "$url"

width=$(identify -format '%w' "$full")
height=$(identify -format '%h' "$full")
slides=$(( width / 1080 ))

if (( width % 1080 != 0 )) || (( height != 1350 && height != 1920 )); then
  echo "Aviso: ${width}x${height} não é múltiplo de 1080 de largura (feed 1350 / story 1920 de altura)." >&2
fi

rm -f "$dest"/slide-*.png
for (( i = 0; i < slides; i++ )); do
  convert "$full" -crop "1080x${height}+$(( i * 1080 ))+0" +repage "$dest/slide-$(( i + 1 )).png"
done

convert "$full" -resize 1620x "$qa/preview.png"

# Zoom de 200 px para cada lado de cada divisa: é onde aparecem cortes de rosto/texto e elementos vazando.
for (( k = 1; k < slides; k++ )); do
  convert "$full" -crop "400x${height}+$(( k * 1080 - 200 ))+0" +repage -resize x700 "$qa/divisa-$k.png"
done

echo "OK: $slides slide(s) ${width}x${height} -> $dest"
echo "QA: $qa/preview.png e $qa/divisa-*.png"
