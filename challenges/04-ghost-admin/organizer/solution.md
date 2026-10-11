# Task 4: Ghost Admin (ORGANIZER ONLY)

Flag: `THM{RED_HERRING_ROOT}`

Checkpoint answers: question 1 is `hvac-sync`, question 2 is `2026-10-29`.

Target solve time: about 8 minutes. Skills: reading `/etc/passwd`, recursive `grep`, reading login timestamps, opening a password-protected zip. No VM is involved: the "server" is a folder of files in the task download.

## How the artifact is built

`blackthorn-server/` is a snapshot of the house server `blackthorn-srv`, taken by the investigation at 01:25 on 1 November.

| File | What it is |
| :---- | :---- |
| `README.txt` | Explains the layout, the `passwd` fields, and how to search on Linux and Windows. |
| `etc/passwd` | 25 accounts. `hvac-sync` sits among the service accounts with user ID `0`, the same as `root`. |
| `etc/group` | Scenery. Shows `a.vale` and `m.vale` in the `sudo` group. |
| `var/log/auth.log` | 1,713 lines, 1 May to 31 October 2026. Mentions `hvac-sync` on 30 lines. |
| `home/a.vale/audit/hvac-sync.txt` | Adrian's audit note, dated 30 October. Says what the zip password is. |
| `home/a.vale/audit/findings.zip` | Password-protected zip holding `findings.txt`, which carries the flag. Password: `2026-10-29`. Legacy ZipCrypto, so Windows Explorer, macOS, `unzip`, and 7-Zip all open it. |
| `home/m.vale/TODO.txt` | Marcus's to-do list. Two lines admit to the account. |
| `home/t.grant/staff-rota.txt` | Scenery. |
| Everything else (35 files under `boot`, `etc`, `opt`, `usr`, `var`, `root`, `tmp`, and the home dot-files) | Scenery, so the folder reads like a real Linux server: system settings, the hub's config and service file, backup scripts, and short logs. None of it mentions `hvac-sync` or the flag, so `grep -r hvac-sync .` still returns only the four files in the intended solution. |
| `organizer/findings.txt` | Plaintext copy of the sealed findings. Never distribute it. |

## Intended solution

1. Download and unzip the task file.
2. Read `etc/passwd`. One account other than `root` has user ID `0`:

   ```
   hvac-sync:x:0:0:HVAC Sync Service:/var/lib/hvac-sync:/bin/bash
   ```

   `awk -F: '$3 == 0' etc/passwd` prints it directly, but reading the file works: it is 25 lines. Answer question 1 with `hvac-sync`.
3. Search the snapshot for the name: `grep -r hvac-sync .` The hits fall in four files: `etc/passwd`, `var/log/auth.log`, `home/m.vale/TODO.txt`, and `home/a.vale/audit/hvac-sync.txt`.
4. In `auth.log`, the first hits show who made the account:

   ```
   2026-05-12T23:48:09-04:00 blackthorn-srv sudo:   m.vale : TTY=pts/0 ; PWD=/home/m.vale ; USER=root ; COMMAND=/usr/sbin/useradd -o -u 0 -g 0 -M -d /var/lib/hvac-sync -s /bin/bash -c HVAC Sync Service hvac-sync
   2026-05-12T23:48:09-04:00 blackthorn-srv useradd[2430]: new user: name=hvac-sync, UID=0, GID=0, home=/var/lib/hvac-sync, shell=/bin/bash, from=/dev/pts/0
   ```

5. The remaining hits are nine logins between May and October, all from `10.13.0.22`, the same address Marcus's own account logs in from. The last one:

   ```
   2026-10-29T23:12:40-04:00 blackthorn-srv sshd[17725]: Accepted password for hvac-sync from 10.13.0.22 port 41217 ssh2
   2026-10-29T23:30:53-04:00 blackthorn-srv sshd[17725]: pam_unix(sshd:session): session closed for user hvac-sync
   ```

   `grep hvac-sync var/log/auth.log | tail` shows it. Answer question 2 with `2026-10-29`.
6. Read `home/a.vale/audit/hvac-sync.txt`. Adrian says the password to `findings.zip` is the date the account was last used, written `YYYY-MM-DD`.
7. Open the zip: `unzip -P 2026-10-29 home/a.vale/audit/findings.zip`, or double-click it and type the date. The flag is in `findings.txt`.

## Adrian's note (plaintext, in the snapshot)

```
AUDIT NOTE
30 October 2026
Subject: the account called hvac-sync

This house has no HVAC sync service. I designed the heating myself. It syncs
with nothing, and it resents being asked.

hvac-sync is a second root account wearing a boiler suit. Look at its user ID
in /etc/passwd. My son made it, and auth.log will tell you the night he did.

I have known since June. I left it alone because I wanted to see what he
would do with it. So far he restarts things, and reads logs he was allowed
to read anyway.

I check on it every day. Tonight I wrote down what I think it means and
sealed it in findings.zip, beside this note.

The password is the date hvac-sync was last used, written the way the log
writes it: YYYY-MM-DD.

If you are reading this and I am not available to gloat, do one thing before
you open it. Check that the date is still the last one.

A.V.
```

## The sealed findings

```
FINDINGS
Sealed 30 October 2026

If this opened, you know when hvac-sync was last used. Good. Hold on to that
date, because somebody will try to talk you out of it.

Here is what is true. The account is real. Marcus built it in secret, it can
do anything on this server, and it breaks every rule I ever wrote for this
family. He is guilty of exactly that, and he will be hearing about it.

Here is what is also true. An account does nothing while nobody is using it.
A login leaves a line in the log, and no line means no login. If something
has happened in this house, look at that night before you look at my son.
If hvac-sync is not there, it did not do it.

A secret is not the same thing as a crime. Whoever points you at this
account is either a poor reader of logs or is hoping that you are.

THM{RED_HERRING_ROOT}

A.V.

P.S. Marcus, if it is you reading this: we need to talk. Bring the thermostat.
```

## What the log shows on Halloween

Only Marcus's ordinary account, `m.vale`, and Adrian's. `hvac-sync` does not appear at all on 30 or 31 October.

| When | What |
| :---- | :---- |
| 09:12:40 to 09:40 | `m.vale` over SSH from his workstation. |
| 14:05:16 to 14:19 | `a.vale` over SSH, reading `auth.log`. Adrian's daily check. |
| 17:30:02 to 17:52 | `m.vale` over SSH. |
| 19:54:10 to 20:06:33 | `m.vale` at the server room console (`tty1`). |
| 22:03:31 to 22:15:48 | `m.vale` at the console, reading hub logs at 22:09:39. |
| 22:22:04 to 23:52:40 | `m.vale` at the console three more times, trying to bring the network back. |

The console sessions line up with Marcus's phone opening the server room door in Task 3 (19:53:25, 22:02:47, 22:21:15, 22:47:36, 23:26:09). At 22:04:11, when "his" account opened the library, he was sitting at the server under his own name.

## Shortcuts

`grep -r "THM{" .` finds nothing, because the flag only exists inside the encrypted zip.

Finding `findings.zip` first (for example with `find . -name "*.zip"`) does not help without the date. The note beside it says what the password is, and the date still has to come from the log.

Guessing dates works in principle. A player who reasons "it must be shortly before Halloween" and tries a few has understood the point, so this is not worth blocking.

## What players should take away

- Marcus created a second root account, `hvac-sync`, on 12 May 2026 and hid it among the service accounts. This is real misconduct.
- It was last used on 29 October, two days before the murder. It was not used on Halloween.
- Adrian already knew about it and was watching it.
- On the night itself, Marcus was logged in at the server console under his own name during the minutes that matter.

Flag 3 said an innocent-looking login can be somebody else. Flag 4 says a guilty-looking account can be irrelevant. Do not tell players who the killer is: this task only removes Marcus's secret from the list of evidence.

## Hints, in order of generosity

1. "In `etc/passwd`, look at the third field on each line. Only `root` should have a `0` there. Somebody else does."
2. "Search everything for that account's name: `grep -r hvac-sync .` Read the last line in `auth.log` that mentions it, and read the note in Adrian's folder."
3. "The account was last used on 29 October. The zip in `home/a.vale/audit` opens with `2026-10-29`."

## Publishing to the room

- Zip `blackthorn-server/` (keeping the `blackthorn-server` folder as the archive root) into `task4-server.zip` and upload it as the task file. This is done by hand once the task is final: the outer zip is not kept in the repo and has no password.
- Do not include the `organizer` or `build` folders.
- Paste `task.md` into the task body. Set the three answers to `hvac-sync`, `2026-10-29`, and the flag above.

## Rebuilding

Run this after changing any account, login, note, or the flag. The build needs only the Python standard library and is reproducible: the same script gives byte-identical files. It also checks its own output (the ghost's last log line is on 29 October, nothing mentions it on 30 or 31 October, every ghost login comes from Marcus's address, and no file outside the zip contains the flag). Keep `canon/canon.md` in sync.

```
python3 challenges/04-ghost-admin/build/make_server.py
```
