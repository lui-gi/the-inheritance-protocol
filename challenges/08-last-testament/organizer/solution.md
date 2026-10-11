# Task 8: The Last Testament (ORGANIZER ONLY)

Flag: `THM{CELESTE_WARD}`

Checkpoint answer (question 1): `trustee`

Target solve time: about 10 minutes. Skills: pulling four findings together from earlier tasks, reading and editing a browser cookie (client-side trust). No VM is involved: the board runs on the player's machine, and the same app can also be hosted on Vercel.

## The story beat

This is the finale. The board makes the player lay the four pieces of evidence onto the timeline, and each one answers part of the final accusation. Then the estate archive's midnight release supplies the motive: Adrian recorded a message on 30 October revoking Celeste's authority as Trustee at 00:00 on 1 November. The message was to be released to the Trustee only, so the player has to become the Trustee, by changing a cookie the release page trusts. Celeste's whole scheme was an abuse of the Trustee's authority, and the last step of the room is the player borrowing it.

The message also closes the thread left open since Task 3: Celeste could sign in as `m.vale` because the Legal Office kept a sealed recovery envelope, with the password, for every family account, and she opened Marcus's on 26 October.

## How the artifacts are built

One download, `case-board/`, built by `build/make_board.py`. The timeline, the four answers, and Adrian's message live in that script in plain, readable form.

```
case-board/
  README.txt      player instructions, Windows, cookies, troubleshooting
  serve.py        local runner (stdlib wsgiref, no installs)
  vercel.json     rewrites every path to /api/index for hosting
  api/index.py    the WSGI app, generated
```

`serve.py` and Vercel both import the same `app` object from `api/index.py`. The app keeps nothing on the server: the visitor's progress and role live in cookies, which is what Vercel's stateless runtime needs and is also the vulnerability.

Nothing that spoils the ending is readable in `api/index.py`. Each answer is stored only as a hash, each row's note is sealed with that row's answer, and Adrian's message is sealed with all four answers together. A player who reads the source instead of the page still needs the four answers. The build checks this.

To rebuild after editing anything: `python3 challenges/08-last-testament/build/make_board.py`.

## The four rows

| Row | Timeline moment | Asks for | Answer | From |
| :---- | :---- | :---- | :---- | :---- |
| 1 | 29 Oct, 19:26. The dashboard learns to say `MARCUS-ADMIN` | Short hash of the commit | `4fc4f25` | Task 7 |
| 2 | 29 Oct, 23:12. A hidden root account logs in for the last time | Name of the account | `hvac-sync` | Task 4 |
| 3 | 31 Oct, 22:04. The library unlocks on Marcus's account | Device ID | `BH-TAB-0417` | Task 3 |
| 4 | 31 Oct, 22:26. A second will appears | SHA-256 of the will Adrian did not sign | `18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6` | Task 5 |

These are the design document's four: commit history, access logs, device ID, and hashes. Answers are trimmed and case is ignored. Rows can be solved in any order. A solved row shows a short note saying what that evidence proved, and those notes name Celeste and her workstation `BH-WS-0418`.

Six other rows are always visible and need no answer: the will signing (1 Oct), the guest list change (28 Oct), dessert (21:30), Adrian found (22:17), lockdown (22:19), and the locked midnight message.

## The vulnerability

On the first visit the app sets a cookie, `role=guest`. The release page compares that cookie with the role it wants and believes it:

```python
if role.strip().lower() != REQUIRED_ROLE:
```

There is no signature and no server-side session. The refusal page prints the required role, the visitor's current role, and says the role was read from the `role` cookie.

## Intended solution

1. Unzip, run `python3 serve.py`, open `http://localhost:8000/`.
2. Fill in the four locked rows with the answers above. Read the notes that appear.
3. The last row now offers "Ask the archive to release it". Click it. The archive refuses:

   ```
   RELEASE WITHHELD

   This recording is released to one role only.

     required role: trustee
     your role:     guest   (read from the "role" cookie in your browser)

   Release page built by the Legal Office. Not reviewed by A. Vale.
   ```

4. Answer question 1 with `trustee`.
5. Open the browser's developer tools (F12), go to Application (Chrome, Edge) or Storage (Firefox), open Cookies for `localhost`, and change the value of `role` from `guest` to `trustee`. Reload the page.
6. The archive releases the transcript. The flag is on its last line: `Name her: THM{CELESTE_WARD}`.

With `curl`, once the four answers are known:

```
curl -s -b "role=trustee; evidence1=4fc4f25; evidence2=hvac-sync; evidence3=BH-TAB-0417; evidence4=18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6" http://localhost:8000/testament
```

## Adrian's message

Entry `EA-0043`, "For the Trustee, at midnight". Recorded 2026-10-30T22:10:00-04:00, thirty minutes after he sealed his findings about `hvac-sync`. Release time 2026-11-01T00:00:00-04:00. The full text is in `build/make_board.py`. What it establishes:

- The Legal Office kept a sealed recovery envelope, with the password, for every family account. On 26 October the archive told Adrian that counsel had opened the one for Marcus's account, with no request and no note.
- That is why he reread his will on 27 October, left the note in his portrait, and added Celeste to the guest list on 28 October.
- At midnight on 1 November her authority as Trustee is revoked, and an independent trustee takes over in the morning.
- He knew about Marcus's hidden account and considered it embarrassing, not dangerous.
- He did not know a replacement will existed, and the message says nothing about how he died.

An investigators' note follows the transcript and states the case in five sentences before the flag.

## How this maps to the final accusation

| Question in the design document | Where the board answers it |
| :---- | :---- |
| Who killed Adrian Vale? | The flag. |
| What was changed or forged after his death? | Row 4: the will was replaced at 22:26. |
| Which account appears guilty at first, and why is that misleading? | Rows 2 and 3: `m.vale`. His hidden account was idle, and the library was opened from the Legal Office tablet. |
| What four pieces of digital evidence connect the killer to the cover-up? | The four rows. |
| What was the killer's motive? | Adrian's message: the revocation at midnight. |

## Shortcuts

Setting `role=trustee` before the board is complete does nothing: the release page checks the board first, and the message cannot be unsealed without all four answers.

Reading `api/index.py` gives the cookie names and the role, but not the answers, the notes, or the message. A player who has the four answers and reads the source can unseal the message with a few lines of Python. That is more work than changing the cookie and is a fair solve.

Any capitalisation of `trustee` works.

Teams who skipped a task cannot finish this one. That is intended: this task is the one that requires the others. Give them the hint for the missing row if time is short.

## Common stumbles

- Port 8000 still in use by the Task 6 portal. Stop it, or run `python3 serve.py 8080`. Cookies are shared between ports on `localhost` in most browsers, which is harmless here.
- Editing the cookie and not reloading the page.
- Adding a second cookie called `role` with a different path instead of editing the existing one. The "Clear the board" link resets everything.
- Pasting the hash with a trailing newline is fine: answers are trimmed. Pasting the genuine will's hash instead of the replacement's is the usual wrong answer for row 4.
- Private windows and "block all cookies" settings stop the board remembering anything.

## Hints, in order of generosity

1. "Each locked row names the task its answer came from. Row 4 wants the hash of the will that did not match Adrian's receipt, the same one that opened the zip in Task 5."
2. "The archive told you the role it wants and where it read yours from. Open your browser's developer tools with F12 and look for Cookies under Application or Storage."
3. "Change the `role` cookie from `guest` to `trustee` and reload the release page."

## Hosting note

The app is stdlib only, so no `requirements.txt` is needed. Deploying `case-board/` to Vercel serves the board from `api/index.py` with `vercel.json` routing every path to it. Not hosted yet, and not tested on Vercel. Unlike Task 6, this app uses three paths (`/submit`, `/testament`, `/reset`), redirects, and cookies, so check on the first deploy that the app sees the original path after the rewrite and that `Set-Cookie` headers on redirects come through. When it is hosted, swap `http://localhost:8000/` in the task text for the hosted URL. The local download can still ship as a fallback.

## Publishing to the room

- Zip the `case-board` folder into `task8-case-board.zip` and upload it as the task file. This is done by hand once the task is final. Delete any `__pycache__` folder first.
- Do not include the `organizer` or `build` folders.
- Paste `task.md` into the task body. Set the answers to `trustee` and the flag above.

## Rebuilding

Run this after changing the timeline, an answer, the message, or the flag. If Task 5's wills or Task 7's repository are ever rebuilt with different contents, their hashes change: update rows 4 and 1 in `build/make_board.py` and rerun. The build needs only the Python standard library.

```
python3 challenges/08-last-testament/build/make_board.py
```
