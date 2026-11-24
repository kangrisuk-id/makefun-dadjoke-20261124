#!/usr/bin/env python3
"""Build-time gallery art for the Dad Joke Showdown entry (not run by the grader)."""
import math
from PIL import Image, ImageDraw, ImageFont

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_dad(draw, cx, cy, s):
    """A flat dad figure: cap, sweater, jeans, one foot through a crack."""
    # legs
    draw.polygon([(cx - 14 * s, cy + 52 * s), (cx - 2 * s, cy + 52 * s), (cx - 4 * s, cy + 96 * s), (cx - 18 * s, cy + 96 * s)], fill=(43, 74, 117))
    draw.polygon([(cx + 3 * s, cy + 52 * s), (cx + 15 * s, cy + 52 * s), (cx + 20 * s, cy + 88 * s), (cx + 7 * s, cy + 90 * s)], fill=(43, 74, 117))
    # shoes
    draw.ellipse([cx - 24 * s, cy + 92 * s, cx - 2 * s, cy + 102 * s], fill=(30, 30, 34))
    draw.ellipse([cx + 4 * s, cy + 86 * s, cx + 27 * s, cy + 96 * s], fill=(30, 30, 34))
    # torso (argyle-ish sweater: plain + diamond)
    draw.rounded_rectangle([cx - 24 * s, cy - 6 * s, cx + 24 * s, cy + 56 * s], radius=10 * s, fill=(178, 58, 44))
    draw.polygon([(cx, cy + 12 * s), (cx + 9 * s, cy + 25 * s), (cx, cy + 38 * s), (cx - 9 * s, cy + 25 * s)], fill=(232, 184, 75))
    # arms: one waving, one on hip
    draw.line([(cx - 22 * s, cy + 2 * s), (cx - 44 * s, cy + 30 * s)], fill=(178, 58, 44), width=int(11 * s))
    draw.line([(cx + 22 * s, cy + 2 * s), (cx + 42 * s, cy - 22 * s)], fill=(178, 58, 44), width=int(11 * s))
    draw.ellipse([cx + 37 * s, cy - 30 * s, cx + 48 * s, cy - 19 * s], fill=(240, 198, 158))
    draw.ellipse([cx - 49 * s, cy + 25 * s, cx - 38 * s, cy + 36 * s], fill=(240, 198, 158))
    # head
    draw.ellipse([cx - 15 * s, cy - 40 * s, cx + 15 * s, cy - 8 * s], fill=(240, 198, 158))
    # moustache + grin
    draw.arc([cx - 8 * s, cy - 22 * s, cx + 8 * s, cy - 12 * s], start=10, end=170, fill=(90, 60, 40), width=max(2, int(2.4 * s)))
    draw.ellipse([cx - 6 * s, cy - 30 * s, cx - 3 * s, cy - 26 * s], fill=(30, 30, 34))
    draw.ellipse([cx + 3 * s, cy - 30 * s, cx + 6 * s, cy - 26 * s], fill=(30, 30, 34))
    # cap
    draw.pieslice([cx - 16 * s, cy - 48 * s, cx + 16 * s, cy - 28 * s], start=180, end=360, fill=(43, 74, 117))
    draw.rectangle([cx + 8 * s, cy - 40 * s, cx + 26 * s, cy - 36 * s], fill=(43, 74, 117))


def lake_scene(w, h):
    img = Image.new("RGB", (w, h), (168, 205, 232))
    d = ImageDraw.Draw(img)
    # sky gradient
    for y in range(int(h * 0.62)):
        t = y / (h * 0.62)
        col = tuple(int(a + (b - a) * t) for a, b in zip((126, 178, 224), (196, 224, 244)))
        d.line([(0, y), (w, y)], fill=col)
    # distant pines
    for i, x in enumerate(range(-20, w, 90)):
        base = int(h * 0.60)
        th = 54 + (i % 3) * 16
        d.polygon([(x, base), (x + 26, base - th), (x + 52, base)], fill=(52, 96, 74))
        d.polygon([(x + 6, base - th // 2), (x + 26, base - th - 12), (x + 46, base - th // 2)], fill=(63, 112, 86))
    # ice
    d.rectangle([0, int(h * 0.60), w, h], fill=(222, 238, 248))
    for i in range(9):
        y = int(h * (0.66 + 0.05 * i))
        d.line([(0, y), (w, y - 14)], fill=(196, 222, 240), width=2)
    # cracks under the dad
    cx, cy = w // 2, int(h * 0.80)
    for ang in range(0, 360, 30):
        r = 66 + (ang % 90)
        x2 = cx + r * math.cos(math.radians(ang))
        y2 = cy + (r // 2) * math.sin(math.radians(ang))
        d.line([(cx, cy), (x2, y2)], fill=(140, 180, 210), width=3)
    d.ellipse([cx - 60, cy - 12, cx + 60, cy + 12], outline=(120, 165, 200), width=3)
    draw_dad(d, cx, cy - 96, 1.15)
    return img, d


def cover():
    img, d = lake_scene(1200, 630)
    d.rounded_rectangle([36, 30, 700, 128], radius=18, fill=(20, 38, 60))
    d.text((60, 52), "DAD JOKE SHOWDOWN", font=font(BOLD, 52), fill=(255, 255, 255))
    d.text((62, 138), "One dad. One frozen lake. One groan, served ice cold.", font=font(REG, 27), fill=(24, 46, 72))
    img.save("/home/hatch/workspace/makefun-dadjoke-20261124/cover.png")


def card(path, title, body, accent):
    img = Image.new("RGB", (1200, 630), (250, 247, 240))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([28, 28, 1172, 602], radius=26, outline=accent, width=6)
    d.text((70, 62), title, font=font(BOLD, 40), fill=accent)
    y = 150
    for line in wrap(d, body, font(BOLD, 47), 1060):
        d.text((70, y), line, font=font(BOLD, 47), fill=(34, 34, 38))
        y += 62
    d.text((70, 540), "make.fun · Dad Joke Showdown · @kangris-uk", font=font(REG, 25), fill=(110, 110, 116))
    img.save(path)


def finalists():
    jokes = [
        ("WINNER", "What do you call a dad who falls through the ice? A popsicle."),
        ("RUNNER-UP", "What do you call a dad telling jokes on a frozen lake? An icebreaker."),
        ("SEMI-FINALIST", "I told my smart fridge a joke. Now it gives me the cold shoulder every time I open it."),
        ("SEMI-FINALIST", "My GPS and I had an argument. In the end, we both had to recalculate our relationship."),
    ]
    img = Image.new("RGB", (1200, 900), (250, 247, 240))
    d = ImageDraw.Draw(img)
    d.text((60, 44), "THE FINAL FOUR — 40 ENTERED, ONE SURVIVED", font=font(BOLD, 38), fill=(178, 58, 44))
    y = 120
    for tag, joke in jokes:
        d.rounded_rectangle([60, y, 1140, y + 168], radius=18, outline=(43, 74, 117), width=3)
        d.text((84, y + 18), tag, font=font(BOLD, 26), fill=(178, 58, 44))
        yy = y + 58
        for line in wrap(d, joke, font(REG, 30), 1030):
            d.text((84, yy), line, font=font(REG, 30), fill=(34, 34, 38))
            yy += 40
        y += 188
    img.save("/home/hatch/workspace/makefun-dadjoke-20261124/shot-finalists.png")


if __name__ == "__main__":
    cover()
    card("/home/hatch/workspace/makefun-dadjoke-20261124/shot-entry.png",
         "THE ENTRY — ALL 61 CHARACTERS OF IT",
         "What do you call a dad who falls through the ice? A popsicle.",
         (178, 58, 44))
    finalists()
    print("images done")
