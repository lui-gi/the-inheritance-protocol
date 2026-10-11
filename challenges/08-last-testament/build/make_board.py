#!/usr/bin/env python3
"""Build the Case Board app module for Task 8.

This script holds the timeline, the four evidence answers, and Adrian's last
message in plain, organizer-readable form, and writes the shipped app module
(case-board/api/index.py).

Nothing that would spoil the ending is left readable in that module:

  - each evidence answer is stored only as a hash,
  - the note that appears when a row is solved is sealed with that row's answer,
  - Adrian's message (and the flag) is sealed with all four answers together.

So a player who opens the source instead of the page still has to bring the
four answers from Tasks 3, 4, 5, and 7. The sealing is a keystream made from
SHA-256. It is there to stop `grep`, not a cryptographer.

Run from anywhere:

    python3 challenges/08-last-testament/build/make_board.py

Nothing to install. Edit the values here, rerun, and the shipped module is
regenerated. Values below must stay in sync with canon/canon.md.
"""
import base64
import hashlib
import json
import zlib
from pathlib import Path

FLAG = "THM{CELESTE_WARD}"

REQUIRED_ROLE = "trustee"  # the role the release page wants. Visitors start as "guest"

# The timeline, top to bottom. Three kinds of row:
#   ("fixed", when, text)                               always shown
#   ("slot", when, text, question, style, answer, note) locked until the answer is given
#   ("final", when, text)                               Adrian's message, opens when all slots are solved
# style says how an answer is tidied before checking: "upper" or "lower".
TIMELINE = [
    ("fixed", "1 Oct, 15:20",
     "Adrian Vale signs his will and files its checksum in the estate archive."),
    ("fixed", "28 Oct, 23:41",
     "Adrian adds a fifth name to the Halloween guest list: Celeste Ward, family counsel."),
    ("slot", "29 Oct, 19:26",
     "Somebody teaches the hall dashboard to call one device MARCUS-ADMIN.",
     "Task 7: what is the short hash of the commit that did it?", "lower",
     "4fc4f25",
     "Commit 4fc4f25, \"Tidy label formatting\". The author was scrubbed, but the commit is "
     "signed by the key on BH-WS-0418, the Legal Office workstation registered to Celeste "
     "Ward. It relabels the Legal Office tablet. The frame was built two days before the dinner."),
    ("slot", "29 Oct, 23:12",
     "A hidden root account on the house server logs in for the last time.",
     "Task 4: what is the name of that account?", "lower",
     "hvac-sync",
     "hvac-sync, created by Marcus in May. Real misconduct, and Adrian knew about it. It did "
     "not log in on 30 or 31 October, and Marcus was at the server room console under his own "
     "name from 22:03 to 22:15. A red herring, with root."),
    ("fixed", "31 Oct, 21:30",
     "Dessert. Adrian tells the table: \"By midnight, none of you will own what you think you own.\""),
    ("slot", "31 Oct, 22:04",
     "The library door unlocks on Marcus Vale's account.",
     "Task 3: what is the ID of the device that opened it?", "upper",
     "BH-TAB-0417",
     "BH-TAB-0417, the Legal Office tablet, registered to Celeste Ward. It was signed in as "
     "her all evening, as m.vale for six minutes, then as her again. Marcus's own phone was "
     "at the server room door. The hall dashboard called the tablet MARCUS-ADMIN."),
    ("fixed", "31 Oct, 22:17",
     "Adrian Vale is found dead in the library."),
    ("fixed", "31 Oct, 22:19",
     "The house locks down and the network uplink drops."),
    ("slot", "31 Oct, 22:26",
     "A second will appears in Adrian's entry in the estate archive.",
     "Task 5: what is the SHA-256 of the will Adrian did NOT sign?", "lower",
     "18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6",
     "Vale_Will_FINAL_signed.pdf, filed by c.ward from BH-WS-0418 nine minutes after Adrian "
     "was found. It fails the manifest he signed. Its Article 4 lets the Trustee vote any "
     "heir's shares for as long as she likes."),
    ("final", "1 Nov, 00:00",
     "A message Adrian recorded the night before, set to be released at midnight."),
]

# Adrian's last recorded message, as the estate archive would have released it.
# Recorded 30 October, half an hour after he sealed his findings about hvac-sync.
TESTAMENT = """\
BLACKTHORN ESTATE ARCHIVE 2.4: SCHEDULED RELEASE
entry:     EA-0043, "For the Trustee, at midnight"
recorded:  2026-10-30T22:10:00-04:00 by a.vale
release:   2026-11-01T00:00:00-04:00, to the Trustee of the Vale Family Trust
status:    RELEASED

TRANSCRIPT

Celeste. If the archive has done as it was told, it is midnight, you are the
only person hearing this, and dessert went the way I planned.

I will be brief, which you will find out of character.

The Legal Office keeps a sealed recovery envelope for every family account,
with the password inside. That was my idea, and it was a poor one. On
26 October the archive told me that the envelope for Marcus's account had been
opened, by counsel, with no request from Marcus and no note in the file. You
may have had a reason. I have waited four days to hear it.

So I did what I do. I reread my will, and it still matches the receipt I
filed. I left a note where a sensible person would look. And I put you on the
guest list, because I would rather do this with you in the room.

As of this moment, midnight on the first of November, your authority as
Trustee of the Vale Family Trust is revoked. The papers are signed and filed.
An independent trustee takes over in the morning. You keep your fee and your
parking space, and nothing else.

To the rest of the family, when this is read to you: nobody owns less than
they did yesterday, whatever I said over dessert. Marcus, I know about the
account you named after the air conditioning. We will talk. It is
embarrassing, not dangerous, and telling those two apart is the whole job.

Good night, Celeste. An account is not a person, a filename is not a
signature, and a title is not a right.

Adrian Vale

END OF TRANSCRIPT

INVESTIGATORS' NOTE

This message was never released. At midnight its only permitted listener was
the Trustee, and the Trustee had spent the evening making sure there would be
nothing left to revoke.

She had Marcus's password from the envelope. She had already taught the
dashboard to blame him. At 22:04 her tablet opened the library under his
name. At 22:26 her workstation filed a will that made her authority permanent.
She was ninety-four minutes ahead of this recording.

Everyone in the house lied. One person needed the logs to lie as well.

Name her: {flag}
""".format(flag=FLAG)


def tidy(answer, style):
    answer = answer.strip()
    return answer.upper() if style == "upper" else answer.lower()


def answer_hash(number, answer):
    return hashlib.sha256(f"blackthorn-case-board:{number}:{answer}".encode("utf-8")).hexdigest()


def seal(text, *answers):
    """Compress, then XOR with a SHA-256 keystream keyed by the answers."""
    key = hashlib.sha256("\x1f".join(answers).encode("utf-8")).digest()
    data = zlib.compress(text.encode("utf-8"), 9)
    stream = b"".join(hashlib.sha256(key + block.to_bytes(4, "big")).digest()
                      for block in range(len(data) // 32 + 1))
    return base64.b64encode(bytes(a ^ b for a, b in zip(data, stream))).decode("ascii")


def build_data():
    rows, answers = [], []
    for row in TIMELINE:
        if row[0] == "slot":
            _, when, text, question, style, answer, note = row
            assert tidy(answer, style) == answer, f"answer {answer!r} is not in its own tidy form"
            answers.append(answer)
            number = len(answers)
            rows.append({"kind": "slot", "number": number, "when": when, "text": text,
                         "question": question, "style": style,
                         "check": answer_hash(number, answer), "sealed_note": seal(note, answer)})
        else:
            rows.append({"kind": row[0], "when": row[1], "text": row[2]})
    assert sum(row["kind"] == "final" for row in rows) == 1
    return {"role": REQUIRED_ROLE, "rows": rows, "sealed_testament": seal(TESTAMENT, *answers)}, answers


APP_TEMPLATE = '''\
#!/usr/bin/env python3
"""Blackthorn House investigation: Case Board (WSGI app).

A timeline of the night Adrian Vale died, with four gaps. Each gap is filled by
a piece of evidence from an earlier task. When all four are in, the estate
archive's last scheduled release becomes reachable.

The same `app` object serves two ways with no changes:

  - Locally, `serve.py` runs it with Python's built-in wsgiref server.
  - On Vercel, the serverless Python runtime imports `app` from this file.

Nothing is stored on the server. Everything the board knows about a visitor
(the evidence they have entered, and their role) lives in that visitor's
cookies, and the board believes whatever those cookies say.

The answers are not in this file. Each one is kept only as a hash, and the
text it unlocks is sealed with the answer itself.
"""
import base64
import hashlib
import html
import json
import zlib
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

# Built by build/make_board.py. Do not hand-edit.
_DATA = json.loads(r"""
__DATA_LITERAL__
""")

ROWS = _DATA["rows"]
SLOTS = [row for row in ROWS if row["kind"] == "slot"]
REQUIRED_ROLE = _DATA["role"]
DEFAULT_ROLE = "guest"


def _tidy(answer, style):
    answer = answer.strip()
    return answer.upper() if style == "upper" else answer.lower()


def _is_right(slot, answer):
    text = "blackthorn-case-board:%d:%s" % (slot["number"], answer)
    return hashlib.sha256(text.encode("utf-8")).hexdigest() == slot["check"]


def _unseal(sealed, *answers):
    key = hashlib.sha256("\\x1f".join(answers).encode("utf-8")).digest()
    data = base64.b64decode(sealed)
    stream = b"".join(hashlib.sha256(key + block.to_bytes(4, "big")).digest()
                      for block in range(len(data) // 32 + 1))
    return zlib.decompress(bytes(a ^ b for a, b in zip(data, stream))).decode("utf-8")


STYLE = """
  :root { color-scheme: light dark; }
  body { font-family: Georgia, "Times New Roman", serif; max-width: 760px;
         margin: 2.5rem auto; padding: 0 1rem; line-height: 1.5;
         background: #faf7f2; color: #1c1a17; }
  h1 { font-size: 1.5rem; margin-bottom: 0.1rem; }
  .sub { color: #8a8275; font-style: italic; margin-top: 0; }
  .row { border: 1px solid #ddd3c2; border-left: 5px solid #c9c0b0; border-radius: 6px;
         padding: 0.7rem 1rem; margin: 0.7rem 0; background: #fff; }
  .row.locked { border-left-color: #7a2e2e; }
  .row.solved { border-left-color: #3d6b45; }
  .row.final { border-left-color: #1c1a17; }
  .when { color: #8a8275; font-size: 0.85rem; letter-spacing: 0.03em; text-transform: uppercase; }
  .what { margin: 0.15rem 0 0.4rem; font-weight: bold; }
  .note { margin: 0.4rem 0 0; }
  .answer { font-family: ui-monospace, monospace; font-size: 0.85rem; overflow-wrap: anywhere; }
  .wrong { color: #7a2e2e; font-size: 0.9rem; margin: 0.4rem 0 0; }
  form { margin: 0.4rem 0 0; display: flex; gap: 0.5rem; flex-wrap: wrap; }
  label { flex-basis: 100%; font-style: italic; }
  input[type=text] { font: inherit; font-family: ui-monospace, monospace; font-size: 0.9rem;
         padding: 0.4rem 0.6rem; flex: 1 1 14rem; min-width: 0;
         border: 1px solid #c9c0b0; border-radius: 4px; }
  button, a.button { font: inherit; padding: 0.4rem 0.9rem; border-radius: 4px;
         border: 1px solid #7a2e2e; background: #7a2e2e; color: #fff;
         cursor: pointer; text-decoration: none; display: inline-block; }
  .blocked { background: #fdecea; color: #7a2e2e; padding: 0.8rem 1rem; border-radius: 6px;
         font-family: ui-monospace, monospace; font-size: 0.9rem; white-space: pre-wrap; }
  pre.transcript { white-space: pre-wrap; font-family: ui-monospace, monospace; font-size: 0.9rem;
         border: 1px solid #ddd3c2; border-radius: 6px; padding: 1rem; background: #fff; }
  footer { color: #8a8275; font-size: 0.8rem; margin-top: 2.5rem;
           border-top: 1px solid #ddd3c2; padding-top: 0.8rem; }
  footer a { color: inherit; }
  @media (prefers-color-scheme: dark) {
    body { background: #15130f; color: #e8e2d6; }
    .row, pre.transcript { background: #1e1b16; border-color: #3a342a; }
    .row.locked { border-left-color: #b2524a; }
    .row.solved { border-left-color: #6fa878; }
    .row.final { border-left-color: #e8e2d6; }
    input[type=text] { background: #15130f; color: #e8e2d6; border-color: #3a342a; }
    .blocked { background: #2a1512; color: #f1c0b4; }
    .wrong { color: #f1a093; }
  }
"""


def _page(title, subtitle, body, role):
    return (
        '<!doctype html>\\n<html lang="en">\\n<head>\\n<meta charset="utf-8">\\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\\n'
        '<title>' + html.escape(title) + '</title>\\n<style>' + STYLE + '</style>\\n</head>\\n<body>\\n'
        '<h1>' + html.escape(title) + '</h1>\\n<p class="sub">' + html.escape(subtitle) + '</p>\\n'
        + body +
        '\\n<footer>You are signed in as: <strong>' + html.escape(role) + '</strong>. '
        'This site keeps no accounts. It remembers you with cookies, and takes their word for it. '
        '<a href="/reset">Clear the board and start again</a>.</footer>\\n</body>\\n</html>'
    )


def _board(given, role, wrong):
    solved = 0
    parts = ['<p>The night Adrian Vale died, in order. Four moments are missing their evidence. '
             'You found all four in earlier tasks: bring them here.</p>']
    for row in ROWS:
        when = '<div class="when">' + html.escape(row["when"]) + '</div>'
        what = '<p class="what">' + html.escape(row["text"]) + '</p>'
        if row["kind"] == "fixed":
            parts.append('<div class="row">' + when + what + '</div>')
        elif row["kind"] == "slot":
            number = row["number"]
            answer = given.get(number)
            anchor = ' id="row%d"' % number
            if answer is not None:
                solved += 1
                parts.append(
                    '<div class="row solved"' + anchor + '>' + when + what
                    + '<div class="answer">' + html.escape(answer) + '</div>'
                    + '<p class="note">' + html.escape(_unseal(row["sealed_note"], answer)) + '</p></div>')
            else:
                oops = ('<p class="wrong">That does not match the evidence. Check the task it came from and try again.</p>'
                        if wrong == number else '')
                parts.append(
                    '<div class="row locked"' + anchor + '>' + when + what
                    + '<form method="get" action="/submit">'
                    + '<label for="answer%d">' % number + html.escape(row["question"]) + '</label>'
                    + '<input type="hidden" name="row" value="%d">' % number
                    + '<input type="text" id="answer%d" name="answer" autocomplete="off" spellcheck="false">' % number
                    + '<button type="submit">Pin it</button></form>' + oops + '</div>')
        else:
            if solved == len(SLOTS):
                tail = ('<p class="note">The board is complete. The archive still holds this message.</p>'
                        '<p class="note"><a class="button" href="/testament">Ask the archive to release it</a></p>')
            else:
                tail = ('<p class="note"><em>Locked. %d of %d pieces of evidence pinned.</em></p>'
                        % (solved, len(SLOTS)))
            parts.append('<div class="row final" id="final">' + when + what + tail + '</div>')
    return _page("Blackthorn House: Case Board", "Case file VALE-1031, the night of 31 October 2026",
                 "\\n".join(parts), role)


def _testament(given, role):
    title, subtitle = "Blackthorn Estate Archive", "Scheduled release EA-0043: \\"For the Trustee, at midnight\\""
    if len(given) < len(SLOTS):
        body = ('<p>The archive will not discuss this entry until the case board is complete.</p>'
                '<p><a class="button" href="/">Back to the board</a></p>')
        return _page(title, subtitle, body, role)
    if role.strip().lower() != REQUIRED_ROLE:
        body = (
            '<div class="blocked">RELEASE WITHHELD\\n\\n'
            'This recording is released to one role only.\\n\\n'
            '  required role: ' + html.escape(REQUIRED_ROLE) + '\\n'
            '  your role:     ' + html.escape(role) + '   (read from the "role" cookie in your browser)\\n\\n'
            'Release page built by the Legal Office. Not reviewed by A. Vale.</div>'
            '<p><a class="button" href="/">Back to the board</a></p>')
        return _page(title, subtitle, body, role)
    text = _unseal(_DATA["sealed_testament"], *[given[slot["number"]] for slot in SLOTS])
    body = ('<pre class="transcript">' + html.escape(text) + '</pre>'
            '<p><a class="button" href="/">Back to the board</a></p>')
    return _page(title, subtitle, body, role)


def _cookie(name, value, clear=False):
    age = "0" if clear else "86400"
    return ("Set-Cookie", "%s=%s; Path=/; Max-Age=%s; SameSite=Lax" % (name, value, age))


def _read(environ):
    """What the visitor's cookies claim: their correct answers so far, and their role."""
    cookies = SimpleCookie()
    try:
        cookies.load(environ.get("HTTP_COOKIE", ""))
    except Exception:
        pass
    given = {}
    for slot in SLOTS:
        morsel = cookies.get("evidence%d" % slot["number"])
        if morsel is not None and _is_right(slot, morsel.value):
            given[slot["number"]] = morsel.value
    role = cookies["role"].value if "role" in cookies else None
    return given, role


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/") or "/"
    params = parse_qs(environ.get("QUERY_STRING", ""))
    given, role = _read(environ)
    headers = []
    if role is None:
        role = DEFAULT_ROLE
        headers.append(_cookie("role", DEFAULT_ROLE))

    def redirect(location, extra=()):
        start_response("303 See Other", [("Location", location), ("Content-Length", "0")] + headers + list(extra))
        return [b""]

    if path == "/reset":
        cleared = [_cookie("evidence%d" % slot["number"], "", clear=True) for slot in SLOTS]
        headers[:] = [_cookie("role", DEFAULT_ROLE)]
        return redirect("/", cleared)

    if path == "/submit":
        try:
            number = int(params.get("row", [""])[0])
            slot = next(slot for slot in SLOTS if slot["number"] == number)
        except (ValueError, StopIteration):
            return redirect("/")
        answer = _tidy(params.get("answer", [""])[0], slot["style"])
        if _is_right(slot, answer):
            return redirect("/#row%d" % number, [_cookie("evidence%d" % number, answer)])
        return redirect("/?wrong=%d#row%d" % (number, number))

    if path == "/testament":
        body = _testament(given, role)
    else:
        try:
            wrong = int(params.get("wrong", [""])[0])
        except ValueError:
            wrong = None
        body = _board(given, role, wrong)

    data = body.encode("utf-8")
    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(data))),
        ("Cache-Control", "no-store"),
    ] + headers)
    return [data]
'''


def main():
    here = Path(__file__).resolve().parent
    out = here.parent / "case-board" / "api" / "index.py"
    data, answers = build_data()
    literal = json.dumps(data, indent=1)
    assert '"""' not in literal
    module = APP_TEMPLATE.replace("__DATA_LITERAL__", literal)
    # Nothing that spoils the ending may be readable in the shipped module.
    for secret in [FLAG, "THM{", "Celeste", "c.ward", "BH-WS-0418", "revoked"] + answers:
        assert secret not in module.replace("Celeste Ward, family counsel", ""), f"{secret} is readable in the app"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(module)
    print(f"Wrote {out} ({len(answers)} evidence rows)")
    for number, answer in enumerate(answers, start=1):
        print(f"  evidence{number}: {answer}")
    print(f"  role:      {REQUIRED_ROLE}")


if __name__ == "__main__":
    main()
