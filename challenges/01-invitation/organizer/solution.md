# The Invitation (ORGANIZER ONLY)

Flag: `THM{THE_GUEST_LIST_CHANGED}`

Target solve time: about 5 minutes. Skills: QR decoding, viewing page source. No VM is involved: the task ships one download, and the portal snapshot is hosted on Vercel at https://blackthorn-portal.vercel.app/.

## Intended solution

1. Download `invitation.png`.
2. Decode the QR code on `invitation.png`, for example `zbarimg invitation.png`, a phone camera, or any QR decoder. It yields `http://portal.blackthorn.thm/rsvp/hallows-eve-1031/`.
3. Swap the dead hostname for the hosted snapshot and keep the path: `https://blackthorn-portal.vercel.app/rsvp/hallows-eve-1031/`.
4. View the page source (Ctrl+U in a browser, or `curl`). An HTML comment above the guest list contains the flag and the edit timestamp.

## No shortcut

The snapshot is no longer a download, so it cannot be grepped. The front page does not link to the event page, and Vercel does not list folders, so `/rsvp/` cannot be browsed. The QR code is the way in.

## What players should take away

- The printed card (dated 17 October 2026) names four guests. The snapshot page names five.
- The guest list was changed on 2026-10-28T23:41:07-04:00, eleven days after printing, and the added guest is Celeste Ward.

This places Celeste in the house without accusing her. Do not explain why she was added: that belongs to Flag 8.

## Hints, in order of generosity

1. "Any QR decoder will do, including the camera in your pocket. You only need the address it gives you."
2. "The address is dead, but the recovered copy is not. Replace `portal.blackthorn.thm` with `blackthorn-portal.vercel.app` and keep the rest of the address."
3. "Browsers show you the page. Ctrl+U shows you what the page is made of."

## Publishing to the room

- Upload `invitation.png` as the task file. Check that it still decodes after download; if the platform recompresses it beyond reading, zip it.
- The snapshot is hosted at https://blackthorn-portal.vercel.app/, deployed from `blackthorn-portal/portal.blackthorn.thm/` (Vercel project `blackthorn-portal`). Redeploy after editing the pages: `cd challenges/01-invitation/blackthorn-portal/portal.blackthorn.thm && npx vercel deploy --prod`.
- If hosting fails on the night, zip `blackthorn-portal/` into `task1-portal.zip` as a fallback; players run `python3 serve.py` (its README covers that) and use `localhost:8000` in place of the hosted address.
- Paste `task.md` into the task body and set the answer to the flag above.

## Rebuilding

`invitation.png` is a hand-made image with no build script. If the QR payload, the print date, the reply date, or the printed guest list changes, the image has to be remade by hand, and its QR must still decode to the payload in `canon/canon.md`. The portal needs no build step: `blackthorn-portal/` is the source, so edit the pages under `portal.blackthorn.thm/` in place (and `serve.py`, `README.txt` for the local fallback), then redeploy. Keep `canon/canon.md` in sync.
