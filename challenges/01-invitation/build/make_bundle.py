#!/usr/bin/env python3
"""Package the Task 1 download: the invitation scan plus the portal snapshot.

Usage: make_bundle.py [output.zip]

The snapshot is laid out like a site mirror, under a folder named after the portal
hostname, so the QR code's path maps directly onto a file in the archive.
Entry timestamps are fixed so the archive is reproducible and fits canon/canon.md.
"""
import sys
import zipfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = TASK_DIR / "site"
INVITATION = TASK_DIR / "player" / "invitation.png"
DEFAULT_OUT = TASK_DIR / "player" / "task1-invitation.zip"

PORTAL_HOST = "portal.blackthorn.thm"
SNAPSHOT_TIME = (2026, 10, 31, 3, 0, 0)  # nightly portal snapshot
SCAN_TIME = (2026, 11, 1, 0, 42, 0)  # invitation scanned by investigators


def add(archive, source, name, timestamp):
    info = zipfile.ZipInfo(name, date_time=timestamp)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    with zipfile.ZipFile(out, "w") as archive:
        add(archive, INVITATION, INVITATION.name, SCAN_TIME)
        for path in sorted(p for p in SITE_DIR.rglob("*") if p.is_file()):
            add(archive, path, f"{PORTAL_HOST}/{path.relative_to(SITE_DIR).as_posix()}", SNAPSHOT_TIME)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
