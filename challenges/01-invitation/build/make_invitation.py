#!/usr/bin/env python3
"""Generate the printed dinner invitation (with QR code) handed to players in Task 1.

Usage: make_invitation.py [output.png]

Values below must stay in sync with canon/canon.md.
"""
import sys
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

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

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "player" / "invitation.png"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


def centered(draw, y, text, fnt, fill=INK, spacing=0):
    draw.text((WIDTH // 2, y), text, font=fnt, fill=fill, anchor="ma", align="center", spacing=spacing)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT

    card = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(card)

    draw.rectangle((40, 40, WIDTH - 40, HEIGHT - 40), outline=INK, width=3)
    draw.rectangle((56, 56, WIDTH - 56, HEIGHT - 56), outline=EMBER, width=1)

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

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(QR_URL)
    qr.make(fit=True)
    code = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_y = y + 350
    card.paste(code, ((WIDTH - code.width) // 2, qr_y))

    centered(draw, qr_y + code.height + 20, "Scan for the evening's particulars.", font(FONT_ITALIC, 30))
    centered(draw, HEIGHT - 110, PRINT_DATE, font(FONT_REGULAR, 22), MUTED)

    out.parent.mkdir(parents=True, exist_ok=True)
    card.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
