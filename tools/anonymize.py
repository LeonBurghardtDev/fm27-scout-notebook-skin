"""Prepare public screenshots: paint over the FPS counter, pixelate real player
photos. Reads shots/pub_<name>_raw.png, writes <outdir>/<nn>-<name>.png."""
import sys
from pathlib import Path
from PIL import Image

shots, outdir = Path(sys.argv[1]), Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)

# full-res (1920x1080) boxes to pixelate, per screen
PIXELATE = {
    "menu": [],
    "squad": [(300, 405, 338, 1020)],          # face column in the squad list
    "tactics": [],
    "scouting": [(42, 975, 80, 1035)],         # agent-offer faces, bottom left
    "player": [(0, 97, 180, 313)],             # player photo
}
ORDER = ["menu", "squad", "tactics", "player", "scouting"]


def pixelate(img, box, block=14):
    reg = img.crop(box)
    small = reg.resize((max(1, reg.width // block), max(1, reg.height // block)), Image.BILINEAR)
    img.paste(small.resize(reg.size, Image.NEAREST), box)


for i, name in enumerate(ORDER, 1):
    img = Image.open(shots / f"pub_{name}_raw.png").convert("RGB")
    # FPS overlay box sits at (0,0)-(36,11), partly over the back button: rebuild
    # it row by row from the pixels just right of it (button) or below it (bar)
    px = img.load()
    for y in range(0, 12):
        for x in range(0, 37):
            px[x, y] = px[44, y] if x >= 17 else px[x, 13]
    for y in range(0, 40):            # frame-time bar along the left edge
        for x in range(0, 6):
            px[x, y] = px[8, y]
    for box in PIXELATE[name]:
        pixelate(img, box)
    out = outdir / f"{i:02d}-{name}.png"
    img.save(out, optimize=True)
    print(out)
