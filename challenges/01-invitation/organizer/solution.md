# Task 1: The Invitation (ORGANIZER ONLY)

Flag: `THM{THE_GUEST_LIST_CHANGED}`

Target solve time: about 5 minutes. Skills: QR decoding, viewing page source. No VM is involved: everything is in the task download.

## Intended solution

1. Download and unzip `task1-invitation.zip`.
2. Decode the QR code on `invitation.png`, for example `zbarimg invitation.png`, a phone camera, or any QR decoder. It yields `http://portal.blackthorn.thm/rsvp/hallows-eve-1031/`.
3. Follow the same path inside the snapshot folder and open `portal.blackthorn.thm/rsvp/hallows-eve-1031/index.html`.
4. View the page source (Ctrl+U in a browser, or any text editor). An HTML comment above the guest list contains the flag and the edit timestamp.

## Accepted shortcut

`grep -r "THM{" .` over the unzipped folder finds the flag without touching the QR code. This is deliberate: it is a fair forensics move on an opening flag. The snapshot holds three other event pages as decoys so the QR code remains the natural route, and none of them contains a flag.

Players who take the shortcut still land on the comment that states the timestamp, so they do not miss the clue.

## What players should take away

- The printed card (dated 17 October 2026) names four guests. The snapshot page names five.
- The guest list was changed on 2026-10-28T23:41:07-04:00, eleven days after printing, and the added guest is Celeste Ward.
- `guests.json` (linked from the page head and mentioned in the comment) holds the full revision history. It is optional reading and contains no flag.

This places Celeste in the house without accusing her. Do not explain why she was added: that belongs to Flag 8.

## Hints, in order of generosity

1. "Any QR decoder will do, including the camera in your pocket. You only need the address it gives you."
2. "The address is dead, but look at the folder name in the download. The rest of the address is a path inside it."
3. "Browsers show you the page. Ctrl+U shows you what the page is made of."

## Publishing to the room

- Upload `player/task1-invitation.zip` as the task file.
- Paste `task.md` into the task body and set the answer to the flag above.

## Rebuilding

Run both steps after changing anything under `site/`, the QR payload, the print date, or the printed guest list. Keep `canon/canon.md` in sync.

```
python3 -m venv .venv
.venv/bin/pip install -r challenges/01-invitation/build/requirements.txt
.venv/bin/python challenges/01-invitation/build/make_invitation.py
.venv/bin/python challenges/01-invitation/build/make_bundle.py
```
