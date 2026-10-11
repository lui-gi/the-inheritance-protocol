#!/usr/bin/env python3
"""Generate the two logs and the sealed zip handed to players in Task 3.

Usage: make_logs.py [output_dir]

Writes three files:
  lock-controller.log             stage 1, every door in the house on Halloween
  device-record.zip               stage 2, sealed with the ID of the device that opened the library
  organizer/device-activity.log   plaintext copy of the zip's contents, never distributed

Standard library only. The build is reproducible: the filler events come from a seeded
generator, and the zip is written here by hand (legacy ZipCrypto, which Windows Explorer
can open) so that its bytes do not depend on the local zip tool.

Values below must stay in sync with canon/canon.md.
"""
import random
import struct
import sys
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

FLAG = "THM{ACCOUNT_IS_NOT_IDENTITY}"
TZ = timezone(timedelta(hours=-4))
DAY = datetime(2026, 10, 31, tzinfo=TZ)

PHONE_ADRIAN = "BH-PH-0101"
PHONE_MARCUS = "BH-PH-0102"
PHONE_EVELYN = "BH-PH-0103"
PHONE_NINA = "BH-PH-0104"
BADGE_THEO = "BH-BDG-0201"
BADGE_KITCHEN = "BH-BDG-0207"
BADGE_GROUNDS = "BH-BDG-0209"
TABLET = "BH-TAB-0417"  # Legal Office tablet, registered to c.ward. Also the zip password.

ZIP_PASSWORD = TABLET
ZIP_MEMBER = "device-activity.log"
EXPORTED = datetime(2026, 11, 1, 1, 10, 0)  # investigators export the hub records

TASK_DIR = Path(__file__).resolve().parent.parent


def at(clock):
    h, m, s = (int(part) for part in clock.split(":"))
    return DAY + timedelta(hours=h, minutes=m, seconds=s)


def lock(clock, door, account, device, result="GRANTED"):
    return (at(clock), f"lock door={door} event=UNLOCK result={result} account={account} device_ID={device}")


def hub(clock, level, text):
    return (at(clock), f"hub  {level} {text}")


# Every scripted line. The entries from 21:30 onward are canon: later tasks rely on them.
SCRIPTED = [
    hub("00:00:00", "INFO", "log rotated. Blackthorn Hub 4.1.2, 9 doors online"),
    hub("03:00:00", "INFO", "nightly portal snapshot complete"),
    hub("07:15:22", "NOTICE", "door=WINE-CELLAR battery at 18 percent. It has been at 18 percent since August"),
    lock("11:32:08", "LIBRARY", "m.vale", PHONE_MARCUS),
    hub("16:40:03", "INFO", "porch sensor: 14 pumpkins detected, 0 threats"),
    hub("18:55:30", "INFO", "guest mode enabled by t.grant"),
    lock("18:58:40", "FRONT-DOOR", "t.grant", BADGE_THEO),
    lock("19:01:12", "FRONT-DOOR", "t.grant", BADGE_THEO),
    lock("19:03:05", "FRONT-DOOR", "t.grant", BADGE_THEO),
    lock("19:06:48", "FRONT-DOOR", "t.grant", BADGE_THEO),
    lock("19:14:09", "SERVER-ROOM", "n.park", PHONE_NINA, "DENIED"),
    hub("19:14:09", "NOTICE", "n.park is not on the SERVER-ROOM list. Nice try"),
    lock("19:14:31", "SERVER-ROOM", "n.park", PHONE_NINA, "DENIED"),
    hub("19:14:31", "NOTICE", "n.park is still not on the SERVER-ROOM list"),
    lock("19:22:15", "STUDY", "e.vale", PHONE_EVELYN),
    hub("19:30:00", "INFO", "dinner scene active: dining room lights 40 percent, organ music on"),
    lock("21:38:19", "WINE-CELLAR", "t.grant", BADGE_THEO),
    lock("21:51:26", "LIBRARY", "a.vale", PHONE_ADRIAN),
    lock("22:02:47", "SERVER-ROOM", "m.vale", PHONE_MARCUS),
    lock("22:04:11", "LIBRARY", "m.vale", TABLET),
    hub("22:04:11", "NOTICE", "unfamiliar device on account m.vale. Device record sealed. It opens with the device ID"),
    hub("22:09:44", "WARN", "door=LIBRARY held open 30 seconds, autolock skipped"),
    hub("22:19:03", "ALERT", "lockdown engaged. Exterior doors sealed"),
    hub("22:19:41", "ERROR", "network uplink lost. Logging locally until the uplink returns"),
    lock("22:21:15", "SERVER-ROOM", "m.vale", PHONE_MARCUS),
    lock("22:24:50", "SERVICE-ENTRANCE", "staff.kitchen", BADGE_KITCHEN, "DENIED"),
    hub("22:24:50", "NOTICE", "door=SERVICE-ENTRANCE is sealed by lockdown. The hub does not make exceptions for catering"),
    lock("22:47:36", "SERVER-ROOM", "m.vale", PHONE_MARCUS),
    hub("23:00:00", "INFO", "dinner scene ended. Organ music off. Nobody had been listening since 22:17"),
    lock("23:26:09", "SERVER-ROOM", "m.vale", PHONE_MARCUS),
    hub("23:30:00", "NOTICE", "uplink still down, 142 retries. Lockdown still engaged"),
]

# Filler: (account, device, window start, window end, doors, count, result). Nothing here
# uses the tablet or puts m.vale on anything but his phone. From 21:30 onward the filler is
# limited to Theo's badge and the shared staff badges, so the tablet line is not the last
# thing in the file and no other suspect's movements are pinned down by accident.
ROUTINES = [
    ("t.grant", BADGE_THEO, "06:10:00", "18:50:00",
     ["FRONT-DOOR", "SERVICE-ENTRANCE", "GARAGE", "GATEHOUSE", "WINE-CELLAR", "CONSERVATORY", "LIBRARY", "STUDY"], 30, "GRANTED"),
    ("t.grant", BADGE_THEO, "19:35:00", "21:25:00", ["WINE-CELLAR", "SERVICE-ENTRANCE"], 5, "GRANTED"),
    ("staff.kitchen", BADGE_KITCHEN, "09:00:00", "21:25:00", ["SERVICE-ENTRANCE"], 24, "GRANTED"),
    ("staff.grounds", BADGE_GROUNDS, "07:00:00", "16:30:00", ["GATEHOUSE", "GARAGE", "SERVICE-ENTRANCE"], 14, "GRANTED"),
    ("a.vale", PHONE_ADRIAN, "07:30:00", "18:30:00", ["STUDY", "LIBRARY", "CONSERVATORY", "WINE-CELLAR"], 14, "GRANTED"),
    ("m.vale", PHONE_MARCUS, "08:00:00", "18:45:00", ["SERVER-ROOM", "SERVER-ROOM", "GARAGE", "FRONT-DOOR", "CONSERVATORY"], 15, "GRANTED"),
    ("m.vale", PHONE_MARCUS, "19:40:00", "21:25:00", ["SERVER-ROOM"], 2, "GRANTED"),
    ("staff.kitchen", BADGE_KITCHEN, "21:32:00", "22:18:30", ["SERVICE-ENTRANCE"], 7, "GRANTED"),
    ("staff.kitchen", BADGE_KITCHEN, "22:26:00", "23:55:00", ["SERVICE-ENTRANCE", "GARAGE"], 8, "DENIED"),
    ("staff.grounds", BADGE_GROUNDS, "22:20:00", "23:50:00", ["GATEHOUSE", "GARAGE"], 5, "DENIED"),
    ("t.grant", BADGE_THEO, "22:22:00", "23:58:00", ["WINE-CELLAR", "STUDY", "CONSERVATORY"], 12, "GRANTED"),
    ("t.grant", BADGE_THEO, "22:22:00", "23:58:00", ["FRONT-DOOR", "GATEHOUSE"], 4, "DENIED"),
]

LOCK_HEADER = """\
# Blackthorn Hub lock controller log
# day: 2026-10-31 (all times local, UTC-04:00)
# exported: 2026-11-01T01:10:00-04:00 for the investigation
#
# One line per event. "lock" lines are doors, "hub" lines are the hub talking to itself.
# Doors relock on their own when they close, so only unlock attempts are recorded.
#   account   = who the hub believes is asking
#   device_ID = the phone, badge, or tablet that actually asked
"""

DEVICE_HEADER = f"""\
# Blackthorn Hub device record
# device:           {TABLET}
# type:             tablet
# assigned to:      Legal Office
# registered owner: c.ward (Celeste Ward, family counsel)
# registered:       2025-06-02T10:12:45-04:00
# flagged:          2026-10-31T22:04:11-04:00 (unfamiliar device on account m.vale)
#
# Everything this device did on the house network on 2026-10-31 (all times local, UTC-04:00).
"""

DEVICE_EVENTS = [
    ("19:03:20", "net     JOIN ssid=BLACKTHORN-GUEST"),
    ("19:03:41", "session SIGN-IN account=c.ward result=OK"),
    ("19:26:02", "screen  LOCK"),
    ("20:41:17", "screen  UNLOCK account=c.ward"),
    ("20:43:50", "screen  LOCK"),
    ("21:36:08", "screen  UNLOCK account=c.ward"),
    ("21:44:29", "screen  LOCK"),
    ("21:58:33", "screen  UNLOCK account=c.ward"),
    ("22:03:38", "session SIGN-OUT account=c.ward"),
    ("22:03:52", "session SIGN-IN account=m.vale result=OK"),
    ("22:03:52", f"hub     WARN account switch on this device: c.ward -> m.vale. House rule, per A. Vale: an account is not a person. {FLAG}"),
    ("22:04:11", "lock    UNLOCK-REQUEST door=LIBRARY account=m.vale result=GRANTED"),
    ("22:04:11", "hub     NOTICE unfamiliar device on account m.vale. This record is now sealed with the device ID"),
    ("22:09:58", "session SIGN-OUT account=m.vale"),
    ("22:10:06", "session SIGN-IN account=c.ward result=OK"),
    ("22:10:15", "screen  LOCK"),
    ("22:19:41", "net     LOST uplink down"),
]


def stamp(when):
    return when.isoformat(timespec="seconds")


def build_lock_log():
    rng = random.Random(1031)
    events = list(SCRIPTED)
    taken = {when for when, _ in events}
    for account, device, start, end, doors, count, result in ROUTINES:
        first, span = at(start), int((at(end) - at(start)).total_seconds())
        for _ in range(count):
            when = first + timedelta(seconds=rng.randrange(span))
            while when in taken:
                when += timedelta(seconds=1)
            taken.add(when)
            events.append((when, f"lock door={rng.choice(doors)} event=UNLOCK result={result} account={account} device_ID={device}"))
    events.sort(key=lambda event: event[0])  # stable, so scripted pairs keep their order
    return LOCK_HEADER + "".join(f"{stamp(when)} {text}\n" for when, text in events)


def build_device_log():
    return DEVICE_HEADER + "".join(f"{stamp(at(clock))} {text}\n" for clock, text in DEVICE_EVENTS)


def check(lock_log, device_log):
    lock_lines = [line for line in lock_log.splitlines() if " lock " in line]
    tablet_lines = [line for line in lock_lines if TABLET in line]
    assert len(tablet_lines) == 1 and "door=LIBRARY" in tablet_lines[0] and "account=m.vale" in tablet_lines[0]
    assert TABLET not in "".join(line for line in lock_log.splitlines() if " hub " in line)
    marcus = [line for line in lock_lines if "account=m.vale" in line]
    assert sum(PHONE_MARCUS in line for line in marcus) == len(marcus) - 1
    assert "c.ward" not in lock_log and "THM{" not in lock_log
    assert device_log.count(FLAG) == 1


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
    rng = random.Random(417)
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
    lock_log, device_log = build_lock_log(), build_device_log()
    check(lock_log, device_log)

    (out / "organizer").mkdir(parents=True, exist_ok=True)
    outputs = {
        out / "lock-controller.log": lock_log.encode("ascii"),
        out / "device-record.zip": build_zip(ZIP_MEMBER, device_log.encode("ascii"), ZIP_PASSWORD),
        out / "organizer" / ZIP_MEMBER: device_log.encode("ascii"),
    }
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
