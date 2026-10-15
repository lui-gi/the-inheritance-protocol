# The Smart Lock (ORGANIZER ONLY)

Flag: `THM{ACCOUNT_IS_NOT_IDENTITY}`

Checkpoint answer (question 1): `BH-TAB-0417`

Target solve time: about 6 minutes. Skills: searching a log, telling an account apart from a device, opening a password-protected zip. No VM is involved: everything is in the task download.

## How the artifacts are built

The task has two stages, and the player only ever reads one file at a time.

| File | Stage | What it is |
| :---- | :---- | :---- |
| `lock-controller.log` | 1 | 179 lines, running to midnight. The library unlock sits at line 137, with about forty lines of lockdown activity after it. Every unlock attempt on the nine house doors on 31 October, plus the hub's own remarks. Contains no flag and never mentions `c.ward`. |
| `device-record.zip` | 2 | Password-protected zip holding `device-activity.log`. Password: `BH-TAB-0417`. Legacy ZipCrypto encryption, so Windows Explorer, macOS, `unzip`, and 7-Zip all open it. |
| `organizer/device-activity.log` | none | Plaintext copy of the zip's contents for organizers. Never distribute it. |

Devices in the lock log:

| Device | Account | What it is |
| :---- | :---- | :---- |
| `BH-PH-0101` | `a.vale` | Adrian's phone |
| `BH-PH-0102` | `m.vale` | Marcus's phone |
| `BH-PH-0103` | `e.vale` | Evelyn's phone |
| `BH-PH-0104` | `n.park` | Nina's phone |
| `BH-BDG-0201` | `t.grant` | Theo's staff badge |
| `BH-BDG-0207` | `staff.kitchen` | Kitchen badge (background noise) |
| `BH-BDG-0209` | `staff.grounds` | Grounds badge (background noise) |
| `BH-TAB-0417` | appears once, as `m.vale` | Legal Office tablet, registered to Celeste Ward |

## Intended solution

1. Download and unzip the task file.
2. Find the library around the time Adrian was found: `grep LIBRARY lock-controller.log`, or search for `22:0` in an editor. The log carries on to midnight, so the entry is not at the bottom of the file. The last library unlock is:

   ```
   2026-10-31T22:04:11-04:00 lock door=LIBRARY event=UNLOCK result=GRANTED account=m.vale device_ID=BH-TAB-0417
   2026-10-31T22:04:11-04:00 hub  NOTICE unfamiliar device on account m.vale. Device record sealed. It opens with the device ID
   ```

3. Notice the device. `grep m.vale lock-controller.log` shows 23 unlocks on Marcus's account: 22 from his phone `BH-PH-0102`, and this one from `BH-TAB-0417`. Searching for `BH-TAB-0417` shows it appears nowhere else in the file.
4. Answer question 1 with `BH-TAB-0417`.
5. Open `device-record.zip` with that ID as the password: `unzip -P BH-TAB-0417 device-record.zip`, or double-click it and type the password.
6. Read `device-activity.log`. The header says the tablet is assigned to the Legal Office and registered to `c.ward`. The events show it signed in as `c.ward` all evening, switching to `m.vale` at 22:03:52, unlocking the library at 22:04:11, and switching back to `c.ward` at 22:10:06. The flag is on the hub's warning line at 22:03:52.

## The sealed record

```
# Blackthorn Hub device record
# device:           BH-TAB-0417
# type:             tablet
# assigned to:      Legal Office
# registered owner: c.ward (Celeste Ward, family counsel)
# registered:       2025-06-02T10:12:45-04:00
# flagged:          2026-10-31T22:04:11-04:00 (unfamiliar device on account m.vale)
#
# Everything this device did on the house network on 2026-10-31 (all times local, UTC-04:00).
2026-10-31T19:03:20-04:00 net     JOIN ssid=BLACKTHORN-GUEST
2026-10-31T19:03:41-04:00 session SIGN-IN account=c.ward result=OK
2026-10-31T19:26:02-04:00 screen  LOCK
2026-10-31T20:41:17-04:00 screen  UNLOCK account=c.ward
2026-10-31T20:43:50-04:00 screen  LOCK
2026-10-31T21:36:08-04:00 screen  UNLOCK account=c.ward
2026-10-31T21:44:29-04:00 screen  LOCK
2026-10-31T21:58:33-04:00 screen  UNLOCK account=c.ward
2026-10-31T22:03:38-04:00 session SIGN-OUT account=c.ward
2026-10-31T22:03:52-04:00 session SIGN-IN account=m.vale result=OK
2026-10-31T22:03:52-04:00 hub     WARN account switch on this device: c.ward -> m.vale. House rule, per A. Vale: an account is not a person. THM{ACCOUNT_IS_NOT_IDENTITY}
2026-10-31T22:04:11-04:00 lock    UNLOCK-REQUEST door=LIBRARY account=m.vale result=GRANTED
2026-10-31T22:04:11-04:00 hub     NOTICE unfamiliar device on account m.vale. This record is now sealed with the device ID
2026-10-31T22:09:58-04:00 session SIGN-OUT account=m.vale
2026-10-31T22:10:06-04:00 session SIGN-IN account=c.ward result=OK
2026-10-31T22:10:15-04:00 screen  LOCK
2026-10-31T22:19:41-04:00 net     LOST uplink down
```

## Shortcuts

`grep "THM{"` finds nothing in the download, because the flag only exists inside the encrypted zip. Players have to identify the device to get in.

Searching the log for "sealed" or "device ID" lands on the hub notice, one line below the library unlock. That is fine: the notice does not contain the ID, so the player still reads the unlock line above it.

Guessing the password by trying every device ID in the log works too (there are eight). That still means reading the device column, which is the point.

## What players should take away

- Marcus's account opened the library at 22:04:11, thirteen minutes before Adrian was found, but his phone did not. His phone was at the server room door at 22:02:47.
- The device was `BH-TAB-0417`, the Legal Office tablet registered to Celeste Ward. It was signed in as Celeste before and after.
- An account name in a log says which login was used. It does not say who was holding the device.

This puts Celeste's tablet at the library door. It does not explain how she could sign in as Marcus, or why the house dashboard would show the event as his: those belong to Flag 7. Do not tell players the tablet proves murder. It proves the log entry is not what it seems.

## Hints, in order of generosity

1. "Search the log for `LIBRARY` and look at the last time it opened before 22:17. The line names an account and a device."
2. "Compare the device on that line with the device on Marcus's other lines. The odd one out is your zip password, typed exactly as the log shows it."
3. "The password is `BH-TAB-0417`. In the record inside, read the header, then the lines around 22:03."

## Publishing to the room

- Zip `lock-controller.log` and `device-record.zip` together into `task3-smart-lock.zip` and upload it as the task file. This is done by hand once the task is final: the outer zip is not kept in the repo and has no password.
- Do not include the `organizer` or `build` folders.
- Paste `task.md` into the task body. Set the answer to question 1 to `BH-TAB-0417` and the answer to question 2 to the flag above.

## Rebuilding

Run this after changing any event, device ID, or the flag line. The build needs only the Python standard library and is reproducible: the same script gives byte-identical files. It also checks its own output (the tablet appears on exactly one lock line, Marcus's other unlocks all use his phone, and the lock log contains neither `c.ward` nor the flag). Keep `canon/canon.md` in sync.

```
python3 challenges/03-smart-lock/build/make_logs.py
```
