"""Scout Notizbuch start-screen backdrop: a dark scout's desk with English
newspapers, an open notebook with a tactics sketch, pencil and coffee ring.
Everything sits right of x=820 (the menu tiles cover the left).
Writes assets/backgrounds/scout-desk.png."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

out = sys.argv[1]
W, H = 1920, 1080
BG = (27, 25, 21)
GOLD = (183, 160, 110)
NEWS = (170, 160, 138)      # aged newsprint, kept dim for the dark theme
NEWS_INK = (46, 42, 36)
PAD = (196, 184, 154)       # notebook paper
GRAPHITE = (58, 54, 48)
RED = (150, 62, 46)
F = "C:/Windows/Fonts/"
random.seed(27)


def font(name, size):
    return ImageFont.truetype(F + name, size)


def fit(d, text, name, w_max, start):
    s = start
    while s > 10 and d.textlength(text, font=font(name, s)) > w_max:
        s -= 1
    return font(name, s)


def body_lines(d, x0, y0, x1, y1, ink, gap=13, h=4):
    y = y0
    while y + h <= y1:
        end = x1 if random.random() > 0.12 else x0 + (x1 - x0) * random.uniform(0.3, 0.8)
        d.rectangle((x0, y, end, y + h), fill=ink)
        y += gap


def halftone(d, box, ink, kind):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(150, 141, 120))
    step = 7
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            u, v = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
            if kind == "stadium":
                t = 0.25 + 0.5 * v
                if v > 0.55 + 0.08 * math.sin(u * 9):       # stands
                    t = 0.85
                if abs(u - 0.15) < 0.015 and v < 0.6 or abs(u - 0.85) < 0.015 and v < 0.6:  # floodlights
                    t = 0.95
                if v > 0.88:                                 # pitch edge
                    t = 0.55
            else:                                            # player silhouette, arms up
                t = 0.2 + 0.3 * v
                cx = 0.5
                if (u - cx) ** 2 / 0.012 + (v - 0.28) ** 2 / 0.012 < 1 or \
                   abs(u - cx) < 0.13 and 0.38 < v < 0.8 or \
                   abs(u - cx - 0.2 + v * 0.25) < 0.04 and 0.12 < v < 0.45 or \
                   abs(u - cx + 0.2 - v * 0.25) < 0.04 and 0.12 < v < 0.45 or \
                   abs(u - cx) < 0.13 and v >= 0.8:
                    t = 0.9
            r = step * 0.55 * min(1, t)
            d.ellipse((x - r, y - r, x + r, y + r), fill=ink)


def newspaper(w, h, mast, date, head, sub, side, kind):
    p = Image.new("RGBA", (w, h), NEWS + (255,))
    d = ImageDraw.Draw(p)
    m = 30
    f_m = fit(d, mast, "georgiab.ttf", w - 2 * m, 72)
    d.text((w / 2, m + 4), mast, font=f_m, fill=NEWS_INK, anchor="mt")
    yb = m + 4 + f_m.size + 14
    d.line((m, yb, w - m, yb), fill=NEWS_INK, width=3)
    d.text((m, yb + 8), date, font=font("times.ttf", 15), fill=NEWS_INK)
    d.text((w - m, yb + 8), "PRICE £1.80", font=font("times.ttf", 15), fill=NEWS_INK, anchor="ra")
    d.line((m, yb + 32, w - m, yb + 32), fill=NEWS_INK, width=1)
    y = yb + 48
    # headline, wrapped
    f_h = font("timesbd.ttf", 54)
    words, line, lines = head.split(), "", []
    for wd in words:
        t = (line + " " + wd).strip()
        if d.textlength(t, font=f_h) > w - 2 * m:
            lines.append(line)
            line = wd
        else:
            line = t
    lines.append(line)
    for ln in lines:
        d.text((m, y), ln, font=f_h, fill=NEWS_INK)
        y += 58
    d.text((m, y + 4), sub, font=font("timesi.ttf", 24), fill=NEWS_INK)
    y += 44
    ph = int(h * 0.30)
    halftone(d, (m, y, int(w * 0.62), y + ph), NEWS_INK, kind)
    body_lines(d, int(w * 0.62) + 16, y, w - m, y + ph, NEWS_INK + (150,))
    y += ph + 18
    d.line((m, y, w - m, y), fill=NEWS_INK, width=1)
    y += 12
    d.text((m, y), side, font=font("timesbd.ttf", 26), fill=NEWS_INK)
    y += 40
    cw = (w - 2 * m - 2 * 18) / 3
    for c in range(3):
        cx0 = m + c * (cw + 18)
        body_lines(d, cx0, y, cx0 + cw, h - m, NEWS_INK + (140,))
    # fold crease + age
    d.line((0, h * 0.52, w, h * 0.52), fill=(120, 112, 96, 90), width=2)
    return p


def notebook(w, h):
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rectangle((0, 0, w, h), fill=PAD + (255,))
    for y in range(110, h - 20, 30):                       # ruling
        d.line((24, y, w - 24, y), fill=(120, 140, 160, 70), width=1)
    d.line((70, 0, 70, h), fill=(170, 80, 70, 110), width=2)  # margin
    for x in range(40, w - 20, 34):                        # spiral holes
        d.ellipse((x - 7, 14, x + 7, 28), fill=BG + (255,))
        d.arc((x - 9, -6, x + 9, 24), 200, 340, fill=(90, 86, 80), width=3)
    hand = lambda s: font("Inkfree.ttf", s)
    d.text((90, 52), "vs. high press  (4-2-3-1)", font=hand(34), fill=GRAPHITE)
    # pitch sketch
    x0, y0, x1, y1 = 100, 130, w - 60, 130 + int((w - 160) * 0.78)
    lw = 3
    d.rectangle((x0, y0, x1, y1), outline=GRAPHITE, width=lw)
    cx = (x0 + x1) / 2
    d.line((x0, (y0 + y1) / 2, x1, (y0 + y1) / 2), fill=GRAPHITE, width=2)
    d.ellipse((cx - 45, (y0 + y1) / 2 - 45, cx + 45, (y0 + y1) / 2 + 45), outline=GRAPHITE, width=2)
    d.rectangle((cx - 110, y0, cx + 110, y0 + 70), outline=GRAPHITE, width=2)
    d.rectangle((cx - 110, y1 - 70, cx + 110, y1), outline=GRAPHITE, width=2)
    pw, phh = x1 - x0, y1 - y0
    P = lambda u, v: (x0 + u * pw, y0 + v * phh)
    team = [(.5, .93), (.18, .78), (.39, .8), (.61, .8), (.82, .78), (.38, .64), (.62, .64),
            (.2, .44), (.5, .48), (.8, .44), (.5, .27)]
    for u, v in team:
        x, y = P(u, v)
        d.ellipse((x - 11, y - 11, x + 11, y + 11), outline=GRAPHITE, width=3)
    for u, v in [(.3, .3), (.55, .2), (.72, .32), (.45, .38), (.62, .52)]:
        x, y = P(u, v)
        d.line((x - 8, y - 8, x + 8, y + 8), fill=GRAPHITE, width=3)
        d.line((x - 8, y + 8, x + 8, y - 8), fill=GRAPHITE, width=3)

    def arrow(a, b, bend, col=GRAPHITE, dash=True):
        (ax, ay), (bx, by) = P(*a), P(*b)
        mx, my = (ax + bx) / 2 + bend[0], (ay + by) / 2 + bend[1]
        pts = [((1 - t) ** 2 * ax + 2 * (1 - t) * t * mx + t * t * bx,
                (1 - t) ** 2 * ay + 2 * (1 - t) * t * my + t * t * by) for t in [i / 40 for i in range(41)]]
        for i in range(0, 39, 3 if dash else 1):
            d.line((*pts[i], *pts[i + (2 if dash else 1)]), fill=col, width=3)
        ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
        for s in (2.6, -2.6):
            d.line((*pts[-1], pts[-1][0] + 14 * math.cos(ang + s), pts[-1][1] + 14 * math.sin(ang + s)), fill=col, width=3)

    arrow((.2, .44), (.24, .2), (-30, 0))
    arrow((.5, .48), (.4, .31), (-20, 10))
    arrow((.62, .64), (.8, .3), (40, 20))
    arrow((.38, .64), (.2, .44), (0, 20), dash=False)
    # red pen: overload zone + key player
    zx0, zy0 = P(.08, .22)
    zx1, zy1 = P(.42, .52)
    d.ellipse((zx0, zy0, zx1, zy1), outline=RED, width=3)
    x, y = P(.5, .48)
    d.ellipse((x - 22, y - 22, x + 22, y + 22), outline=RED, width=3)
    y = y1 + 26
    notes = ["- overload left half-space", "- #10 drops between the lines", "- press trigger: back pass to CB",
             "- watch their RB, slow on the turn!"]
    for i, n in enumerate(notes):
        d.text((90, y + i * 30), n, font=hand(25), fill=RED if i == 3 else GRAPHITE)
    return p


def place(canvas, layer, cx, cy, angle, shadow=18):
    lay = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    a = lay.split()[3]
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: v * 0.7))
    sh = sh.filter(ImageFilter.GaussianBlur(shadow))
    x, y = int(cx - lay.width / 2), int(cy - lay.height / 2)
    canvas.paste((0, 0, 0, 255), (x + 10, y + 16), sh)
    canvas.paste(lay, (x, y), lay)


img = Image.new("RGBA", (W, H), BG + (255,))
d = ImageDraw.Draw(img)
# faint dot grid on the desk blotter
for y in range(24, H, 24):
    for x in range(24, W, 24):
        d.ellipse((x - 0.9, y - 0.9, x + 0.9, y + 0.9), fill=GOLD + (14,))

p1 = newspaper(640, 900, "THE TOUCHLINE", "SUNDAY, 1 NOVEMBER 2026",
               "YELLOW WALL ERUPTS AS LATE WINNER SEALS TOP SPOT", "Statement victory sends title race wide open",
               "Scouts flock to see 17-year-old prodigy", "stadium")
p2 = newspaper(560, 780, "The Football Gazette", "TRANSFER SPECIAL  ·  NO. 2,727",
               "DEADLINE DAY: RECORD BID REJECTED", "'We are not a selling club,' insists manager",
               "Wonderkid hands in transfer request", "player")
nb = notebook(540, 760)

place(img, p2, 1720, 300, 8)
place(img, p1, 1190, 470, -6)
place(img, nb, 1640, 790, 5, shadow=24)

# pencil across the notebook corner
pen = Image.new("RGBA", (520, 26), (0, 0, 0, 0))
pd = ImageDraw.Draw(pen)
pd.rectangle((40, 3, 470, 23), fill=(176, 138, 64, 255))
pd.line((40, 9, 470, 9), fill=(196, 160, 86, 255), width=3)
pd.rectangle((470, 3, 505, 23), fill=(150, 150, 140, 255))
pd.rectangle((505, 3, 520, 23), fill=(180, 110, 100, 255))
pd.polygon([(40, 3), (40, 23), (0, 13)], fill=(214, 190, 150, 255))
pd.polygon([(12, 9), (12, 17), (0, 13)], fill=(50, 48, 44, 255))
place(img, pen, 1180, 985, 14, shadow=8)

# coffee ring
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ring)
for i in range(6):
    r = 92 + i * 1.5
    rd.ellipse((980 - r, 900 - r, 980 + r, 900 + r), outline=(90, 60, 30, 26 - i * 3), width=4)
img.alpha_composite(ring.filter(ImageFilter.GaussianBlur(1.5)))

img = img.convert("RGB")
# dim the props so the paper never glares against the dark skin
lum = Image.new("L", (W, H), 0)
ImageDraw.Draw(lum).rectangle((0, 0, W, H), fill=192)
img = ImageChops.multiply(img, Image.merge("RGB", [lum] * 3))
# grain + vignette, darker towards the menu on the left
noise = Image.effect_noise((W, H), 14).convert("L")
img = Image.blend(img, Image.merge("RGB", [noise] * 3), 0.04)
vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse((W * 0.30, -H * 0.4, W * 1.35, H * 1.4), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(260))
img = Image.composite(img, Image.new("RGB", (W, H), (16, 15, 12)), vig)
img.save(out, optimize=True)
print(out)
