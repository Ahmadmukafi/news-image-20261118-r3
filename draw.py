#!/usr/bin/env python3
"""Draw the front page for 18 November 2026.

Bright broadsheet, one big PIL-drawn Gulf map, one giant headline,
three supporting stories and a news ticker. No network, deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 46)
NAVY = (20, 33, 61)
RED = (180, 35, 24)
SEA = (191, 217, 232)
LAND = (232, 220, 195)
SAND = (214, 196, 160)
GREY = (90, 90, 100)
RULE = (26, 26, 46)

F = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def fit(name, size, max_w, text):
    while size > 10 and d.textlength(text, font=font(name, size)) > max_w:
        size -= 2
    return font(name, size)

def text_center(y, s, fnt, fill=INK):
    d.text((W // 2, y), s, font=fnt, fill=fill, anchor="ma")

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def rule(y, x0=36, x1=988, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

MX = 36          # margin
CW = 952         # content width

# ---------- masthead ----------
y = 30
text_center(y, "THE WORLD IN ONE DAY", font(SERIF_B, 64), NAVY)
y = 108
rule(y)
y = 118
text_center(y, "WEDNESDAY 18 NOVEMBER 2026", font(SANS_B, 24), RED)
y = 150
text_center(y, "ONE DAY  ·  ONE PAGE  ·  THE NEWS THAT MATTERED", font(SANS, 17), GREY)
y = 178
rule(y, w=4)

# ---------- giant headline ----------
y = 196
text_center(y, "GULF WAR WIDENS", fit(SERIF_B, 96, CW, "GULF WAR WIDENS"), INK)
y = 296
text_center(y, "Iran strikes U.S. bases in Kuwait and Bahrain", font(SERIF_B, 33), NAVY)
y = 338
text_center(y, "after American jets hit a missile site on Qeshm Island",
            font(SERIF, 24), INK)
y = 372
rule(y, w=2)

# ---------- big Gulf map illustration ----------
MAP_TOP, MAP_H = 388, 300
MAP_L, MAP_R = 36, 988
d.rectangle([MAP_L, MAP_TOP, MAP_R, MAP_TOP + MAP_H], fill=SEA,
            outline=NAVY, width=2)
# land masses (schematic): Iran top, Arabia bottom-left, Qatar bump
d.polygon([(36, 388), (988, 388), (988, 470), (700, 470), (640, 520),
           (560, 470), (430, 470), (330, 540), (180, 470), (36, 470)],
          fill=LAND, outline=SAND)
d.polygon([(36, 560), (300, 560), (430, 640), (700, 640), (988, 560),
           (988, 688), (36, 688)], fill=LAND, outline=SAND)
# Qatar peninsula bump
d.polygon([(560, 560), (600, 600), (640, 560)], fill=LAND, outline=SAND)
# strait narrows at right
d.polygon([(860, 470), (988, 470), (988, 560), (860, 560)], fill=SEA)

d.text((500, 402), "I R A N", font=font(SANS_B, 20), fill=(120, 100, 70), anchor="ma")
d.text((500, 660), "S A U D I   A R A B I A", font=font(SANS_B, 18),
       fill=(120, 100, 70), anchor="ma")
d.text((760, 520), "PERSIAN GULF", font=font(SERIF, 22), fill=(40, 90, 130),
       anchor="ma")
d.text((930, 600), "STRAIT OF\nHORMUZ", font=font(SANS_B, 15), fill=(40, 90, 130),
       anchor="ma")

def star(cx, cy, r=14, fill=RED):
    pts = []
    import math
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

def marker(cx, cy, label, sub, lx, ly):
    star(cx, cy, 13)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    d.text((lx, ly), label, font=font(SANS_B, 19), fill=INK, anchor="ma")
    d.text((lx, ly + 22), sub, font=font(SANS, 14), fill=GREY, anchor="ma")

# dashed red arcs: Iran -> Kuwait and Iran -> Bahrain
def dashed_arc(x0, y0, x1, y1, lift=40):
    import math
    n = 26
    prev = None
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t - lift * math.sin(math.pi * t)
        if prev is not None and i % 2 == 0:
            d.line([prev, (x, y)], fill=RED, width=3)
        prev = (x, y)

dashed_arc(700, 440, 300, 505, lift=46)
dashed_arc(700, 440, 560, 545, lift=30)
marker(300, 505, "KUWAIT", "Ali Al Salem base hit", 300, 462)
marker(560, 545, "BAHRAIN", "3rd attack this week", 560, 588)
marker(880, 500, "QESHM ISLAND", "U.S. strike, Nov 17", 880, 452)

d.text((36, 693), "★  U.S. base struck  —  schematic map, not to scale",
       font=font(SANS, 13), fill=GREY)

# ---------- three supporting stories ----------
COL_TOP = 716
col_w = 300
gap = 26
cols = [
    ("UKRAINE", "KERCH BRIDGE\nFALLS — AGAIN",
     "Second-day strike drops part of the road span into the strait."),
    ("SUMMIT", "XI MEETS PUTIN\nIN SHENZHEN",
     "Three-way talks with Trump set for Thursday."),
    ("AMERICA", "DEMOCRATS TAKE\nTHE SENATE",
     "Peltola wins Alaska; the party now holds 56 seats."),
]
for i, (kick, head, deck) in enumerate(cols):
    x0 = MX + i * (col_w + gap)
    d.text((x0, COL_TOP), kick, font=font(SANS_B, 17), fill=RED)
    d.line([(x0, COL_TOP + 26), (x0 + col_w, COL_TOP + 26)], fill=RULE, width=2)
    yy = COL_TOP + 38
    for ln in head.split("\n"):
        d.text((x0, yy), ln, font=font(SERIF_B, 27), fill=INK)
        yy += 34
    for ln in wrap(deck, font(SERIF, 17), col_w):
        d.text((x0, yy), ln, font=font(SERIF, 17), fill=INK)
        yy += 23

# ---------- ticker ----------
TICK_TOP = 918
rule(TICK_TOP, w=2)
ticker = ("EBOLA PASSES 11,000 CASES IN CONGO   •   U.S. LOSES MEASLES-FREE STATUS"
          "   •   RUSSIAN PLANE CRASH KILLS 19   •   CYCLONE XAVIER HITS COOK ISLANDS")
text_center(TICK_TOP + 12, ticker, fit(SANS_B, 16, CW, ticker), NAVY)
rule(TICK_TOP + 44, w=2)
text_center(TICK_TOP + 56,
            "All stories reported 18 November 2026  ·  Sources: AP, Reuters, Wall Street Journal",
            font(SANS, 14), GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
