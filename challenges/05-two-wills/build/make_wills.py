#!/usr/bin/env python3
"""Generate the two wills, the archive entry, and the sealed zip handed to players in the Two Wills task.

Usage: make_wills.py [output_dir]

Writes five files:
  Vale_Will_superseded.pdf           the genuine will, signed 1 October (matches the receipt)
  Vale_Will_FINAL_signed.pdf         the replacement, created 29 October (does not match)
  archive-entry.txt                  stage 1, the archive's export with Adrian's filing receipt
  replacement-record.zip             stage 2, sealed with the SHA-256 of the replacement will
  organizer/replacement-record.log   plaintext copy of the zip's contents, never distributed

Standard library only. The build is reproducible: the PDFs and the zip are written here by
hand, so their bytes (and therefore the hashes) do not depend on any local tool. Changing a
single character of either will changes its hash, the receipt, the record, and the zip
password, so rerun this script and update canon/canon.md whenever the wording changes.

Values below must stay in sync with canon/canon.md.
"""
import hashlib
import random
import struct
import sys
import textwrap
import zlib
from datetime import datetime
from pathlib import Path

FLAG = "THM{THE_WILL_WAS_REPLACED}"

GENUINE_NAME = "Vale_Will_superseded.pdf"
FORGED_NAME = "Vale_Will_FINAL_signed.pdf"
ORIGINAL_NAME = "Vale_Will.pdf"  # what the genuine will was called before the replacement
ENTRY = "EA-0042"
WORKSTATION = "BH-WS-0418"  # Legal Office workstation, registered to c.ward. Flag 7 relies on it.

ZIP_MEMBER = "replacement-record.log"
EXPORTED = datetime(2026, 11, 1, 1, 40, 0)  # investigators export the archive entry

TASK_DIR = Path(__file__).resolve().parent.parent

WRAP = 76  # characters per line: Courier 10pt on US Letter with one-inch margins
PAGE_LINES = 49

ARTICLE_4_GENUINE = (
    "Article 4. The Trustee. Celeste Ward serves as Trustee of the Vale Family Trust. "
    "The Trustee keeps the records and files the paperwork. The Trustee has no vote in "
    "Blackthorn Security and no authority over my heirs, under any circumstances."
)
ARTICLE_4_FORGED = (
    "Article 4. The Trustee. Celeste Ward serves as Trustee of the Vale Family Trust. "
    "If any heir is judged unfit to serve, the Trustee shall hold and vote that heir's "
    "shares in Blackthorn Security until the Trustee decides otherwise. The Trustee alone "
    "judges fitness."
)


def will_blocks(article_4, signed_on):
    """The two wills are identical except for Article 4 and the signing date."""
    return [
        ("title", "LAST WILL AND TESTAMENT"),
        ("title", "OF ADRIAN VALE"),
        ("gap", ""),
        ("title", "Blackthorn House"),
        ("gap", ""),
        ("gap", ""),
        ("para", "I, Adrian Vale, of Blackthorn House, being of sound mind and suspicious disposition, "
                 "declare this to be my last will. It revokes every earlier will, including the one I "
                 "wrote on a napkin in 1998."),
        ("para", "Article 1. Blackthorn House. The house and its grounds pass to the Vale Family Trust, "
                 "for the use of my family. The thermostat stays where I set it."),
        ("para", "Article 2. Blackthorn Security. My voting shares in Blackthorn Security pass to my "
                 "children, Evelyn Vale and Marcus Vale, in equal parts. They may vote them however "
                 "they like, provided they do it in the same room."),
        ("para", "Article 3. Bequests. To my niece, Nina Park, I leave my books and the right to say "
                 "she told me so. To Theo Grant, I leave the wine cellar, including its door, whose "
                 "battery is now his problem."),
        ("para", article_4),
        ("para", "Article 5. Integrity. The only authentic copy of this will is the one whose SHA-256 "
                 "checksum matches the receipt I filed in the estate archive on the day I signed it. "
                 "Trust the signed hash, not the filename."),
        ("gap", ""),
        ("para", f"Signed at Blackthorn House on {signed_on}."),
        ("gap", ""),
        ("para", "/s/ Adrian Vale"),
        ("para", "Adrian Vale, Testator"),
        ("gap", ""),
        ("para", "Prepared by Celeste Ward, family counsel, Legal Office, Blackthorn House."),
    ]


def pdf_text(text):
    return "(" + text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


def build_pdf(blocks, created):
    """Write a one-page PDF by hand: Courier text, no compression, fixed dates and ID."""
    lines = []  # (font, text)
    for kind, text in blocks:
        if kind == "title":
            lines.append(("F2", text.center(WRAP).rstrip()))
        elif kind == "gap":
            lines.append(("F1", ""))
        else:
            lines.extend(("F1", line) for line in textwrap.wrap(text, WRAP))
            lines.append(("F1", ""))
    assert len(lines) <= PAGE_LINES, f"will runs to {len(lines)} lines, one page holds {PAGE_LINES}"

    stream = ["BT", "13 TL", "72 710 Td"]
    for font, text in lines:
        stream.append(f"/{font} 10 Tf {pdf_text(text)} Tj T*")
    stream.append("ET")
    content = "\n".join(stream).encode("ascii")

    date = created.strftime("D:%Y%m%d%H%M%S-04'00'")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R "
        b"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
        (f"<< /Title (Last Will and Testament of Adrian Vale) /Author (Adrian Vale) "
         f"/Creator (Blackthorn Legal Office) /Producer (Blackthorn Estate Archive 2.4) "
         f"/CreationDate ({date}) /ModDate ({date}) >>").encode("ascii"),
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1) + b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    file_id = hashlib.md5(bytes(out)).hexdigest().encode("ascii")
    out += (b"trailer\n<< /Size %d /Root 1 0 R /Info 7 0 R /ID [<%s> <%s>] >>\n"
            % (len(objects) + 1, file_id, file_id))
    out += b"startxref\n%d\n%%%%EOF\n" % xref
    return bytes(out)


def build_entry(genuine_hash):
    return f"""\
# Blackthorn Estate Archive 2.4
# entry:    {ENTRY}, Last Will and Testament of Adrian Vale
# exported: 2026-11-01T01:40:00-04:00 for the investigation
#
# This entry is supposed to hold one will. Tonight it holds two.

FILES IN THIS ENTRY
  {FORGED_NAME}
  {GENUINE_NAME}

FILING RECEIPT
  Written once, on the day the will was signed. A receipt cannot be edited afterwards,
  not by counsel, not by family, and not by A. Vale, who tested this personally.

  document=Last Will and Testament of Adrian Vale
  signed=2026-10-01T15:20:00-04:00
  filed=2026-10-01T15:42:10-04:00
  filed_by=a.vale
  algorithm=SHA-256
  sha256={genuine_hash}
  note_from_a.vale="This number is my will. Anything that does not hash to it is somebody else's."

INTEGRITY CHECK
  result=ONE FILE IN THIS ENTRY DOES NOT MATCH THE RECEIPT
  The archive will not say which one. Per A. Vale: "Make them do the arithmetic."

  A replacement record was sealed in replacement-record.zip.
  It opens with the SHA-256 of the file that does NOT match the receipt:
  all 64 characters, in lowercase, exactly as sha256sum prints them.
"""


def build_record(genuine_hash, forged_hash):
    events = [
        ("2026-10-01T13:05:27", f"file    CREATED name={ORIGINAL_NAME} account=c.ward workstation_ID={WORKSTATION}"),
        ("2026-10-01T15:20:00", f"file    SIGNED name={ORIGINAL_NAME} account=a.vale"),
        ("2026-10-01T15:42:10", f"archive FILED name={ORIGINAL_NAME} account=a.vale sha256={genuine_hash}"),
        ("2026-10-01T15:42:10", f"archive MANIFEST signed_by=a.vale signed_sha256={genuine_hash} manifest_signature=VALID"),
        ("2026-10-01T15:42:11", "archive RECEIPT written for a.vale. Receipts cannot be edited"),
        ("2026-10-27T20:52:16", f"archive READ name={ORIGINAL_NAME} account=a.vale manifest_signature=VALID"),
        ("2026-10-29T18:47:33", f"file    CREATED name={FORGED_NAME} account=c.ward workstation_ID={WORKSTATION}"),
        ("2026-10-31T22:26:17", f"archive REPLACE-REQUEST old={ORIGINAL_NAME} new={FORGED_NAME} account=c.ward workstation_ID={WORKSTATION} result=ACCEPTED (counsel may replace files)"),
        ("2026-10-31T22:26:17", f"archive RENAME old={ORIGINAL_NAME} new={GENUINE_NAME}"),
        ("2026-10-31T22:26:17", f"archive FILED name={FORGED_NAME} account=c.ward sha256={forged_hash}"),
        ("2026-10-31T22:26:18", f"archive MANIFEST signed_by=a.vale signed_sha256={genuine_hash} manifest_signature=MISMATCH"),
        ("2026-10-31T22:26:18", f"archive WARN the file now called FINAL was never signed by a.vale. House rule, per A. Vale: trust the signed hash, not the filename. {FLAG}"),
        ("2026-10-31T22:26:18", "archive NOTICE this record is now sealed with the SHA-256 of the file that failed the manifest"),
        ("2026-10-31T22:31:40", f"archive READ name={FORGED_NAME} account=c.ward workstation_ID={WORKSTATION} manifest_signature=MISMATCH"),
        ("2026-11-01T01:40:00", f"archive EXPORT entry={ENTRY} for the investigation"),
    ]
    header = f"""\
# Blackthorn Estate Archive replacement record
# entry:       {ENTRY}, Last Will and Testament of Adrian Vale
# sealed:      2026-10-31T22:26:18-04:00 (a file was replaced, and the new file fails the signed manifest)
# workstation: {WORKSTATION} is the Legal Office workstation
# registered:  c.ward (Celeste Ward, family counsel)
#
# Everything that has happened to this entry (all times local, UTC-04:00).
"""
    return header + "".join(f"{when}-04:00 {text}\n" for when, text in events)


def check(genuine, forged, entry, record):
    genuine_hash, forged_hash = hashlib.sha256(genuine).hexdigest(), hashlib.sha256(forged).hexdigest()
    assert genuine_hash != forged_hash
    assert genuine_hash in entry and forged_hash not in entry
    assert "c.ward" not in entry and WORKSTATION not in entry
    for data in (genuine, forged, entry.encode("ascii")):
        assert b"THM{" not in data
    assert record.count(FLAG) == 1
    assert record.count("manifest_signature=MISMATCH") == 2


def zipcrypto(data, password, crc, rng):
    """Encrypt with the legacy PKWARE stream cipher, including its 12-byte header."""
    table = []  # raw CRC-32 table
    for i in range(256):
        for _ in range(8):
            i = (i >> 1) ^ 0xEDB88320 if i & 1 else i >> 1
        table.append(i)
    keys = [0x12345678, 0x23456789, 0x34567890]

    def update(byte):
        keys[0] = (keys[0] >> 8) ^ table[(keys[0] ^ byte) & 0xFF]
        keys[1] = ((keys[1] + (keys[0] & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        keys[2] = (keys[2] >> 8) ^ table[(keys[2] ^ (keys[1] >> 24)) & 0xFF]

    for byte in password:
        update(byte)
    header = bytes(rng.randrange(256) for _ in range(11)) + bytes([crc >> 24])  # last byte lets tools test the password
    out = bytearray()
    for byte in header + data:
        temp = keys[2] | 2
        out.append(byte ^ (((temp * (temp ^ 1)) >> 8) & 0xFF))
        update(byte)
    return bytes(out)


def build_zip(name, content, password):
    rng = random.Random(1001)
    crc = zlib.crc32(content)
    deflater = zlib.compressobj(9, zlib.DEFLATED, -15)
    body = zipcrypto(deflater.compress(content) + deflater.flush(), password.encode("ascii"), crc, rng)
    dos_time = EXPORTED.hour << 11 | EXPORTED.minute << 5 | EXPORTED.second // 2
    dos_date = (EXPORTED.year - 1980) << 9 | EXPORTED.month << 5 | EXPORTED.day
    encoded = name.encode("ascii")
    # version 2.0, flag bit 0 (encrypted), deflate
    common = struct.pack("<HHHHHIIIHH", 20, 0x0001, 8, dos_time, dos_date, crc, len(body), len(content), len(encoded), 0)
    local = b"PK\x03\x04" + common + encoded
    central = b"PK\x01\x02" + struct.pack("<H", 20) + common + struct.pack("<HHHII", 0, 0, 0, 0x20, 0) + encoded
    end = b"PK\x05\x06" + struct.pack("<HHHHIIH", 0, 0, 1, 1, len(central), len(local) + len(body), 0)
    return local + body + central + end


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else TASK_DIR
    genuine = build_pdf(will_blocks(ARTICLE_4_GENUINE, "1 October 2026"), datetime(2026, 10, 1, 13, 5, 27))
    forged = build_pdf(will_blocks(ARTICLE_4_FORGED, "29 October 2026"), datetime(2026, 10, 29, 18, 47, 33))
    genuine_hash, forged_hash = hashlib.sha256(genuine).hexdigest(), hashlib.sha256(forged).hexdigest()
    entry, record = build_entry(genuine_hash), build_record(genuine_hash, forged_hash)
    check(genuine, forged, entry, record)

    (out / "organizer").mkdir(parents=True, exist_ok=True)
    outputs = {
        out / GENUINE_NAME: genuine,
        out / FORGED_NAME: forged,
        out / "archive-entry.txt": entry.encode("ascii"),
        out / "replacement-record.zip": build_zip(ZIP_MEMBER, record.encode("ascii"), forged_hash),
        out / "organizer" / ZIP_MEMBER: record.encode("ascii"),
    }
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"wrote {path}")
    print(f"genuine sha256 ({GENUINE_NAME}): {genuine_hash}")
    print(f"forged  sha256 ({FORGED_NAME}): {forged_hash}  <- zip password")


if __name__ == "__main__":
    main()
