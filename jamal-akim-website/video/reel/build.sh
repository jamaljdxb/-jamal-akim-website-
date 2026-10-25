#!/bin/bash
# Real-footage brand reel: graded iPhone clips + brand typography + generated beat.
#   video/reel/build.sh <clips dir>
# Expects IMG_3811, IMG_4245, IMG_4144, IMG_4133 (.mov) in the clips dir.
# Outputs video/out/reel-v.mp4 (1080x1920) and video/out/reel-h.mp4 (1920x1080).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
OUT=$HERE/../out
TMP=$(mktemp -d)
mkdir -p "$OUT"

# order and lengths match SHOTS in overlay.html (2.9, 3.1, 4.4, 6.0 s)
clip() { ls "$SRC"/*"$1"*.mov | head -1; }
GRADE="eq=contrast=1.12:brightness=-0.03:saturation=1.08:gamma=0.96,unsharp=5:5:0.4,vignette=PI/6"
i=0
for spec in "IMG_3811:0:2.9" "IMG_4245:0:3.1" "IMG_4144:0:4.4" "IMG_4133:0:6.0"; do
  IFS=: read name ss len <<< "$spec"
  f=$(clip "$name")
  # vertical: full portrait frame
  ffmpeg -loglevel error -y -ss "$ss" -t "$len" -i "$f" -an \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,$GRADE,fps=30" \
    -c:v libx264 -crf 16 -preset fast "$TMP/v$i.mp4"
  # horizontal: footage panel on the right 44% of a 1920x1080 frame
  ffmpeg -loglevel error -y -ss "$ss" -t "$len" -i "$f" -an \
    -vf "scale=845:-2,crop=845:1080:0:(ih-1080)*0.25,$GRADE,fps=30,pad=1920:1080:1075:0:0x0E0E0E" \
    -c:v libx264 -crf 16 -preset fast "$TMP/h$i.mp4"
  i=$((i + 1))
done
# end card background (overlay paints it blue)
for m in v h; do
  [ $m = v ] && size=1080x1920 || size=1920x1080
  ffmpeg -loglevel error -y -f lavfi -i "color=c=0x2B3DF5:s=$size:d=2.6:r=30" -c:v libx264 -crf 16 "$TMP/${m}4.mp4"
  printf "file '%s'\n" "$TMP/${m}0.mp4" "$TMP/${m}1.mp4" "$TMP/${m}2.mp4" "$TMP/${m}3.mp4" "$TMP/${m}4.mp4" > "$TMP/$m.txt"
  ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/$m.txt" -c copy "$TMP/$m-base.mp4"
done

# beat: 120 bpm kick + offbeat hat + A minor pad, faded
ffmpeg -loglevel error -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*(45+70*exp(-mod(t,0.5)*30))*mod(t,0.5))*exp(-mod(t,0.5)*9)+0.05*(random(0)*2-1)*exp(-mod(t+0.25,0.5)*70)+0.05*(sin(2*PI*220*t)+sin(2*PI*261.6*t)+sin(2*PI*329.6*t))*(0.8+0.2*sin(2*PI*0.25*t))':s=48000:d=19" \
  -af "afade=t=in:d=1,afade=t=out:st=16.5:d=2.5,loudnorm=I=-14:TP=-1.5" -ac 2 "$TMP/beat.wav"

# typography overlay rendered with alpha, composited over the footage
for m in v h; do
  node "$HERE/overlay.cjs" $m | ffmpeg -loglevel error -y -i "$TMP/$m-base.mp4" -f image2pipe -framerate 30 -c:v png -i - -i "$TMP/beat.wav" \
    -filter_complex "[0][1]overlay=format=auto" -map 2:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT/reel-$m.mp4"
  echo "$OUT/reel-$m.mp4"
done
rm -rf "$TMP"
