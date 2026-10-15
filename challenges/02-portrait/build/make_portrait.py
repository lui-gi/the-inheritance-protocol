#!/usr/bin/env python3
"""Generate the hall portrait handed to players in the Portrait in the Hall task.

Usage: make_portrait.py [output.jpg]

The result is an ordinary JPEG. Its EXIF UserComment holds Adrian's note in plain English.
Only the flag inside the note is encoded as Base64, and the note itself nudges the reader
toward decoding it.

Values below must stay in sync with canon/canon.md.
"""
import base64
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CATALOGUE_NO = "BH-1959-AV"
DESCRIPTION = f"Adrian Vale, founder. Oil on canvas, digitised for the east hall frame. Catalogue no. {CATALOGUE_NO}"
ARTIST = "Commissioned by the sitter, who also chose the lighting, the chair, and the expression."
SOFTWARE = "Blackthorn Gallery Frame 2.3"
COPYRIGHT = "Blackthorn Security. Do not hang crooked."
DIGITISED = "2024:04:13 11:20:00"
MODIFIED = "2026:10:27 21:15:44"  # Adrian writes the note into the file
UTC_OFFSET = "-04:00"

FLAG = "THM{TRUST_THE_HASH}"

# Stored in the EXIF UserComment as one line of plain English, paragraphs joined by spaces.
# Only {flag} is Base64. The paragraph before it is the nudge toward decoding it.
NOTE = """\
If you are reading this, you looked behind the portrait. Nobody in this family ever has. They walk past me every day and not one of them has checked.

27 October. I spent tonight rereading my own will, and I no longer trust a document just because it has my name on the cover. Anyone can call a file "final". Several people in this house would like to.

So here is the one rule I still believe. Trust the signed hash, not the filename. On the day I signed the real will, I filed its checksum in the estate archive. If two wills ever turn up, that number settles it. Nothing else does, including whoever sounds most certain.

Tomorrow I change the guest list. I want everyone in the room when I say this out loud.

The next thing I write is the part worth stealing, so I have put it in a costume. It is not locked. Its alphabet has sixty-four letters, and any decoder will take it off for you.

{flag}

A.V.
"""

FONT_REGULAR = "/usr/share/fonts/google-noto-vf/NotoSerif[wght].ttf"
FONT_ITALIC = "/usr/share/fonts/google-noto-vf/NotoSerif-Italic[wght].ttf"

WIDTH, HEIGHT = 1200, 1500
WALL = (38, 20, 26)
GILT = (176, 138, 62)
GILT_DARK = (104, 76, 30)
GILT_LIGHT = (222, 190, 112)
CANVAS = (34, 30, 36)
SUIT = (18, 16, 22)
SKIN = (196, 160, 134)
SKIN_SHADE = (150, 116, 98)
HAIR = (188, 186, 184)
SHIRT = (226, 220, 208)
EMBER = (150, 62, 20)
INK = (28, 22, 30)

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "portrait.jpg"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


def paint():
    rng = random.Random(1959)
    img = Image.new("RGB", (WIDTH, HEIGHT), WALL)
    draw = ImageDraw.Draw(img)

    # damask-ish wallpaper
    for row, y in enumerate(range(0, HEIGHT, 90)):
        for x in range(45 if row % 2 else 0, WIDTH, 90):
            draw.regular_polygon((x, y, 16), 4, rotation=45, outline=(52, 28, 36))

    # frame
    frame = (110, 90, WIDTH - 110, HEIGHT - 250)
    for inset, colour in ((0, GILT_DARK), (10, GILT), (34, GILT_LIGHT), (42, GILT), (62, GILT_DARK)):
        draw.rectangle((frame[0] + inset, frame[1] + inset, frame[2] - inset, frame[3] - inset), fill=colour)
    inner = (frame[0] + 72, frame[1] + 72, frame[2] - 72, frame[3] - 72)
    draw.rectangle(inner, fill=CANVAS)

    # sitter, painted on a separate layer so the brushwork can be softened
    layer = Image.new("RGB", (inner[2] - inner[0], inner[3] - inner[1]), CANVAS)
    art = ImageDraw.Draw(layer)
    w, h = layer.size
    cx = w // 2
    for radius in range(520, 0, -8):  # glow behind the sitter
        shade = 34 + (520 - radius) // 14
        art.ellipse((cx - radius, 430 - radius, cx + radius, 430 + radius), fill=(shade + 8, shade, shade + 2))
    art.rectangle((0, h - 150, w, h), fill=(52, 34, 26))  # desk
    art.polygon(((cx - 420, h - 150), (cx - 300, 640), (cx - 110, 560), (cx + 110, 560), (cx + 300, 640), (cx + 420, h - 150)), fill=SUIT)
    art.polygon(((cx - 70, 560), (cx + 70, 560), (cx, 760)), fill=SHIRT)
    art.polygon(((cx - 22, 590), (cx + 22, 590), (cx + 30, 740), (cx, 780), (cx - 30, 740)), fill=EMBER)
    art.rectangle((cx - 52, 480, cx + 52, 590), fill=SKIN_SHADE)  # neck
    art.ellipse((cx - 150, 190, cx + 150, 540), fill=SKIN)  # head
    art.pieslice((cx - 162, 170, cx + 162, 470), 180, 360, fill=HAIR)
    art.ellipse((cx - 150, 262, cx + 150, 400), fill=SKIN)
    art.polygon(((cx - 162, 320), (cx - 138, 300), (cx - 132, 420), (cx - 156, 400)), fill=HAIR)
    art.polygon(((cx + 162, 320), (cx + 138, 300), (cx + 132, 420), (cx + 156, 400)), fill=HAIR)
    for side in (-1, 1):
        ex = cx + side * 62
        art.line((ex - 34, 338 + side * 6, ex + 34, 326 - side * 6), fill=HAIR, width=10)  # one raised eyebrow
        art.ellipse((ex - 20, 356, ex + 20, 380), fill=SHIRT)
        art.ellipse((ex - 8, 358, ex + 12, 378), fill=INK)
    art.line((cx, 380, cx - 14, 446, cx + 10, 450), fill=SKIN_SHADE, width=6)
    art.arc((cx - 60, 440, cx + 70, 500), 20, 150, fill=(112, 60, 54), width=6)  # the smirk
    for _ in range(9000):  # brushwork
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b = layer.getpixel((x, y))
        d = rng.randint(-14, 14)
        length = rng.randint(6, 22)
        art.line((x, y, x + length, y + rng.randint(-4, 4)), fill=(r + d, g + d, b + d), width=3)
    layer = layer.filter(ImageFilter.GaussianBlur(1.6))
    img.paste(layer, (inner[0], inner[1]))

    # brass nameplate
    plate = (WIDTH // 2 - 300, HEIGHT - 200, WIDTH // 2 + 300, HEIGHT - 70)
    draw.rectangle(plate, fill=GILT, outline=GILT_DARK, width=4)
    draw.text((WIDTH // 2, plate[1] + 18), "ADRIAN VALE", font=font(FONT_REGULAR, 46), fill=INK, anchor="ma")
    draw.text((WIDTH // 2, plate[1] + 80), "Founder, Blackthorn Security", font=font(FONT_ITALIC, 26), fill=INK, anchor="ma")
    return img


def comment():
    encoded = base64.b64encode(FLAG.encode("ascii")).decode("ascii")
    paragraphs = NOTE.format(flag=encoded).strip().split("\n\n")
    return " ".join(paragraphs)


def exif_block(img):
    exif = img.getexif()
    exif[0x010E] = DESCRIPTION
    exif[0x013B] = ARTIST
    exif[0x0131] = SOFTWARE
    exif[0x0132] = MODIFIED
    exif[0x8298] = COPYRIGHT
    sub = exif.get_ifd(0x8769)
    sub[0x9003] = DIGITISED
    sub[0x9010] = UTC_OFFSET  # OffsetTime, applies to MODIFIED
    sub[0x9011] = UTC_OFFSET  # OffsetTimeOriginal
    sub[0x9286] = b"ASCII\x00\x00\x00" + comment().encode("ascii")
    return exif


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT

    portrait = paint()
    out.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(out, "JPEG", quality=88, exif=exif_block(portrait))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
