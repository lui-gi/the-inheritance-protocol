#!/usr/bin/env python3
"""Stamp the hall portrait handed to players in the Portrait in the Hall task.

Usage: make_portrait.py [output.jpg]

Reads the hand-made painting in portrait-source.png, keeps only its pixels, and writes
it out as an ordinary JPEG. Its EXIF UserComment holds Adrian's note in plain English.
Only the flag inside the note is encoded as Base64, and the note itself nudges the reader
toward decoding it.

Values below must stay in sync with canon/canon.md.
"""
import base64
import sys
from pathlib import Path

from PIL import Image

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

SOURCE = Path(__file__).resolve().parent / "portrait-source.png"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "portrait.jpg"


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

    with Image.open(SOURCE) as src:
        portrait = Image.new("RGB", src.size)  # fresh image: none of the source's metadata comes along
        portrait.paste(src.convert("RGB"))
    out.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(out, "JPEG", quality=88, exif=exif_block(portrait))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
