#!/usr/bin/env python3
"""Generate the dashboard Git repository, the README, and the sealed zip handed to players in Task 7.

Usage: make_repo.py [output_dir]

Writes four things:
  blackthorn-dashboard/          stage 1, a Git repository with thirteen signed commits
  README.txt                     the investigators' note that sits beside the repository
  signing-record.zip             stage 2, sealed with the short hash of the relabelling commit
  organizer/signing-record.log   plaintext copy of the zip's contents, never distributed

Needs Python, git, and ssh-keygen (git uses it to make the SSH signatures). The commit hashes
are reproducible: every date, name, and message is pinned below, and Ed25519 signatures are
deterministic, so the same script gives the same hashes on any machine. The files under
.git are not byte-identical between machines (zlib versions differ), which does not matter.

blackthorn-dashboard/ holds its own .git folder, so the outer repository cannot track it and
ignores it. Run this script to recreate it before publishing.

The four private keys below are props. They sign nothing outside this fictional repository.

Values below must stay in sync with canon/canon.md.
"""
import base64
import hashlib
import os
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from datetime import datetime
from pathlib import Path

FLAG = "THM{FOLLOW_THE_COMMIT}"

REPO_NAME = "blackthorn-dashboard"
TABLET = "BH-TAB-0417"  # Legal Office tablet, from Task 3
OLD_LABEL = "LEGAL-TABLET"
NEW_LABEL = "MARCUS-ADMIN"
WORKSTATION = "BH-WS-0418"  # Legal Office workstation, from Task 5

# The relabelling commit. The build fails if the hash it produces is not this one, so a
# change to any commit at or before it must be followed by updating this value, the task
# answers, and canon/canon.md.
EXPECTED_SHORT_HASH = "4fc4f25"

ZIP_MEMBER = "signing-record.log"
EXPORTED = datetime(2026, 11, 1, 1, 55, 0)  # investigators export the repository and the record

TASK_DIR = Path(__file__).resolve().parent.parent


def private_key(body):
    return f"-----BEGIN OPENSSH PRIVATE KEY-----\n{body.strip()}\n-----END OPENSSH PRIVATE KEY-----\n"


# name: (key name on the hub, workstation, account, registered, public key, private key)
KEYS = {
    "adrian": ("hub-key-1", "BH-WS-0401", "a.vale", "2025-03-10T09:02:48",
               "AAAAC3NzaC1lZDI1NTE5AAAAIGDjMQdXd+pMCZX4i3uMPhKxh669b0Wz52khULkjajL7", private_key("""
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBg4zEHV3fqTAmV+It7jD4SsYeuvW9Fs+dpIVC5I2oy+wAAAIihqnKhoapy
oQAAAAtzc2gtZWQyNTUxOQAAACBg4zEHV3fqTAmV+It7jD4SsYeuvW9Fs+dpIVC5I2oy+w
AAAEBMuNIvuE4VF9D8v18QjTvfWmw66eNvQsoT1NE3CDwZsWDjMQdXd+pMCZX4i3uMPhKx
h669b0Wz52khULkjajL7AAAAAAECAwQF""")),
    "marcus": ("hub-key-2", "BH-WS-0402", "m.vale", "2025-03-10T09:05:30",
               "AAAAC3NzaC1lZDI1NTE5AAAAIKlcL+wlofN96aqyPSSyAY0BI/csVqFlVkjvjTUym04G", private_key("""
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCpXC/sJaHzfemqsj0ksgGNASP3LFahZVZI7401MptOBgAAAIguxzOKLscz
igAAAAtzc2gtZWQyNTUxOQAAACCpXC/sJaHzfemqsj0ksgGNASP3LFahZVZI7401MptOBg
AAAEAfwPJSu5XeHR+TBl8axPnqRoLO3C5L+CXTp42qs2aniqlcL+wlofN96aqyPSSyAY0B
I/csVqFlVkjvjTUym04GAAAAAAECAwQF""")),
    "legal": ("hub-key-3", WORKSTATION, "c.ward", "2025-06-02T10:25:13",
              "AAAAC3NzaC1lZDI1NTE5AAAAIOkflH+BGuIdtF0rShGba2KlsjzrUlWJr3HXEx1yIaLJ", private_key("""
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDpH5R/gRriHbRdK0oRm2tipbI861JVia9x1xMdciGiyQAAAIhAUiltQFIp
bQAAAAtzc2gtZWQyNTUxOQAAACDpH5R/gRriHbRdK0oRm2tipbI861JVia9x1xMdciGiyQ
AAAEAg4qGWqTEmgJZ42ShCtim2vcPhMXm/L1zzv1VK3KA2EekflH+BGuIdtF0rShGba2Kl
sjzrUlWJr3HXEx1yIaLJAAAAAAECAwQF""")),
    "theo": ("hub-key-4", "BH-WS-0403", "t.grant", "2025-09-18T14:10:02",
             "AAAAC3NzaC1lZDI1NTE5AAAAIP3l0SdMkBEUtJNueIEbm8e9Pf51rQAFRVRrH97xWzNH", private_key("""
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD95dEnTJARFLSTbniBG5vHvT3+da0ABUVUax/e8VszRwAAAIiMOkVSjDpF
UgAAAAtzc2gtZWQyNTUxOQAAACD95dEnTJARFLSTbniBG5vHvT3+da0ABUVUax/e8VszRw
AAAECBVtB36c7Gq+KLoomYcr66mTVBcGHGw5rDyPJoBiRBWv3l0SdMkBEUtJNueIEbm8e9
Pf51rQAFRVRrH97xWzNHAAAAAAECAwQF""")),
}

AUTHORS = {
    "adrian": ("Adrian Vale", "a.vale@blackthorn.thm"),
    "marcus": ("Marcus Vale", "m.vale@blackthorn.thm"),
    "theo": ("Theo Grant", "t.grant@blackthorn.thm"),
    "legal": ("unknown", ""),  # the author was scrubbed. The signature could not be
}

REPO_README = """\
# blackthorn-dashboard

The wall display in the front hall of Blackthorn House. It reads events from the
Blackthorn Hub and shows them as a feed, so that anyone walking past can see which
doors opened, when, and for whom.

The hub's own log records the real device ID on every line. This dashboard does not
show device IDs, because the family complained that they looked like parking tickets.
It shows the friendly labels in `dashboard/labels.py` instead.

The dashboard is a convenience. The hub log is the record. If the two ever disagree,
believe the hub, and then come and find out who touched the labels.

A. Vale
"""

CONTRIBUTING = """\
# Contributing

Three rules. I have kept them short so that nobody can claim to have skimmed.

1. Every commit must be signed with the signing key of a registered house workstation.
   The hub will not deploy an unsigned commit, and it will not deploy a commit signed
   by a key it has never met.
2. A signing key lives on one workstation and cannot be copied off it. I tested this
   personally, with a screwdriver.
3. The author field is whatever you type. The signature is wherever you were sitting.
   I only read one of them.

A. Vale
"""

FEED_V1 = '''\
"""Turn raw hub events into lines for the dashboard feed."""


def render(event):
    return f"{event['time']}  {event['door']:<17}{event['result']:<8}{event['device_ID']}"


def render_feed(events):
    return "\\n".join(render(event) for event in events)
'''

LABELS_V1 = '''\
"""Friendly names for the devices on the hub. The feed shows these instead of device IDs."""

DEVICE_LABELS = {
    "BH-PH-0101": "ADRIAN-PHONE",
    "BH-PH-0102": "MARCUS-PHONE",
    "BH-PH-0103": "EVELYN-PHONE",
    "BH-PH-0104": "NINA-PHONE",
}


def label_for(device_id):
    """Fall back to the raw device ID when a device has no label yet."""
    return DEVICE_LABELS.get(device_id, device_id)
'''

THEME_DARK = """\
/* Dark theme. The hall display is visible from the driveway at night. */
body {
    background: #101014;
    color: #e8e6df;
    font-family: monospace;
}

.denied {
    color: #ff5a4f;
}
"""

THEME_OPTIONAL = """\
/* The default. It was good enough for the house and it is good enough for the feed. */
body {
    background: #f1e9d2;
    color: #2b2620;
    font-family: monospace;
}

.denied {
    color: #a3211a;
}

/* Optional dark theme, for those who insist. Add class="dark" to the body. */
body.dark {
    background: #101014;
    color: #e8e6df;
}

body.dark .denied {
    color: #ff5a4f;
}
"""

FEED, LABELS, THEME = "dashboard/feed.py", "dashboard/labels.py", "dashboard/theme.css"


def swap(old, new):
    """An edit that replaces one exact piece of a file."""
    def edit(text):
        assert text.count(old) == 1, f"expected exactly one {old!r}"
        return text.replace(old, new)
    return edit


def tidy_labels(text):
    """Celeste's commit: line up the label column, and change one label on the way past."""
    text = swap(f'"{TABLET}": "{OLD_LABEL}"', f'"{TABLET}": "{NEW_LABEL}"')(text)
    assert text.count('"BH-PH-') == 4
    return text.replace('": "', '":  "', 4)  # the four phone lines come first


# (when, who, message, {path: new contents, or an edit of the old contents})
COMMITS = [
    ("2025-03-10T09:14:22", "adrian", "Initial dashboard: a feed of hub events for the hall display",
     {"README.md": REPO_README, "CONTRIBUTING.md": CONTRIBUTING, FEED: FEED_V1}),
    ("2025-03-14T16:40:05", "adrian", "Show friendly device labels in the feed instead of device IDs",
     {LABELS: LABELS_V1,
      FEED: lambda text: swap("{event['device_ID']}", "{label_for(event['device_ID'])}")(
          swap('feed."""\n', 'feed."""\nfrom dashboard.labels import label_for\n')(text))}),
    ("2025-04-02T23:51:38", "marcus", "Add dark theme. Father, it is 2025",
     {THEME: THEME_DARK}),
    ("2025-04-03T07:02:11", "adrian", "Make the dark theme optional. The default stays beige",
     {THEME: THEME_OPTIONAL}),
    ("2025-06-02T10:31:09", "adrian", "Label the new Legal Office tablet",
     {LABELS: swap('    "BH-PH-0104": "NINA-PHONE",\n',
                   f'    "BH-PH-0104": "NINA-PHONE",\n    "{TABLET}": "{OLD_LABEL}",\n')}),
    ("2025-09-18T14:22:47", "theo", "Add labels for the staff badges",
     {LABELS: swap(f'    "{TABLET}": "{OLD_LABEL}",\n',
                   f'    "{TABLET}": "{OLD_LABEL}",\n'
                   '    "BH-BDG-0201": "THEO-BADGE",\n'
                   '    "BH-BDG-0207": "KITCHEN-BADGE",\n'
                   '    "BH-BDG-0209": "GROUNDS-BADGE",\n')}),
    ("2026-04-22T20:15:30", "marcus", "Mark denied unlocks so they stand out",
     {FEED: swap("def render(event):\n    return f\"{event['time']}",
                 "def render(event):\n"
                 "    mark = \"!!\" if event[\"result\"] == \"DENIED\" else \"  \"\n"
                 "    return f\"{mark} {event['time']}")}),
    ("2026-07-11T11:05:56", "theo", "Warn on the feed when the wine cellar door battery is low",
     {FEED: swap("\n\ndef render_feed(events):",
                 "\n\ndef battery_warning(door, percent):\n"
                 "    if door == \"WINE-CELLAR\" and percent < BATTERY_WARN_PERCENT:\n"
                 "        return f\"!! {door} door battery at {percent} percent. Somebody tell Theo\"\n"
                 "    return None\n"
                 "\n\ndef render_feed(events):"),
      }),
    ("2026-09-02T22:37:14", "marcus", "Fix feed times showing an hour early in summer",
     {FEED: lambda text: swap("{event['time']}", "{house_time(event['time'])}")(
         swap("\n\ndef render(event):",
              "\n\ndef house_time(utc_hour_minute):\n"
              "    \"\"\"The hub reports UTC. The house does not live in UTC.\"\"\"\n"
              "    hour, minute = utc_hour_minute.split(\":\")\n"
              "    return f\"{(int(hour) + HOUSE_OFFSET_HOURS) % 24:02d}:{minute}\"\n"
              "\n\ndef render(event):")(text))}),
    ("2026-10-16T14:31:20", "adrian", "Add a banner to the feed for the Halloween dinner",
     {FEED: lambda text: swap("return \"\\n\".join(render(event) for event in events)",
                              "return \"\\n\".join([BANNER] + [render(event) for event in events])")(
         swap("\n\n\ndef house_time", "\nBANNER = \"*** BLACKTHORN HOUSE: ALL HALLOWS' EVE DINNER, 31 OCTOBER ***\"\n\n\ndef house_time")(text))}),
    ("2026-10-29T19:26:41", "legal", "Tidy label formatting",
     {LABELS: tidy_labels}),
    ("2026-10-30T09:15:03", "adrian", "List the nine doors under the banner for the party",
     {FEED: lambda text: swap("[BANNER] + [render", "[BANNER, \"Doors: \" + \", \".join(DOORS)] + [render")(
         swap("\n\n\ndef house_time",
              "\nDOORS = [\n"
              "    \"FRONT-DOOR\", \"SERVICE-ENTRANCE\", \"GARAGE\", \"GATEHOUSE\", \"WINE-CELLAR\",\n"
              "    \"SERVER-ROOM\", \"STUDY\", \"LIBRARY\", \"CONSERVATORY\",\n"
              "]\n\n\ndef house_time")(text))}),
    ("2026-10-30T16:48:27", "theo", "Raise the wine cellar battery warning to 20 percent",
     {FEED: swap("BATTERY_WARN_PERCENT = 15", "BATTERY_WARN_PERCENT = 20")}),
]
RELABEL = 10  # index of Celeste's commit in COMMITS

# Constants are introduced by the commits that first use them. These two edits ride along
# with the commits above (kept apart so the commit list stays readable).
EXTRA_EDITS = {
    7: swap('from dashboard.labels import label_for\n',
            'from dashboard.labels import label_for\n\nBATTERY_WARN_PERCENT = 15\n'),
    8: swap('BATTERY_WARN_PERCENT = 15\n',
            'BATTERY_WARN_PERCENT = 15\nHOUSE_OFFSET_HOURS = -4  # was -5, which is only true in winter\n'),
}

PLAYER_README = f"""\
BLACKTHORN DASHBOARD: EVIDENCE COPY
===================================

This download holds two things, copied by the investigation at 01:55 on
1 November 2026:

  {REPO_NAME}/    The code for the wall display in the front hall, as a
                           Git repository. Start here.
  signing-record.zip       A record the hub sealed about one commit in that
                           repository. Locked. Open it second.

Nothing here runs, and nothing here touches the internet. You only need Git.
The AttackBox has it. On your own machine, type "git --version" to check.


WHAT GIT IS, IN FOUR LINES
--------------------------

Git keeps every saved version of a project. Each saved version is a "commit".
A commit records what changed, when, a message, and who the author claims to be.
Every commit has a hash, a long string of letters and digits that names it.
The first 7 characters of a hash are its "short hash", and Git accepts those too.


LOOKING THROUGH THE HISTORY
---------------------------

Open a terminal inside the {REPO_NAME} folder first. The commands are
the same on Linux, macOS, the AttackBox, and Windows.

  git log                         every commit, newest first, with author and date
  git log --oneline               the same, one line each, with short hashes
  git show SHORTHASH              exactly what one commit changed
  git log -p                      every commit together with what it changed
  git log -S "SOME TEXT"          only the commits that added or removed that text

If the history fills the screen, press space for the next page and q to leave.


THE SEALED RECORD
-----------------

One commit taught the display to call a device {NEW_LABEL}.
signing-record.zip opens with the short hash of that commit: the first 7
characters, in lowercase, exactly as "git log --oneline" prints them.

All times are local house time (UTC-04:00).
"""


def fingerprint(public_key):
    digest = hashlib.sha256(base64.b64decode(public_key)).digest()
    return "SHA256:" + base64.b64encode(digest).decode("ascii").rstrip("=")


def git(repo, env, *args):
    result = subprocess.run(["git", *args], cwd=repo, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stdout}{result.stderr}")
    return result.stdout


def build_repo(repo, scratch):
    """Make the thirteen commits and return their full hashes, oldest first."""
    key_files = {}
    for name, key in KEYS.items():
        key_files[name] = scratch / name
        key_files[name].write_text(key[5])
        key_files[name].chmod(0o600)

    # Ignore the builder's own Git settings: only what is written here may shape the commits.
    base_env = {"PATH": os.environ["PATH"], "HOME": str(scratch), "TZ": "UTC",
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    repo.mkdir(parents=True)
    git(repo, base_env, "init", "-q", "-b", "main")

    files, hashes = {}, []
    for index, (when, who, message, changes) in enumerate(COMMITS):
        changes = dict(changes)
        if index in EXTRA_EDITS:
            first, second = EXTRA_EDITS[index], changes[FEED]
            changes[FEED] = lambda text, first=first, second=second: second(first(text))
        for path, change in changes.items():
            files[path] = change(files[path]) if callable(change) else change
            (repo / path).parent.mkdir(parents=True, exist_ok=True)
            (repo / path).write_text(files[path], newline="\n")
        name, email = AUTHORS[who]
        stamp = f"{when}-04:00"
        env = dict(base_env, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_AUTHOR_DATE=stamp,
                   GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email, GIT_COMMITTER_DATE=stamp)
        git(repo, env, "add", "-A")
        git(repo, env, "-c", "gpg.format=ssh", "-c", f"user.signingkey={key_files[who]}",
            "commit", "-q", "-S", "-m", message)
        hashes.append(git(repo, env, "rev-parse", "HEAD").strip())

    # What the player's copy needs: no build leftovers, no surprises from line endings or
    # file modes after unzipping, and the hub's key list so that signatures can be checked.
    dot_git = repo / ".git"
    for leftover in ("logs", "hooks", "COMMIT_EDITMSG"):
        target = dot_git / leftover
        shutil.rmtree(target) if target.is_dir() else target.unlink(missing_ok=True)
    signers = "".join(f'{key[0]} namespaces="git" ssh-ed25519 {key[4]}\n' for key in KEYS.values())
    (dot_git / "allowed_signers").write_text(signers)
    git(repo, base_env, "config", "core.autocrlf", "false")
    git(repo, base_env, "config", "core.filemode", "false")
    git(repo, base_env, "config", "gpg.format", "ssh")
    git(repo, base_env, "config", "gpg.ssh.allowedSignersFile", ".git/allowed_signers")
    return hashes, base_env


def build_record(hashes):
    relabel = hashes[RELABEL]
    short = relabel[:7]
    events = [(key[3], f"key     REGISTERED signing_key={key[0]} workstation_ID={key[1]} owner={key[2]} "
                       f"fingerprint={fingerprint(key[4])}") for key in KEYS.values()]
    for index, (when, who, message, _) in enumerate(COMMITS):
        key = KEYS[who]
        seconds = int(when[-2:]) + 3
        deployed = f"{when[:-2]}{seconds:02d}"
        events.append((deployed, f"deploy  commit={hashes[index][:7]} author=\"{AUTHORS[who][0]}\" signature=GOOD "
                                 f"signing_key={key[0]} workstation_ID={key[1]}"))
        if index == RELABEL:
            events += [
                (deployed, f"hub     WARN commit {short} has no author, but it is signed, and {key[0]} lives on "
                           f"{key[1]}, registered to {key[2]}. House rule, per A. Vale: you can scrub a name, "
                           f"you cannot scrub a signature. {FLAG}"),
                (deployed, "hub     NOTICE this record is now sealed with the short hash of that commit"),
                (deployed, f"feed    LABEL-CHANGE device_ID={TABLET} old={OLD_LABEL} new={NEW_LABEL}"),
            ]
    events += [
        ("2026-10-31T22:04:11", f"feed    SHOWN door=LIBRARY result=GRANTED device_ID={TABLET} shown_as={NEW_LABEL}"),
        ("2026-11-01T01:55:00", f"hub     EXPORT repository={REPO_NAME} for the investigation"),
    ]
    assert all(int(when[-2:]) < 57 for when, _, _, _ in COMMITS)
    events.sort(key=lambda event: event[0])  # stable, so same-second lines keep their order
    header = f"""\
# Blackthorn Hub signing record
# repository: {REPO_NAME} (the wall display in the front hall)
# commit:     {relabel}
# sealed:     2026-10-29T19:26:44-04:00 (a commit with no author was deployed)
#
# The hub checks the signature on every commit before it deploys it. A signing key
# lives on one workstation and cannot be copied off it.
#
# Every key the hub knows, and every commit it has deployed (all times local, UTC-04:00).
"""
    return header + "".join(f"{when}-04:00 {text}\n" for when, text in events)


def check(repo, env, hashes, record):
    relabel = hashes[RELABEL]
    assert relabel[:7] == EXPECTED_SHORT_HASH, (
        f"relabel commit is {relabel[:7]}, expected {EXPECTED_SHORT_HASH}: update the constant, "
        f"the task answers, and canon/canon.md")
    assert len({commit[:7] for commit in hashes}) == len(hashes)
    assert git(repo, env, "log", "--format=%H", "-S", NEW_LABEL).split() == [relabel]
    assert git(repo, env, "log", "--format=%an <%ae>", "-1", relabel).strip() == "unknown <>"
    assert git(repo, env, "status", "--porcelain") == ""
    # Nothing in the repository, in any commit, names Celeste, her workstation, or the flag.
    everything = git(repo, env, "log", "-p", "--format=fuller", "--show-signature")
    everything += (repo / ".git" / "allowed_signers").read_text() + PLAYER_README
    for secret in ("THM{", "c.ward", "Celeste", "Ward", WORKSTATION):
        assert secret not in everything, f"{secret} leaked into the player's stage 1 files"
    assert everything.count('Good "git" signature for') == len(hashes)
    assert everything.count(f'Good "git" signature for {KEYS["legal"][0]} ') == 1
    assert record.count(FLAG) == 1


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
    with tempfile.TemporaryDirectory() as scratch:
        scratch = Path(scratch)
        repo = scratch / REPO_NAME
        hashes, env = build_repo(repo, scratch)
        record = build_record(hashes)
        check(repo, env, hashes, record)
        shutil.rmtree(out / REPO_NAME, ignore_errors=True)
        shutil.copytree(repo, out / REPO_NAME)
    print(f"wrote {out / REPO_NAME}")

    short = hashes[RELABEL][:7]
    (out / "organizer").mkdir(parents=True, exist_ok=True)
    outputs = {
        out / "README.txt": PLAYER_README.encode("ascii"),
        out / "signing-record.zip": build_zip(ZIP_MEMBER, record.encode("ascii"), short),
        out / "organizer" / ZIP_MEMBER: record.encode("ascii"),
    }
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"wrote {path}")
    print(f"relabel commit: {hashes[RELABEL]}")
    print(f"short hash:     {short}  <- zip password")
    print(f"signed by:      {KEYS['legal'][0]} {fingerprint(KEYS['legal'][4])}")


if __name__ == "__main__":
    main()
