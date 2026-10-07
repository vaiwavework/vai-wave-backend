# Clip tool: Brad thread, video HI1PVF4l0Hs

Captions follow the Cole Gordan 3-5 word spec (Inter Medium, 87px @1080p, ScaleX 88, no outline, 50% black shadow).

- `words.json`: word timings from the video's YouTube auto-captions (json3).
- `clipdefs.json`: exact clip ranges in SOURCE seconds, keyed by tweet number. Tweets 1, 8, 9 get no clip.
- `make_ass.py`: builds the ASS per spec PART 3 and 4.
- `render.sh <video_1080p.mp4> <out_dir>`: cuts and burns all clips. Needs ffmpeg with libass and the Inter Medium font installed.

| Tweet | Source range | Topic |
|---|---|---|
| 2 | 6:15.04 to 7:23.10 | liquidity sweep, imbalance refill |
| 3 | 16:39.52 to 18:44.40 | timeframe jobs, wait for zone |
| 4 | 20:36.96 to 22:12.10 | premium/discount, supply in premium |
| 5 | 24:21.36 to 26:54.30 | sessions on EUR/USD |
| 6 | 29:43.92 to 31:17.70 | internal vs external range |
| 7 | 32:47.84 to 33:18.55 | 3-sentence entry process |
| 10 | 0:12.32 to 0:30.75 | intro: 5 secrets and checklist |

Download the source locally (cloud servers get blocked by YouTube):
`yt-dlp -f "299+140/bv*[height=1080]+ba" --merge-output-format mp4 -o video.mp4 "https://www.youtube.com/watch?v=HI1PVF4l0Hs"`
