# Task 7: Commit History (ORGANIZER ONLY)

Flag: `THM{FOLLOW_THE_COMMIT}`

Checkpoint answers: `4fc4f25` (question 1) and `BH-WS-0418` (question 2)

Target solve time: about 7 minutes. Skills: reading a Git history, searching it for a string, reading a diff, opening a password-protected zip. No VM is involved: everything is in the task download, and the player needs only Git.

## The story beat

Task 3 showed that the hub's raw log put the Legal Office tablet `BH-TAB-0417` at the library door at 22:04:11, under Marcus's account. But nobody in the house reads the raw log. They read the hall dashboard, and the dashboard called that device `MARCUS-ADMIN`. This task explains why: two days earlier, someone edited the dashboard's label table. The author was scrubbed, but Adrian's house rule is that every commit must be signed by a registered workstation key, and the key belongs to `BH-WS-0418`, the Legal Office workstation from Task 5.

## How the artifacts are built

The task has two stages, and the player only ever reads one thing at a time.

| File | Stage | What it is |
| :---- | :---- | :---- |
| `blackthorn-dashboard/` | 1 | A Git repository with thirteen commits by Adrian, Marcus, and Theo, plus one by `unknown <>`. Five small files. Contains no flag and never mentions Celeste, `c.ward`, or `BH-WS-0418`. |
| `README.txt` | 1 | The investigators' note: what Git is, five commands, and a plain statement of what the zip password is. |
| `signing-record.zip` | 2 | Password-protected zip holding `signing-record.log`. Password: `4fc4f25`. Legacy ZipCrypto encryption, so Windows Explorer, macOS, `unzip`, and 7-Zip all open it. |
| `organizer/signing-record.log` | none | Plaintext copy of the zip's contents for organizers. Never distribute it. |

`blackthorn-dashboard/` is not kept in this repository, because it holds its own `.git` folder and the outer repository cannot track it. It is listed in `.gitignore`. Run the build script to recreate it: the commit hashes come out the same every time.

The history, newest first:

| Short hash | Date | Author | Message |
| :---- | :---- | :---- | :---- |
| `6e7c666` | 2026-10-30 16:48 | Theo Grant | Raise the wine cellar battery warning to 20 percent |
| `bf7618f` | 2026-10-30 09:15 | Adrian Vale | List the nine doors under the banner for the party |
| `4fc4f25` | 2026-10-29 19:26 | unknown | Tidy label formatting |
| `900ee5c` | 2026-10-16 14:31 | Adrian Vale | Add a banner to the feed for the Halloween dinner |
| `605641f` | 2026-09-02 22:37 | Marcus Vale | Fix feed times showing an hour early in summer |
| `127520c` | 2026-07-11 11:05 | Theo Grant | Warn on the feed when the wine cellar door battery is low |
| `0cdd05a` | 2026-04-22 20:15 | Marcus Vale | Mark denied unlocks so they stand out |
| `71400f4` | 2025-09-18 14:22 | Theo Grant | Add labels for the staff badges |
| `ddded28` | 2025-06-02 10:31 | Adrian Vale | Label the new Legal Office tablet |
| `f6817c8` | 2025-04-03 07:02 | Adrian Vale | Make the dark theme optional. The default stays beige |
| `0d9bc2d` | 2025-04-02 23:51 | Marcus Vale | Add dark theme. Father, it is 2025 |
| `299a326` | 2025-03-14 16:40 | Adrian Vale | Show friendly device labels in the feed instead of device IDs |
| `04bf5e7` | 2025-03-10 09:14 | Adrian Vale | Initial dashboard: a feed of hub events for the hall display |

The relabelling commit sits third from the top, so it is neither the newest commit nor the last thing on the screen.

## Intended solution

1. Download and unzip the task file. Open a terminal in `blackthorn-dashboard/`.
2. Find the commit: `git log -S "MARCUS-ADMIN"` returns exactly one. `git log -p`, or `git log -p -- dashboard/labels.py`, gets there by reading.

   ```
   commit 4fc4f250b5a56ee45b5bb78425938f2d860556e1
   Author: unknown <>
   Date:   Thu Oct 29 19:26:41 2026 -0400

       Tidy label formatting
   ```

3. Look at what it did: `git show 4fc4f25`. The message says formatting. Four lines really are only realigned. The fifth changes a value:

   ```
   -    "BH-TAB-0417": "LEGAL-TABLET",
   +    "BH-TAB-0417": "MARCUS-ADMIN",
   ```

4. Answer question 1 with `4fc4f25`.
5. Open `signing-record.zip` with that short hash as the password: `unzip -P 4fc4f25 signing-record.zip`, or double-click it and type the password.
6. Read `signing-record.log`. Every deployed commit is listed with the key that signed it and the workstation the key lives on. The line for `4fc4f25` says `author="unknown"` and `workstation_ID=BH-WS-0418`. Answer question 2 with `BH-WS-0418`. The flag is on the hub's warning line directly below.

## The sealed record

```
# Blackthorn Hub signing record
# repository: blackthorn-dashboard (the wall display in the front hall)
# commit:     4fc4f250b5a56ee45b5bb78425938f2d860556e1
# sealed:     2026-10-29T19:26:44-04:00 (a commit with no author was deployed)
#
# The hub checks the signature on every commit before it deploys it. A signing key
# lives on one workstation and cannot be copied off it.
#
# Every key the hub knows, and every commit it has deployed (all times local, UTC-04:00).
2025-03-10T09:02:48-04:00 key     REGISTERED signing_key=hub-key-1 workstation_ID=BH-WS-0401 owner=a.vale fingerprint=SHA256:Un7FyfuK9ATGRziBtVHgxYnq4yDeWKJ7U8K28vmCekU
2025-03-10T09:05:30-04:00 key     REGISTERED signing_key=hub-key-2 workstation_ID=BH-WS-0402 owner=m.vale fingerprint=SHA256:5VzICtwEjaJTrTbwc8MF1+k0lTXyhzsTDXyEQEgY1ME
2025-03-10T09:14:25-04:00 deploy  commit=04bf5e7 author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2025-03-14T16:40:08-04:00 deploy  commit=299a326 author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2025-04-02T23:51:41-04:00 deploy  commit=0d9bc2d author="Marcus Vale" signature=GOOD signing_key=hub-key-2 workstation_ID=BH-WS-0402
2025-04-03T07:02:14-04:00 deploy  commit=f6817c8 author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2025-06-02T10:25:13-04:00 key     REGISTERED signing_key=hub-key-3 workstation_ID=BH-WS-0418 owner=c.ward fingerprint=SHA256:WWa9zXsseSgn/FtOPchlRXPwssNTquse+dAF2gMr4mw
2025-06-02T10:31:12-04:00 deploy  commit=ddded28 author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2025-09-18T14:10:02-04:00 key     REGISTERED signing_key=hub-key-4 workstation_ID=BH-WS-0403 owner=t.grant fingerprint=SHA256:cuELgekckCSHa92+Ol9S1SV/y58jwYEXwX18DCWkDXg
2025-09-18T14:22:50-04:00 deploy  commit=71400f4 author="Theo Grant" signature=GOOD signing_key=hub-key-4 workstation_ID=BH-WS-0403
2026-04-22T20:15:33-04:00 deploy  commit=0cdd05a author="Marcus Vale" signature=GOOD signing_key=hub-key-2 workstation_ID=BH-WS-0402
2026-07-11T11:05:59-04:00 deploy  commit=127520c author="Theo Grant" signature=GOOD signing_key=hub-key-4 workstation_ID=BH-WS-0403
2026-09-02T22:37:17-04:00 deploy  commit=605641f author="Marcus Vale" signature=GOOD signing_key=hub-key-2 workstation_ID=BH-WS-0402
2026-10-16T14:31:23-04:00 deploy  commit=900ee5c author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2026-10-29T19:26:44-04:00 deploy  commit=4fc4f25 author="unknown" signature=GOOD signing_key=hub-key-3 workstation_ID=BH-WS-0418
2026-10-29T19:26:44-04:00 hub     WARN commit 4fc4f25 has no author, but it is signed, and hub-key-3 lives on BH-WS-0418, registered to c.ward. House rule, per A. Vale: you can scrub a name, you cannot scrub a signature. THM{FOLLOW_THE_COMMIT}
2026-10-29T19:26:44-04:00 hub     NOTICE this record is now sealed with the short hash of that commit
2026-10-29T19:26:44-04:00 feed    LABEL-CHANGE device_ID=BH-TAB-0417 old=LEGAL-TABLET new=MARCUS-ADMIN
2026-10-30T09:15:06-04:00 deploy  commit=bf7618f author="Adrian Vale" signature=GOOD signing_key=hub-key-1 workstation_ID=BH-WS-0401
2026-10-30T16:48:30-04:00 deploy  commit=6e7c666 author="Theo Grant" signature=GOOD signing_key=hub-key-4 workstation_ID=BH-WS-0403
2026-10-31T22:04:11-04:00 feed    SHOWN door=LIBRARY result=GRANTED device_ID=BH-TAB-0417 shown_as=MARCUS-ADMIN
2026-11-01T01:55:00-04:00 hub     EXPORT repository=blackthorn-dashboard for the investigation
```

## The signatures are real

Every commit carries a genuine SSH signature, and the repository ships with the hub's key list (`.git/allowed_signers`) already wired into `.git/config`. A curious player can run `git log --show-signature` and see:

```
commit 4fc4f250b5a56ee45b5bb78425938f2d860556e1
Good "git" signature for hub-key-3 with ED25519 key SHA256:WWa9zXsseSgn/FtOPchlRXPwssNTquse+dAF2gMr4mw
Author: unknown <>
```

This is a bonus, not a step. It needs `ssh-keygen` on the player's machine (present on Linux, macOS, the AttackBox, and current Windows). It shows only the key's name, `hub-key-3`: which workstation that key lives on is in the sealed record and nowhere else. Adrian's, Marcus's, and Theo's commits show `hub-key-1`, `hub-key-2`, and `hub-key-4`.

## Shortcuts

`grep -r "THM{"` and `git grep` across every commit find nothing, because the flag only exists inside the encrypted zip.

`git log --author=unknown`, or simply reading `git log` and noticing the one commit with no name, finds the commit without looking at the change. That is fine: the missing author is half the point, and question 1 is still answered.

`grep -r MARCUS-ADMIN .` finds the label in `dashboard/labels.py` but not the commit. `git blame dashboard/labels.py` from there gives the short hash, with a `^` or a longer prefix in some Git versions: the first 7 characters are still the password.

Trying all thirteen short hashes as the password works. That still means reading the log.

Players who remember `BH-WS-0418` from Task 5 can guess question 2 before opening the zip. They still need the zip for the flag.

## Common stumbles

- Running Git outside the `blackthorn-dashboard` folder gives "not a git repository". The player must `cd` into it first.
- `git log` opens a pager. Space scrolls, `q` quits. `README.txt` says so.
- Typing the full 40-character hash, or capitals, as the zip password fails. It wants the first 7 characters in lowercase.
- Git may print "detected dubious ownership" if the folder was unzipped by another user (for example as root). The message includes the one-line fix, `git config --global --add safe.directory ...`.
- On Windows, `git status` may list files as modified because of line endings. Nothing in the history is affected, and the task never asks for `git status`.

## What players should take away

- The dashboard's `MARCUS-ADMIN` was not a device Marcus owned. It was a label somebody put on the Legal Office tablet `BH-TAB-0417` on 29 October at 19:26:41, two days before the dinner and thirty-nine minutes after the replacement will was created.
- The commit hid its author and described itself as formatting. The signature it had to carry to be deployed came from `BH-WS-0418`, the Legal Office workstation registered to `c.ward`: the same machine the replacement will was created on.
- An author name in Git is typed in by whoever makes the commit. A signature is not.
- This was planned before Halloween. The frame was built first.

This ties the relabelling to Celeste's workstation and shows premeditation. It does not show who was holding the tablet at 22:04, or how the tablet was able to sign in as `m.vale` (still open from Task 3). Flag 8 puts the four pieces together. Do not tell players this alone proves murder.

## Hints, in order of generosity

1. "Inside the `blackthorn-dashboard` folder, run `git log -S \"MARCUS-ADMIN\"`. It lists the one commit that brought that text in."
2. "The first 7 characters of that commit's hash are the zip password, in lowercase. `git log --oneline` prints them for you. Look for the line that says it is only tidying."
3. "The password is `4fc4f25`. In the record inside, find the line for that commit and read the workstation ID on it, then the line below."

## Publishing to the room

- Run the build script first, because `blackthorn-dashboard/` is not stored in this repository.
- Zip `blackthorn-dashboard/` (including its hidden `.git` folder), `README.txt`, and `signing-record.zip` together into `task7-commit-history.zip` and upload it as the task file. This is done by hand once the task is final: the outer zip is not kept in the repo and has no password. Check the zip afterwards: unzip it somewhere fresh and run `git log --oneline` inside the folder. Some zip tools skip hidden folders.
- Do not include the `organizer` or `build` folders.
- Paste `task.md` into the task body. Set the three answers to `4fc4f25`, `BH-WS-0418`, and the flag above.

## Rebuilding

Run this after changing any commit, any dashboard file, the record, or the flag. The build needs Python, `git`, and `ssh-keygen`. It ignores your own Git settings. It also checks its own output (exactly one commit introduces `MARCUS-ADMIN`, its author is `unknown <>`, every signature verifies, the repository and `README.txt` contain neither the flag nor any mention of Celeste or her workstation).

The commit hashes are reproducible: every date, name, and message is pinned, and Ed25519 signatures are deterministic. Changing anything in the relabelling commit or any commit before it changes its hash, and the build then stops and tells you the new one. Copy it into `EXPECTED_SHORT_HASH` in the script, into this file, and into `canon/canon.md`, because Flag 8 reuses it.

The four private keys inside the build script are props made for this room. They sign nothing else.

```
python3 challenges/07-commit-history/build/make_repo.py
```
