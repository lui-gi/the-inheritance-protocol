# Task 1: The Invitation (ORGANIZER ONLY)

Flag: `THM{THE_GUEST_LIST_CHANGED}`

Target solve time: about 5 minutes. Skills: QR decoding, viewing page source. No VM is involved: the task ships two downloads, and the portal runs on the player's own machine.

## Intended solution

1. Download both task files: `invitation.png` and `task1-portal.zip`. Unzip the portal.
2. Decode the QR code on `invitation.png`, for example `zbarimg invitation.png`, a phone camera, or any QR decoder. It yields `http://portal.blackthorn.thm/rsvp/hallows-eve-1031/`.
3. In the unzipped `blackthorn-portal` folder, run `python3 serve.py` (the bundled `README.txt` walks through this). The snapshot comes up at `http://localhost:8000/`.
4. Swap the dead hostname for the local one and keep the path: `http://localhost:8000/rsvp/hallows-eve-1031/`.
5. View the page source (Ctrl+U in a browser, or `curl`). An HTML comment above the guest list contains the flag and the edit timestamp.

## Accepted shortcut

`grep -r "THM{" .` over the unzipped folder finds the flag without touching the QR code or the server. So does opening `portal.blackthorn.thm/rsvp/hallows-eve-1031/index.html` straight from disk. This is deliberate: it is a fair forensics move on an opening flag. The snapshot holds three other event pages as decoys so the QR code remains the natural route, and none of them contains a flag. The local server refuses to list folders, so `/rsvp/` cannot be browsed to find the event pages.

Players who take the shortcut still land on the comment that states the timestamp, so they do not miss the clue.

## What players should take away

- The printed card (dated 17 October 2026) names four guests. The snapshot page names five.
- The guest list was changed on 2026-10-28T23:41:07-04:00, eleven days after printing, and the added guest is Celeste Ward.
- `guests.json` (linked from the page head and mentioned in the comment) holds the full revision history. It is optional reading and contains no flag.

This places Celeste in the house without accusing her. Do not explain why she was added: that belongs to Flag 8.

## Hints, in order of generosity

1. "Any QR decoder will do, including the camera in your pocket. You only need the address it gives you."
2. "The address is dead, but your local copy is not. Run `serve.py`, then replace `portal.blackthorn.thm` with `localhost:8000` and keep the rest of the address."
3. "Browsers show you the page. Ctrl+U shows you what the page is made of."

## Publishing to the room

- Zip `player/blackthorn-portal/` (keeping the `blackthorn-portal` folder as the archive root) into `task1-portal.zip`. This is done by hand once the task is final: no zip is kept in the repo.
- Upload both as task files: `player/invitation.png` and `task1-portal.zip`.
- Check that the uploaded `invitation.png` still decodes after download. If the platform will not take two files, or recompresses the image beyond reading, fall back to zipping the two together.
- Paste `task.md` into the task body and set the answer to the flag above.

## Rebuilding

Run `make_invitation.py` after changing the QR payload, the print date, or the printed guest list. The portal needs no build step: `player/blackthorn-portal/` is the source, so edit `serve.py`, `README.txt`, and the pages under `portal.blackthorn.thm/` in place. Keep `canon/canon.md` in sync.

```
python3 -m venv .venv
.venv/bin/pip install -r challenges/01-invitation/build/requirements.txt
.venv/bin/python challenges/01-invitation/build/make_invitation.py
```
