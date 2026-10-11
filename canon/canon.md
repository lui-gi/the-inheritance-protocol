# Canon (ORGANIZER ONLY)

Shared facts that every task must agree with. Never distribute this file to players.
Add to it whenever a task introduces a new name, timestamp, device ID, hash, or key.

## Conventions

- Timezone: America/New_York. Halloween 2026 falls on a Saturday and is still on daylight time, so every timestamp uses the offset `-04:00`.
- Timestamp format in artifacts: ISO 8601 with offset, for example `2026-10-31T22:17:00-04:00`.
- Account names: first initial, dot, surname (`a.vale`, `m.vale`, `e.vale`, `n.park`, `c.ward`, `t.grant`).
- House portal hostname (offline in the story): `portal.blackthorn.thm`. The room has no VM. Players get a nightly portal snapshot as a folder named after the hostname, and serve it locally with the bundled `serve.py` (default `http://localhost:8000/`).

## Timeline

| When | What | Introduced by |
| :---- | :---- | :---- |
| 2026-05-12T23:48:09-04:00 | Marcus creates the hidden root account `hvac-sync` on the house server. | Task 4 |
| 2026-10-16T14:05:32-04:00 | Guest list revision 1 saved by `a.vale`: Evelyn, Marcus, Nina, Theo. Organizer background: not shown to players. | Task 1 |
| 2024-04-13T11:20:00-04:00 | Adrian's portrait digitised for the east hall frame. | Task 2 |
| 2026-10-17 | Invitations printed. The card reads "Printed 17 October 2026". | Task 1 |
| 2026-10-27T21:15:44-04:00 | Adrian writes a note into his hall portrait's metadata (the portrait file's last-modified time). | Task 2 |
| 2026-10-28T23:41:07-04:00 | Guest list revision 2 saved by `a.vale`: Celeste Ward added. Invitations are not reprinted. | Task 1 |
| 2026-10-29T23:12:40-04:00 | `hvac-sync` logs in for the last time (session ends 23:30:53). | Task 4 |
| 2026-10-30T21:40:00-04:00 | Adrian seals his findings about `hvac-sync` in `findings.zip`. | Task 4 |
| 2026-10-31T03:00:00-04:00 | Nightly portal snapshot taken. This is the copy players receive. | Task 1 |
| 2026-10-31T19:00:00-04:00 | Guests arrive, cocktails in the hall. | Task 1 |
| 2026-10-31T19:30:00-04:00 | Dinner is served. | Task 1 |
| 2026-10-31T21:30:00-04:00 | Dessert. Adrian says: "By midnight, none of you will own what you think you own." | Design doc |
| 2026-10-31T19:03:41-04:00 | The Legal Office tablet `BH-TAB-0417` signs in to the house network as `c.ward`. | Task 3 |
| 2026-10-31T21:38:19-04:00 | Theo's badge opens the wine cellar. | Task 3 |
| 2026-10-31T21:51:26-04:00 | Adrian's phone opens the library. | Task 3 |
| 2026-10-31T22:02:47-04:00 | Marcus's phone opens the server room. | Task 3 |
| 2026-10-31T22:03:38-04:00 | The tablet signs out of `c.ward`, then signs in as `m.vale` at 22:03:52. | Task 3 |
| 2026-10-31T22:03:31-04:00 | Marcus logs in at the server room console as `m.vale` (until 22:15:48). | Task 4 |
| 2026-10-31T22:04:11-04:00 | The tablet, signed in as `m.vale`, unlocks the library. The hub flags the unfamiliar device. | Task 3 |
| 2026-10-31T22:09:44-04:00 | Hub warns that the library door was held open and did not relock. | Task 3 |
| 2026-10-31T22:09:58-04:00 | The tablet signs out of `m.vale`, then back in as `c.ward` at 22:10:06. | Task 3 |
| 2026-10-31T22:17:00-04:00 | Adrian Vale is found dead in the library. | Design doc |
| 2026-10-31T22:19:03-04:00 | Lockdown engages and the exterior doors seal. | Task 3 |
| 2026-10-31T22:19:41-04:00 | The house network uplink drops. The hub keeps logging locally until midnight, and the tablet's device record ends here. | Task 3 |
| 2026-10-31T22:21:15-04:00 | Marcus's phone opens the server room again (and at 22:47:36 and 23:26:09). | Task 3 |
| 2026-11-01T00:00:00-04:00 | Celeste's trustee authority was due to be revoked. | Design doc (Flag 8) |
| 2026-11-01T00:42:00-04:00 | Investigators scan the invitation found in the library. | Task 1 |
| 2026-11-01T00:55:00-04:00 | Investigators pull the portrait file from the east hall frame. | Task 2 |
| 2026-11-01T01:10:00-04:00 | Investigators export the hub's lock log and the sealed device record. | Task 3 |
| 2026-11-01T01:25:00-04:00 | Investigators snapshot the house server `blackthorn-srv`. | Task 4 |

## Task 1 facts

- Event page path: `/rsvp/hallows-eve-1031/` (in `task1-portal.zip`: `blackthorn-portal/portal.blackthorn.thm/rsvp/hallows-eve-1031/index.html`, served locally at `http://localhost:8000/rsvp/hallows-eve-1031/`)
- The snapshot holds only the portal front page and the event page. There are no decoy pages and no `guests.json`.
- QR payload: `http://portal.blackthorn.thm/rsvp/hallows-eve-1031/`
- Printed guest list (four): Evelyn Vale, Marcus Vale, Nina Park, Theo Grant.
- Live guest list (five): the four above plus Celeste Ward.
- Why Celeste was added (organizer reasoning): Adrian wanted her in the room when he revoked her authority. Nothing player-facing in Task 1 explains why she was added.
- Flag: `THM{THE_GUEST_LIST_CHANGED}`

## Task 2 facts

- Artifact: `portrait.jpg`, an ordinary JPEG. Adrian's note is stored in the EXIF UserComment as Base64. Nothing is appended to the file and there is no password.
- Location in the story: a digital frame in the east hall.
- Catalogue number: `BH-1959-AV` (Adrian is 67, born 1959). Flavour only.
- The note is written by Adrian on 27 October 2026, the night before he added Celeste to the guest list. It says "Tomorrow I change the guest list."
- The note's rule: "Trust the signed hash, not the filename."
- The note commits Task 5 to this: Adrian filed a checksum of the genuine will in the estate archive on the day he signed it. The signing date is not stated yet.
- The note names no suspect and does not say a counterfeit will already exists.
- Flag: `THM{TRUST_THE_HASH}`

## Task 3 facts

- Artifacts: `lock-controller.log` (stage 1) and `device-record.zip` (stage 2, holding `device-activity.log`). The zip password is `BH-TAB-0417`.
- Devices and their accounts:

| Device | Account | What it is |
| :---- | :---- | :---- |
| `BH-PH-0101` | `a.vale` | Adrian's phone |
| `BH-PH-0102` | `m.vale` | Marcus's phone |
| `BH-PH-0103` | `e.vale` | Evelyn's phone |
| `BH-PH-0104` | `n.park` | Nina's phone |
| `BH-BDG-0201` | `t.grant` | Theo's staff badge |
| `BH-BDG-0207` | `staff.kitchen` | Shared kitchen badge |
| `BH-BDG-0209` | `staff.grounds` | Shared grounds badge |
| `BH-TAB-0417` | `c.ward` | Tablet assigned to the Legal Office, registered to Celeste on 2025-06-02T10:12:45-04:00 |

- Doors on the hub (nine): `FRONT-DOOR`, `SERVICE-ENTRANCE`, `GARAGE`, `GATEHOUSE`, `WINE-CELLAR`, `SERVER-ROOM`, `STUDY`, `LIBRARY`, `CONSERVATORY`.
- Hub software: Blackthorn Hub 4.1.2. The hub records the true device ID on every lock line. Flag 7's relabelling to `MARCUS-ADMIN` happens in the dashboard, not in these raw logs.
- `c.ward` never appears in the lock log: Theo's badge let the guests in at the front door (18:58:40 to 19:06:48), and Celeste opened no door under her own account.
- The tablet appears in the lock log exactly once, at 22:04:11. Every other `m.vale` unlock that day comes from `BH-PH-0102`.
- Before dinner, Nina's phone was denied at the server room twice (19:14:09 and 19:14:31) and Evelyn's phone opened the study (19:22:15). Flavour, outside the murder window.
- All other lock-log entries are generated filler. From 21:30 onward the filler uses only Theo's badge and the shared staff badges: kitchen staff at the service entrance until lockdown, then denied attempts on exterior doors and Theo's badge on interior doors (wine cellar, study, conservatory) until midnight. Later tasks may ignore the filler but must not contradict the entries listed in the timeline.
- Not decided here: how Celeste was able to sign in as `m.vale`, and who found Adrian (the library door was left unlatched at 22:09, so no unlock is logged at 22:17).
- Flag: `THM{ACCOUNT_IS_NOT_IDENTITY}`

## Task 4 facts

- Artifact: `blackthorn-server/`, a file snapshot of the house server. Hostname: `blackthorn-srv`, address `10.13.0.2`, Ubuntu 24.04. It runs the Blackthorn Hub software (service `blackthorn-hub`, version 4.1.2, installed in `/opt/blackthorn-hub`) and the sensor message broker. The hub's lock log and device records (Task 3) were exported separately and are not in this snapshot, and neither is the hub's paired-device database.
- Shell accounts on the server: `a.vale` (UID 1001), `m.vale` (UID 1002), `t.grant` (UID 1003, created openly by Adrian on 2026-05-04T10:02:11-04:00). Evelyn, Nina, and Celeste have no login on this server.
- The ghost: `hvac-sync`, UID 0, described as "HVAC Sync Service", created by `m.vale` with `sudo useradd`. It must never be called `MARCUS-ADMIN`: that label belongs to Flag 7.
- Addresses: Adrian's workstation `10.13.0.10`, Marcus's workstation `10.13.0.22`, Theo's `10.13.0.31`. Every `hvac-sync` login comes from `10.13.0.22`.
- `hvac-sync` logged in nine times: 12 May, 30 May, 21 June, 4 July, 9 August, 2 September, 27 September, 11 October, 29 October. Nothing on 30 or 31 October.
- Adrian found the account in June and watched it. His note in `home/a.vale/audit/hvac-sync.txt` is dated 30 October. `findings.zip` beside it opens with `2026-10-29` (the last-used date).
- Halloween on the server: `m.vale` over SSH at 09:12:40 and 17:30:02, `a.vale` over SSH at 14:05:16, then `m.vale` at the server room console at 19:54:10, 22:03:31, 22:22:04, 22:48:22, and 23:27:15 (last session ends 23:52:40). These follow his phone's server room unlocks in Task 3. After lockdown he is trying to restart the network.
- Marcus therefore has a console session under his own name from 22:03:31 to 22:15:48, covering the 22:04:11 library unlock.
- The snapshot also holds scenery system files (settings, scripts, short logs). The hub config there lists the same nine doors as Task 3 and a 30-second autolock. `var/log/syslog` repeats the 22:19:03 lockdown and 22:19:41 network loss.
- `auth.log` entries before Halloween other than the `hvac-sync` and account-creation lines are generated filler.
- Flag: `THM{RED_HERRING_ROOT}`
