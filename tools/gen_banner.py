"""Replacement for the marketing video banner: a newspaper-style clipping
"VIDEO GUIDES" strip. Writes assets/backgrounds/guides-banner.png (2x of 640x112)."""
import sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
W, H = 1280, 224
PANEL = (42, 39, 35)
GOLD = (183, 160, 110)
TEXT = (216, 204, 178)
DIM = (150, 138, 112)
F = "C:/Windows/Fonts/"

img = Image.new("RGB", (W, H), PANEL)
d = ImageDraw.Draw(img, "RGBA")
for y in range(0, H, 3):                                   # faint newsprint texture
    d.line((0, y, W, y), fill=GOLD + (6,))
d.rectangle((0, 0, 6, H), fill=GOLD)
d.text((44, 38), "FOOTBALL MANAGER 27  ·  LEARN THE GAME", font=ImageFont.truetype(F + "georgia.ttf", 24), fill=DIM)
d.line((44, 78, 760, 78), fill=GOLD + (90,), width=2)
d.text((40, 92), "Video Guides", font=ImageFont.truetype(F + "georgiab.ttf", 84), fill=TEXT)
# stamp on the right
cx, cy = 1110, 112
d.ellipse((cx - 84, cy - 84, cx + 84, cy + 84), outline=GOLD + (200,), width=4)
d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=GOLD + (120,), width=2)
d.polygon([(cx - 22, cy - 34), (cx - 22, cy + 34), (cx + 36, cy)], fill=GOLD + (220,))
d.text((cx - 190, cy), "WATCH", font=ImageFont.truetype(F + "georgiab.ttf", 30), fill=GOLD, anchor="rm")
img.save(out, optimize=True)
print(out)
