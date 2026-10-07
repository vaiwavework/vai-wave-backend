#!/bin/bash
# Cuts each clip in clipdefs.json from the source video and burns Cole Gordan 3-5 word captions.
# Usage: bash clip-tool/render.sh <source_1080p.mp4> <out_dir>
set -e
SRC="$1"; OUT="${2:-clips}"; DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
python3 - "$DIR" "$OUT" <<'PY'
import json,sys,os
d,out=sys.argv[1],sys.argv[2]
os.chdir(d); sys.path.insert(0,d)
import make_ass
for k,(a,b) in json.load(open('clipdefs.json')).items():
    print(k, make_ass.build(a,b,os.path.join(os.path.abspath(out) if not os.path.isabs(out) else out, k+'.ass')))
PY
for k in $(python3 -c "import json;print(' '.join(json.load(open('$DIR/clipdefs.json'))))"); do
  read A B < <(python3 -c "import json;a,b=json.load(open('$DIR/clipdefs.json'))['$k'];print(a,b)")
  ffmpeg -y -v error -ss "$A" -to "$B" -i "$SRC" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 160k "$OUT/$k.raw.mp4"
  ffmpeg -y -v error -i "$OUT/$k.raw.mp4" -vf "subtitles=$OUT/$k.ass" \
    -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT/$k.mp4"
  rm "$OUT/$k.raw.mp4"; echo "rendered $OUT/$k.mp4"
done
