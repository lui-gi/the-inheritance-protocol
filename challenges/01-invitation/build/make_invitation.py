#!/usr/bin/env python3
"""Generate the printed dinner invitation (with QR code) handed to players in the Invitation task.

Usage: make_invitation.py [output.png]

Values below must stay in sync with canon/canon.md.
"""
import sys
from pathlib import Path

import random

import qrcode
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

QR_URL = "http://portal.blackthorn.thm/rsvp/hallows-eve-1031/"
PRINT_DATE = "Printed 17 October 2026"
GUESTS = ["Evelyn Vale", "Marcus Vale", "Nina Park", "Theo Grant"]

FONT_REGULAR = "/usr/share/fonts/google-noto-vf/NotoSerif[wght].ttf"
FONT_ITALIC = "/usr/share/fonts/google-noto-vf/NotoSerif-Italic[wght].ttf"

WIDTH, HEIGHT = 1200, 1800
PAPER = (240, 232, 214)
INK = (28, 22, 30)
EMBER = (150, 62, 20)
MUTED = (110, 98, 88)

SCAN_BED = (226, 226, 222)
SCAN_MARGIN = 70
SEED = 1031

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "invitation.png"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


def centered(draw, y, text, fnt, fill=INK, spacing=0):
    draw.text((WIDTH // 2, y), text, font=fnt, fill=fill, anchor="ma", align="center", spacing=spacing)


def rule(draw, y, half_width):
    """A thin ember rule with a small diamond in the middle."""
    cx = WIDTH // 2
    draw.line((cx - half_width, y, cx - 14, y), fill=EMBER, width=1)
    draw.line((cx + 14, y, cx + half_width, y), fill=EMBER, width=1)
    draw.polygon([(cx, y - 6), (cx + 6, y), (cx, y + 6), (cx - 6, y)], fill=EMBER)


def corner_ornaments(draw):
    """Small L-shaped flourishes inside the inner border, like a letterpress card."""
    inset, arm = 76, 46
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        x = inset if sx > 0 else WIDTH - inset
        y = inset if sy > 0 else HEIGHT - inset
        draw.line((x, y, x + sx * arm, y), fill=EMBER, width=2)
        draw.line((x, y, x, y + sy * arm), fill=EMBER, width=2)
        draw.ellipse((x + sx * 12 - 4, y + sy * 12 - 4, x + sx * 12 + 4, y + sy * 12 + 4), fill=EMBER)


def age_paper(card, rng):
    """Give the flat card paper grain, uneven ink, and a faint fold and scuff."""
    grain = Image.effect_noise(card.size, 18).convert("RGB")
    card = ImageChops.blend(card, ImageChops.multiply(card, grain), 0.10)

    stains = Image.new("L", card.size, 0)
    sd = ImageDraw.Draw(stains)
    for _ in range(5):
        x, y = rng.randrange(WIDTH), rng.randrange(HEIGHT)
        r = rng.randrange(80, 260)
        sd.ellipse((x - r, y - r, x + r, y + r), fill=rng.randrange(10, 22))
    sd.line((0, HEIGHT // 2 + 3, WIDTH, HEIGHT // 2 - 2), fill=28, width=3)
    stains = stains.filter(ImageFilter.GaussianBlur(40))
    stains.paste(stains.filter(ImageFilter.GaussianBlur(2)))
    tint = Image.new("RGB", card.size, (150, 120, 80))
    card = Image.composite(tint, card, stains)
    return card.filter(ImageFilter.GaussianBlur(0.6))


def scan(card, rng):
    """Lay the card on a scanner bed, slightly crooked, with a soft shadow."""
    w, h = card.size
    bed = Image.new("RGB", (w + 2 * SCAN_MARGIN, h + 2 * SCAN_MARGIN), SCAN_BED)

    shadow = Image.new("L", bed.size, 0)
    ImageDraw.Draw(shadow).rectangle((SCAN_MARGIN + 8, SCAN_MARGIN + 10, SCAN_MARGIN + w + 8, SCAN_MARGIN + h + 10), fill=90)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    bed = Image.composite(Image.new("RGB", bed.size, (120, 120, 116)), bed, shadow)

    tilted = card.convert("RGBA").rotate(-0.8, resample=Image.BICUBIC, expand=True)
    bed.paste(tilted, (SCAN_MARGIN - (tilted.width - w) // 2, SCAN_MARGIN - (tilted.height - h) // 2), tilted)

    noise = Image.effect_noise(bed.size, 6).convert("RGB")
    return ImageChops.blend(bed, ImageChops.multiply(bed, noise), 0.04)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT

    card = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(card)

    draw.rectangle((40, 40, WIDTH - 40, HEIGHT - 40), outline=INK, width=3)
    draw.rectangle((56, 56, WIDTH - 56, HEIGHT - 56), outline=EMBER, width=1)
    corner_ornaments(draw)

    centered(draw, 130, "B L A C K T H O R N   H O U S E", font(FONT_REGULAR, 30), EMBER)
    centered(draw, 220, "All Hallows' Eve Dinner", font(FONT_REGULAR, 78))
    centered(draw, 350, "Adrian Vale requests the pleasure, or at least the attendance,\nof the following at his table:", font(FONT_ITALIC, 34), spacing=14)

    y = 500
    for guest in GUESTS:
        centered(draw, y, guest, font(FONT_REGULAR, 46))
        y += 72

    centered(draw, y + 30, "A table is set for four. No more, no fewer.", font(FONT_ITALIC, 32), MUTED)
    centered(draw, y + 120, "Saturday, 31 October 2026\nArrival at seven o'clock. Dinner at half past.", font(FONT_REGULAR, 34), spacing=14)
    centered(draw, y + 250, "Costumes encouraged. Honesty preferred.", font(FONT_ITALIC, 32), MUTED)
    rule(draw, y + 318, 120)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(QR_URL)
    qr.make(fit=True)
    code = qr.make_image(fill_color=INK, back_color=PAPER).convert("RGB")
    qr_y = y + 350
    card.paste(code, ((WIDTH - code.width) // 2, qr_y))

    centered(draw, qr_y + code.height + 20, "Scan for the evening's particulars.", font(FONT_ITALIC, 30))
    centered(draw, HEIGHT - 150, "Blackthorn House  \u00b7  Kindly reply by 24 October", font(FONT_REGULAR, 24), MUTED)
    centered(draw, HEIGHT - 110, PRINT_DATE, font(FONT_REGULAR, 22), MUTED)

    rng = random.Random(SEED)
    card = scan(age_paper(card, rng), rng)

    out.parent.mkdir(parents=True, exist_ok=True)
    card.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
