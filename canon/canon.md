# Canon (ORGANIZER ONLY)

Shared facts that every task must agree with. Never distribute this file to players.
Add to it whenever a task introduces a new name, timestamp, device ID, hash, or key.

## Conventions

- Timezone: America/New_York. Halloween 2026 falls on a Saturday and is still on daylight time, so every timestamp uses the offset `-04:00`.
- Timestamp format in artifacts: ISO 8601 with offset, for example `2026-10-31T22:17:00-04:00`.
- Account names: first initial, dot, surname (`a.vale`, `m.vale`, `e.vale`, `n.park`, `c.ward`, `t.grant`).
- House portal hostname (offline in the story): `portal.blackthorn.thm`. The room has no VM. The investigators put the nightly portal snapshot back online at `https://blackthorn-portal.vercel.app/`, which the invitation's QR code points to directly; the source is the folder named after the hostname, with a local `serve.py` as a fallback.

## Timeline

| When | What | Introduced by |
| :---- | :---- | :---- |
| 2026-05-12T23:48:09-04:00 | Marcus creates the hidden root account `hvac-sync` on the house server. | Ghost Admin |
| 2026-10-01T13:05:27-04:00 | Celeste drafts the genuine will, `Vale_Will.pdf`, on the Legal Office workstation `BH-WS-0418`. | The Two Wills |
| 2026-10-01T15:20:00-04:00 | Adrian signs the genuine will. | The Two Wills |
| 2026-10-01T15:42:10-04:00 | Adrian files the will in the estate archive (entry `EA-0042`). The archive signs a manifest with its SHA-256 and writes his receipt. | The Two Wills |
| 2026-10-16T14:05:32-04:00 | Guest list revision 1 saved by `a.vale`: Evelyn, Marcus, Nina, Theo. Organizer background: not shown to players. | The Invitation |
| 2024-04-13T11:20:00-04:00 | Adrian's portrait digitised for the east hall frame. | Portrait in the Hall |
| 2026-10-17 | Invitations printed. The card reads "Printed 17 October 2026" and asks guests to reply by 24 October. | The Invitation |
| 2026-10-24 | Nina copies the unreleased Project Lantern lock firmware to a personal drive. Time of day not decided. | Counsel Portal |
| 2026-10-26 | Counsel opens the Legal Office's sealed recovery envelope for the `m.vale` account. The estate archive tells Adrian. Time of day not decided. | The Last Testament |
| 2026-10-27T20:52:16-04:00 | Adrian rereads his will in the archive. It still verifies. | The Two Wills |
| 2026-10-27T21:15:44-04:00 | Adrian writes a note into his hall portrait's metadata (the portrait file's last-modified time). | Portrait in the Hall |
| 2026-10-28T23:41:07-04:00 | Guest list revision 2 saved by `a.vale`: Celeste Ward added. Invitations are not reprinted. | The Invitation |
| 2026-10-29T18:47:33-04:00 | Celeste creates the replacement will, `Vale_Will_FINAL_signed.pdf`, on `BH-WS-0418`. It claims to be signed that day. | The Two Wills |
| 2026-10-29T19:26:41-04:00 | Commit `4fc4f25` ("Tidy label formatting", author `unknown <>`) relabels `BH-TAB-0417` from `LEGAL-TABLET` to `MARCUS-ADMIN` in the dashboard. Signed by the key on `BH-WS-0418`. The hub deploys it at 19:26:44 and seals a signing record. | Commit History |
| 2026-10-29T23:12:40-04:00 | `hvac-sync` logs in for the last time (session ends 23:30:53). | Ghost Admin |
| 2026-10-30T21:40:00-04:00 | Adrian seals his findings about `hvac-sync` in `findings.zip`. | Ghost Admin |
| 2026-10-30T22:10:00-04:00 | Adrian records his message for the Trustee (archive entry `EA-0043`), set for release at midnight on 1 November. | The Last Testament |
| 2026-10-31T03:00:00-04:00 | Nightly portal snapshot taken. This is the copy the investigators put back online. | The Invitation |
| 2026-10-31T19:00:00-04:00 | Guests arrive, cocktails in the hall. | The Invitation |
| 2026-10-31T19:30:00-04:00 | Dinner is served. | The Invitation |
| 2026-10-31T21:30:00-04:00 | Dessert. Adrian says: "By midnight, none of you will own what you think you own." | Design doc |
| 2026-10-31T19:03:41-04:00 | The Legal Office tablet `BH-TAB-0417` signs in to the house network as `c.ward`. | The Smart Lock |
| 2026-10-31T19:24:00-04:00 | Evelyn, in the study, wires 4.2 million from the company reserve. | Counsel Portal |
| 2026-10-31T21:35:00-04:00 | Theo switches off camera 07 (cellar stairs) until 21:50. | Counsel Portal |
| 2026-10-31T21:38:19-04:00 | Theo's badge opens the wine cellar. | The Smart Lock |
| 2026-10-31T21:51:26-04:00 | Adrian's phone opens the library. | The Smart Lock |
| 2026-10-31T22:02:47-04:00 | Marcus's phone opens the server room. | The Smart Lock |
| 2026-10-31T22:03:38-04:00 | The tablet signs out of `c.ward`, then signs in as `m.vale` at 22:03:52. | The Smart Lock |
| 2026-10-31T22:03:31-04:00 | Marcus logs in at the server room console as `m.vale` (until 22:15:48). | Ghost Admin |
| 2026-10-31T22:04:11-04:00 | The tablet, signed in as `m.vale`, unlocks the library. The hub flags the unfamiliar device. | The Smart Lock |
| 2026-10-31T22:04:11-04:00 | The hall dashboard shows the library unlock as `MARCUS-ADMIN`. Evelyn, Nina, and Theo are in the hall and see it. | The Commit History task, the Counsel Portal task |
| 2026-10-31T22:09:44-04:00 | Hub warns that the library door was held open and did not relock. | The Smart Lock |
| 2026-10-31T22:09:58-04:00 | The tablet signs out of `m.vale`, then back in as `c.ward` at 22:10:06. | The Smart Lock |
| 2026-10-31T22:17:00-04:00 | Adrian Vale is found dead in the library. | Design doc |
| 2026-10-31T22:19:03-04:00 | Lockdown engages and the exterior doors seal. | The Smart Lock |
| 2026-10-31T22:19:41-04:00 | The house network uplink drops. The hub keeps logging locally until midnight, and the tablet's device record ends here. | The Smart Lock |
| 2026-10-31T22:21:15-04:00 | Marcus's phone opens the server room again (and at 22:47:36 and 23:26:09). | The Smart Lock |
| 2026-10-31T22:26:17-04:00 | `c.ward`, on `BH-WS-0418`, replaces the will in the archive. The genuine file is renamed `Vale_Will_superseded.pdf`, the manifest check fails at 22:26:18, and the archive seals a replacement record. | The Two Wills |
| 2026-10-31T22:31:40-04:00 | `c.ward` reads the replacement will in the archive from `BH-WS-0418`. | The Two Wills |
| 2026-10-31T23:40:00-04:00 | Celeste, as family counsel, takes the five first statements and files them in the Legal Office case portal (23:40 to 23:56, hers at 23:52). | Counsel Portal |
| 2026-11-01T00:00:00-04:00 | Adrian was due to sign the papers revoking Celeste's trustee authority, in front of the family, and `EA-0043` was due to be released to the Trustee. The papers stayed unsigned and the message was never released. | Design doc, the Last Testament task |
| 2026-11-01T00:11:00-04:00 | Celeste writes four sealed counsel's notes on the others (00:11 to 00:14). | Counsel Portal |
| 2026-11-01T00:33:00-04:00 | Celeste replaces her own statement. The portal seals a revision record holding both versions. | Counsel Portal |
| 2026-11-01T00:42:00-04:00 | Investigators scan the invitation found in the library. | The Invitation |
| 2026-11-01T00:55:00-04:00 | Investigators pull the portrait file from the east hall frame. | Portrait in the Hall |
| 2026-11-01T01:10:00-04:00 | Investigators export the hub's lock log and the sealed device record. | The Smart Lock |
| 2026-11-01T01:25:00-04:00 | Investigators snapshot the house server `blackthorn-srv`. | Ghost Admin |
| 2026-11-01T01:40:00-04:00 | Investigators export estate archive entry `EA-0042`. | The Two Wills |
| 2026-11-01T01:55:00-04:00 | Investigators export the dashboard repository and the hub's signing record. | Commit History |

## The Invitation facts

- Event page path: `/rsvp/hallows-eve-1031/` (source `blackthorn-portal/portal.blackthorn.thm/rsvp/hallows-eve-1031/index.html`, hosted at `https://blackthorn-portal.vercel.app/rsvp/hallows-eve-1031/`)
- The snapshot holds only the portal front page and the event page. There are no decoy pages and no `guests.json`.
- QR payload: `https://blackthorn-portal.vercel.app/rsvp/hallows-eve-1031/`
- Printed guest list (four): Evelyn Vale, Marcus Vale, Nina Park, Theo Grant.
- Printed reply date: "Kindly reply by 24 October" (card footer, above the print date).
- Live guest list (five): the four above plus Celeste Ward.
- Why Celeste was added (organizer reasoning): Adrian wanted her in the room when he signed the papers revoking her authority. Nothing player-facing in the Invitation task explains why she was added.
- Flag: `THM{THE_GUEST_LIST_CHANGED}`

## Portrait in the Hall facts

- Artifact: `portrait.jpg`, an ordinary JPEG. Adrian's note is stored in the EXIF UserComment in plain English. Only the flag inside the note is Base64, and the sentence before it nudges the reader to decode it. Nothing is appended to the file and there is no password.
- Location in the story: a digital frame in the east hall.
- Catalogue number: `BH-1959-AV` (Adrian is 67, born 1959). Flavour only.
- The note is written by Adrian on 27 October 2026, the night before he added Celeste to the guest list. It says "Tomorrow I change the guest list."
- The note's rule: "Trust the signed hash, not the filename."
- The note commits the Two Wills task to this: Adrian filed a checksum of the genuine will in the estate archive on the day he signed it. The Two Wills task sets the signing date to 1 October 2026.
- The note names no suspect and does not say a counterfeit will already exists.
- Flag: `THM{TRUST_THE_HASH}`

## The Smart Lock facts

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
- How Celeste was able to sign in as `m.vale` is answered in the Last Testament task (the recovery envelope). Not decided anywhere: who found Adrian (the library door was left unlatched at 22:09, so no unlock is logged at 22:17).
- Flag: `THM{ACCOUNT_IS_NOT_IDENTITY}`

## Ghost Admin facts

- Artifact: `blackthorn-server/`, a file snapshot of the house server. Hostname: `blackthorn-srv`, address `10.13.0.2`, Ubuntu 24.04. It runs the Blackthorn Hub software (service `blackthorn-hub`, version 4.1.2, installed in `/opt/blackthorn-hub`) and the sensor message broker. The hub's lock log and device records (the Smart Lock task) were exported separately and are not in this snapshot, and neither is the hub's paired-device database.
- Shell accounts on the server: `a.vale` (UID 1001), `m.vale` (UID 1002), `t.grant` (UID 1003, created openly by Adrian on 2026-05-04T10:02:11-04:00). Evelyn, Nina, and Celeste have no login on this server.
- The ghost: `hvac-sync`, UID 0, described as "HVAC Sync Service", created by `m.vale` with `sudo useradd`. It must never be called `MARCUS-ADMIN`: that label belongs to Flag 7.
- Addresses: Adrian's workstation `10.13.0.10`, Marcus's workstation `10.13.0.22`, Theo's `10.13.0.31`. Every `hvac-sync` login comes from `10.13.0.22`.
- `hvac-sync` logged in nine times: 12 May, 30 May, 21 June, 4 July, 9 August, 2 September, 27 September, 11 October, 29 October. Nothing on 30 or 31 October.
- Adrian found the account in June and watched it. His note in `home/a.vale/audit/hvac-sync.txt` is dated 30 October. `findings.zip` beside it opens with `2026-10-29` (the last-used date).
- Halloween on the server: `m.vale` over SSH at 09:12:40 and 17:30:02, `a.vale` over SSH at 14:05:16, then `m.vale` at the server room console at 19:54:10, 22:03:31, 22:22:04, 22:48:22, and 23:27:15 (last session ends 23:52:40). These follow his phone's server room unlocks in the Smart Lock task. After lockdown he is trying to restart the network.
- Marcus therefore has a console session under his own name from 22:03:31 to 22:15:48, covering the 22:04:11 library unlock.
- The snapshot also holds scenery system files (settings, scripts, short logs). The hub config there lists the same nine doors as the Smart Lock task and a 30-second autolock. `var/log/syslog` repeats the 22:19:03 lockdown and 22:19:41 network loss.
- `auth.log` entries before Halloween other than the `hvac-sync` and account-creation lines are generated filler.
- Flag: `THM{RED_HERRING_ROOT}`

## The Two Wills facts

- Artifacts: `Vale_Will_superseded.pdf` (genuine), `Vale_Will_FINAL_signed.pdf` (replacement), `archive-entry.txt` (stage 1, with Adrian's receipt), and `replacement-record.zip` (stage 2, holding `replacement-record.log`). The zip password is the replacement will's SHA-256, all 64 characters in lowercase.
- Hashes (SHA-256). Flag 8 reuses these, so they must be updated here whenever the wills are rebuilt with different wording:

| File | SHA-256 |
| :---- | :---- |
| `Vale_Will_superseded.pdf` (genuine) | `93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914` |
| `Vale_Will_FINAL_signed.pdf` (replacement) | `18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6` |

- The estate archive: "Blackthorn Estate Archive 2.4", the house's document vault. It is not on `blackthorn-srv` and is not in the Ghost Admin task snapshot. It is reachable on the house's local network, which kept working after the uplink dropped at 22:19:41. Adrian's will is entry `EA-0042`.
- Archive rules: family counsel may replace a file in an entry. A filing receipt can never be edited. Each entry has a manifest signed by the person who filed it, listing the file's SHA-256, and every read or replacement is checked against it.
- The genuine will was called `Vale_Will.pdf` until the replacement. The archive renamed it to `Vale_Will_superseded.pdf`.
- New device: `BH-WS-0418`, the Legal Office workstation, registered to `c.ward`. The Legal Office is a room in Blackthorn House with no smart lock (it is not one of the nine hub doors). Flag 7's signing key must map to this workstation. Its network address is not decided yet.
- Celeste drafted both wills on `BH-WS-0418` as family counsel, so the workstation alone does not distinguish them. The genuine one was signed by Adrian on 1 October. The replacement was created on 29 October (the day after Adrian added her to the guest list) and never signed by him.
- The wills are identical except for Article 4 and the signing date. Genuine Article 4: the Trustee keeps records, has no vote in Blackthorn Security, and has no authority over the heirs. Replacement Article 4: if any heir is judged unfit, the Trustee holds and votes that heir's shares until she decides otherwise, and she alone judges fitness.
- Other terms, the same in both wills: the house goes to the Vale Family Trust, the voting shares go to Evelyn and Marcus in equal parts, Nina gets Adrian's books, Theo gets the wine cellar. Celeste Ward is named as Trustee and as the counsel who prepared the document.
- The genuine will does not mention revoking Celeste as Trustee. That is Adrian's midnight plan and belongs to Flag 8.
- The replacement is filed under Celeste's own account. Her cover story is that Adrian signed an updated will on 29 October and she filed it as counsel. The failed manifest is what disproves it.
- Not decided here: where Celeste was between 22:10 and 22:26 beyond the tablet record. How she signed in as `m.vale` is answered in the Last Testament task.
- Flag: `THM{THE_WILL_WAS_REPLACED}`

## Counsel Portal facts

- Artifact: `counsel-portal/`, a WSGI app hosted at `https://blackthorn-counsel-portal.vercel.app/` (local `serve.py` as a fallback). Players are never given its source. The Legal Office case portal, case file `VALE-1031`. SQL injection in the search box.
- Celeste took all five first statements herself, as family counsel, while the house waited for the investigators. This is why the interviews are in her portal.
- Ten records: five guest-visible statements, four sealed counsel's notes (Celeste's private file on the others), and one sealed revision record (written by the portal) for Celeste's own statement. The checkpoint answer is `5` sealed records.
- The lies and the secrets:

| Suspect | Lie in the statement | Truth in the sealed record |
| :---- | :---- | :---- |
| Evelyn | Went to the study only for her glasses, the books are in order. | Wired 4.2 million from the company reserve at 19:24, from the study, to cover the collapsed Northgate acquisition. |
| Marcus | Has one account on the house system. | The hidden administrator account from the Ghost Admin task. The note does not name `hvac-sync`. |
| Nina | No product code in months, nowhere near the server room. | Copied the Project Lantern lock firmware on 24 October and tried it on the server room door at 19:14 (the two denials in the Smart Lock task). |
| Theo | Every camera ran all night. | Switched off camera 07, on the cellar stairs, from 21:35 to 21:50, for a job interview by video call in the wine cellar. He means to resign. |
| Celeste | In the conservatory on a client call from 22:00 to 22:15. | Her first version (23:52) said she was in the hall and saw the dashboard name Marcus. She withdrew it at 00:33. |

- Evelyn, Nina, and Theo were in the hall at 22:04 and saw the dashboard say `MARCUS-ADMIN`. They are the "three people" in the Commit History task's text. Each of their statements names the other two and not Celeste.
- Marcus's statement puts him at the server room console from ten to a quarter past, matching the Ghost Admin task.
- No camera covers the library: Adrian would not have cameras on his private rooms. Camera 07 covers the cellar stairs.
- The counsel's notes are in Celeste's voice and serve the replacement will's Article 4: they rate each person's secret as grounds for "unfitness". Her note on Marcus says to point the investigators at his hidden account first, as Adrian's findings in the Ghost Admin task predicted.
- The revision record is in the portal's voice. Rule: counsel can edit a filed statement but cannot erase one.
- Flag: `THM{SECRETS_ARE_NOT_MURDER}`

## Commit History facts

- Artifacts: `blackthorn-dashboard/` (stage 1, a Git repository), `README.txt`, and `signing-record.zip` (stage 2, holding `signing-record.log`). The zip password is the relabelling commit's short hash, `4fc4f25`.
- The relabelling commit: `4fc4f250b5a56ee45b5bb78425938f2d860556e1`, 2026-10-29T19:26:41-04:00, author and committer `unknown <>`, message "Tidy label formatting". Flag 8 reuses this hash, so update it here whenever the repository is rebuilt with different contents.
- The dashboard is the wall display in the front hall. It shows labels from `dashboard/labels.py` instead of device IDs. The hub's raw log (the Smart Lock task) is unaffected and always records the real device ID.
- Dashboard labels: `ADRIAN-PHONE`, `MARCUS-PHONE`, `EVELYN-PHONE`, `NINA-PHONE` for `BH-PH-0101` to `0104`, `THEO-BADGE`, `KITCHEN-BADGE`, `GROUNDS-BADGE` for the three badges, and `LEGAL-TABLET` for `BH-TAB-0417` until the relabelling.
- House rule: every commit must be signed by a registered workstation key, the hub refuses to deploy anything else, and a key cannot be copied off its workstation. This is why Celeste could scrub the author but not the signature.
- Signing keys (Ed25519, real, generated for the room):

| Key | Workstation | Owner | Registered | Fingerprint |
| :---- | :---- | :---- | :---- | :---- |
| `hub-key-1` | `BH-WS-0401` | `a.vale` | 2025-03-10T09:02:48-04:00 | `SHA256:Un7FyfuK9ATGRziBtVHgxYnq4yDeWKJ7U8K28vmCekU` |
| `hub-key-2` | `BH-WS-0402` | `m.vale` | 2025-03-10T09:05:30-04:00 | `SHA256:5VzICtwEjaJTrTbwc8MF1+k0lTXyhzsTDXyEQEgY1ME` |
| `hub-key-3` | `BH-WS-0418` | `c.ward` | 2025-06-02T10:25:13-04:00 | `SHA256:WWa9zXsseSgn/FtOPchlRXPwssNTquse+dAF2gMr4mw` |
| `hub-key-4` | `BH-WS-0403` | `t.grant` | 2025-09-18T14:10:02-04:00 | `SHA256:cuELgekckCSHa92+Ol9S1SV/y58jwYEXwX18DCWkDXg` |

- New devices: `BH-WS-0401` (Adrian's workstation, `10.13.0.10` in the Ghost Admin task), `BH-WS-0402` (Marcus's, `10.13.0.22`), `BH-WS-0403` (Theo's, `10.13.0.31`).
- The repository names no one from the Legal Office. The mapping from `hub-key-3` to `BH-WS-0418` and `c.ward` exists only in the sealed record.
- Three people in the hall saw the dashboard say `MARCUS-ADMIN` at 22:04 (task text). The Counsel Portal task names them: Evelyn, Nina, and Theo.
- How the tablet signed in as `m.vale` is answered in the Last Testament task (the recovery envelope).
- Flag: `THM{FOLLOW_THE_COMMIT}`

## The Last Testament facts

- Artifact: `case-board/`, a WSGI app hosted at `https://blackthorn-case-board.vercel.app/` (local `serve.py` as a fallback). A timeline with four locked rows, then the estate archive's release page for Adrian's message.
- The four answers, in row order: `4fc4f25` (the Commit History task), `hvac-sync` (the Ghost Admin task), `BH-TAB-0417` (the Smart Lock task), and the replacement will's SHA-256 (the Two Wills task). If any of these change upstream, `build/make_board.py` must be updated and rerun.
- The release page trusts a `role` cookie, set to `guest` on the first visit. Changing it to `trustee` releases the message once the board is complete.
- Adrian's message: archive entry `EA-0043`, "For the Trustee, at midnight", recorded 2026-10-30T22:10:00-04:00, release time 2026-11-01T00:00:00-04:00, addressed to Celeste. It says the papers revoking her authority as Trustee are drawn up on his desk in the library, that he will sign them in front of the family at midnight, and that an independent trustee takes over in the morning. Unsigned, they end nothing, which is why his death before midnight matters.
- How Celeste signed in as `m.vale` (open since the Smart Lock task): the Legal Office kept a sealed recovery envelope, with the password, for every family account. Counsel opened the one for Marcus's account on 26 October, with no request from Marcus and no note in the file. The archive told Adrian, which is what set off his actions on 27 and 28 October.
- Order of the motive (investigators' note): Celeste opened the envelope on 26 October as the first step of a forgery she meant to take her time over, before Adrian suspected her. Her name on the guest list on 28 October told her she was found out, so on 29 October she drafted the replacement will and relabelled the dashboard. Dessert confirmed the midnight deadline, and the forgery became a murder.
- Adrian knew about `hvac-sync` and considered it embarrassing, not dangerous. He did not know a replacement will existed. Nothing in this task describes how he died.
- The solved rows name Celeste and `BH-WS-0418`. Nothing readable in the shipped `api/index.py` does: notes and message are sealed with the answers.
- Flag: `THM{CELESTE_WARD}`
