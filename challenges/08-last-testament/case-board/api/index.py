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
{
 "role": "trustee",
 "rows": [
  {
   "kind": "fixed",
   "when": "1 Oct, 15:20",
   "text": "Adrian Vale signs his will and files its checksum in the estate archive."
  },
  {
   "kind": "fixed",
   "when": "28 Oct, 23:41",
   "text": "Adrian adds a fifth name to the Halloween guest list: Celeste Ward, family counsel."
  },
  {
   "kind": "slot",
   "number": 1,
   "when": "29 Oct, 19:26",
   "text": "Somebody teaches the hall dashboard to call one device MARCUS-ADMIN.",
   "question": "Commit History: what is the short hash of the commit that did it?",
   "style": "lower",
   "check": "4a94a26d11cadfa55ddb49a0ad74f8f8e8b8ff6c45dbe2f02af2b5a1a0d9133e",
   "sealed_note": "Q6GB+p/Px9GQ9GAe7AuuMzYcLhurjY7jzM3FHsNxXDiuDT829wYqJfrBLzI692fZfwEcZrzFlKSCkb8Vn/P8XdeaT0rf6HwIBduizSQCFYX5EX3STDb/EEz3+IrcE2RO63v6MtX5CkgWSTgJUzwZyIZxgMYIfKOgbrXx5QFd4f2SVDQbAlDR/hPcVeHzUHQ41uOJTlcYtVu+iuj5vQEwHaa3J2HkzIZdBOZIbScSUYol2vY5C29BW9GW"
  },
  {
   "kind": "slot",
   "number": 2,
   "when": "29 Oct, 23:12",
   "text": "A hidden root account on the house server logs in for the last time.",
   "question": "Ghost Admin: what is the name of that account?",
   "style": "lower",
   "check": "4e72bf99df06be6a58b01b7a9f87c1920a394143f55cfce7f32ab46e29a6dd69",
   "sealed_note": "Z8O2HC2WZFMn9IVgoJOBt4ALJr/VKLYQCwG/mnhUmE+4LKFhm8/N2Fe8cdQYsL0VMSLgIKhtTS5kxl+8XwC3+OStj+PhFg6igjz9AKcRsEKNLOhhVOjUQri1WvGDf4IYOgYz7jOayaA0mwU8KgcnNxO8tXAmX1tpOKI2WNxNXDiTZbnBt5jcUgig2NugFnN/ltqvuL5ekvrE+O/TZD9TgLhINKZcFpIesxM="
  },
  {
   "kind": "fixed",
   "when": "31 Oct, 21:30",
   "text": "Dessert. Adrian tells the table: \"By midnight, none of you will own what you think you own.\""
  },
  {
   "kind": "slot",
   "number": 3,
   "when": "31 Oct, 22:04",
   "text": "The library door unlocks on Marcus Vale's account.",
   "question": "The Smart Lock: what is the ID of the device that opened it?",
   "style": "upper",
   "check": "4b32da62622df5fef1e5aa5eadf7d0d35ff5ee621de918655860fb295429bdab",
   "sealed_note": "/tZYPiKqTvItr4YD/VJNCJbX5ywbBskEscCy9VLFHDChUfmIf2sZnzG3qDoRiUZNnsPmo5emtAp1CZdf2EhRHy1J4wnQemu3wG2iMyUlsmgyw3kB6qV5aOKcnG/1oX9xPCp1JZumN30FFrtZ50YX3ZXWt0/rP+VZKaNFcOBVwwiclBdhYaWgqUoYQzmdYwj+bgUh1jV/ndw2LY4nvd/qoskR2sKJWUKl76gTupMvvjPoD8NQa01YeToCVTcF"
  },
  {
   "kind": "fixed",
   "when": "31 Oct, 22:17",
   "text": "Adrian Vale is found dead in the library."
  },
  {
   "kind": "fixed",
   "when": "31 Oct, 22:19",
   "text": "The house locks down and the network uplink drops."
  },
  {
   "kind": "slot",
   "number": 4,
   "when": "31 Oct, 22:26",
   "text": "A second will appears in Adrian's entry in the estate archive.",
   "question": "The Two Wills: what is the SHA-256 of the will Adrian did NOT sign?",
   "style": "lower",
   "check": "f05dfef789c0dee78bf31baf0e57f678b6976d148941e4373bcdec804440af1d",
   "sealed_note": "rfGPaiDvOQhYVqOufyIKHTmdDXknB3jAIJQMDKGW4BEkvb4ZlwPQmXHEyojw+b+1zLeAxNF+A8h8n4KbAcUYyr3ETDjN2gLwdHJ/idQVNNF0RZPY05xpQChZqp0xds10gDT64VD34q8GtYpYK8o8CMw88APDQK3YRWSW9iwvjcwhx0s4o/B8/y3iyivO1oS368LI6hBM9O5SLUxdgUN1/rxOqS3BABzvaw=="
  },
  {
   "kind": "final",
   "when": "1 Nov, 00:00",
   "text": "A message Adrian recorded the night before, set to be released at midnight."
  }
 ],
 "sealed_testament": "72Um95GUoFYjBT1tU/cL7haO4ohganHIs9n5yObu+6sfE6nDbIy4KjvrfdHMTH6QBrSFzW+aQFnWYtF8F6xyeaX6ELJJXdr3TZ0PAbAy6tM2YOIM/qllS532eltD7u9JiLHt1tsd3EzqicohrcbZau6+3ipNSKYNTcoJzDK+izZUgfwRnjY09aNcf5dSq2ytlqlcSfTHCmXMxagFRgEIUhen8HHrwnilyoZ5Nd0Pp2dGC+tBPdgHUlDcZehODIdLTY+ryoYkCxZZq6P4cwKNzE++rUmE6P/fzmCWIueyeORvOeX5sEgDE5aXuesGpSP21J9UrvXZT+xo3uy0ATPgFSc6wiHwyLiU51Jxnc1Ienezw7qRAcoTOeKfRRiZdNSzFBWSr1QscaIhFQvmaj1awcjJ2LbGjS9zI+p2LR/5o+7LaYlpKCPj9pS8cMHoPmUf5Rp83vdg21gt/sPlouY3GXOAgmpWZ2wh6KH4pU/BJH4iNZNzKgUYbZA1qEsouQc1PL+AHdFMa+OfXt2qxypnj7RFuAfJB7fKyBuc/M5q7pYzr66j5/IU1L2lW8L2pM6Ept+/abGOU94H2wval/GTHaRbLJ5HIQYvENbqtlM9+XoHb/R7cMbFad23tjBv6xCnyb2VRfufwMaes988TKH5UkepiLzEdY5OtRBjC2M7KCBapIKhh0fKzDe+0b8eSjGM/ACo7h6POnpUF4XqRsFXRX8VK8TTeG4XN0y0W8ASAsWhQz+nNOrLaWGIC1rz6g6Wigw+hvUYWyVFe/0j+EsgU+XcrBLo/RCmOLHXNtXJ3ekynh8G8MgSez/lhUURbuInue6ke3BZq1V1vjoj+goOuxlKQgBJmEicojnpWmAa/nAjSIUfp29sR0mf/Bd/mwRywzgNqF0+1yM8rjSqxJpchAh3NXstoPuX8PoBegXxBPXWkb3exwALI3bPLS8VHXvSUZ3n83/sPenYJCdRW5KyltjGU5jB9uFQPqZrw3ioQU6haPb6EW2u1s4r80zaK3kAYOXav3nLWrED2iposMkMkynr7jpQO2dHBxZz/NvkZCeyQTsoSY17YraOZCihPvZSqPACxApp22IRWPAyUYzeraTxrfczbjEEp8rRBdUEyCLaXfWaUhnzGVhvtejB5kHsFPZAA4Vzo54Aln/0cNGWUOo/iFTKWtohWMD1FnlGVzCJNUgOgH/OmxisyXOSKyZn4SfekELFsSuI/REUGmCXgQTaIlhD4rD8qiZba5gn+LaC4AX2HIgLL2mjs4Ltg9jQdvARjkOzo63L7WL23K1dzPiSNIzE8q+jkPhVMO7h2wiQ35MnuNDbo5vsQ5Qg3xFep3iFHIQGMpvZ06jmAVv8245BlOftpQ+5ZObd9SQUxMdcdTgXm0uzn7Fqevfe/AOKpTWmIl3QUfDZ+xCqa3x1q8S7zy8zIIMuMftpLEm0CY50EdozNTJs2CJhnTCYXKq+Rh10nY6geeRXsLU0S2c6GrjIdMZL5JAf4UcZQFkiV0oZjk0yfsl3Jrg+oVAd6jcfcYpyaM0gxktRlvGoUNyX+tyLpTd8Ba6gpZLBdCUkxaJo4weIcVRtKEQWObJdYff5LwvqmmTvedlr4KKpgbgSAxY3vGTOCR8VjgvpjW3D9tVQLbdScAhjc9cO7bvWReET55GGq6cquXRK0OMZrUJM8rZ/W6Nlvh905aG4v/jph4+j5gTtLAof+jBbgWiXIEiNg5eOYsV5OKzq4YBgLg17VUhnYC2IieCySuLM1aOXmOsz0FnXwqT+o60BKsMbABqXHwOJzfHya54t7IDRFFj/kW77wGiVd+yAClUllIBS8Mwwn2VWAwTgqU7TMGIr2NQBtOH3qdpXmyfUujWPdIT3to8v5vjARK4D1qG+nQw71fZjDXF+7Av81qTs2ZgYYlLpO4K5y533kZAeuXyFcpChGnDrY4Cckc7cFMruOf+huQ=="
}
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
    key = hashlib.sha256("\x1f".join(answers).encode("utf-8")).digest()
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
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + html.escape(title) + '</title>\n<style>' + STYLE + '</style>\n</head>\n<body>\n'
        '<h1>' + html.escape(title) + '</h1>\n<p class="sub">' + html.escape(subtitle) + '</p>\n'
        + body +
        '\n<footer>You are signed in as: <strong>' + html.escape(role) + '</strong>. '
        'This site keeps no accounts. It remembers you with cookies, and takes their word for it. '
        '<a href="/reset">Clear the board and start again</a>.</footer>\n</body>\n</html>'
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
                 "\n".join(parts), role)


def _testament(given, role):
    title, subtitle = "Blackthorn Estate Archive", "Scheduled release EA-0043: \"For the Trustee, at midnight\""
    if len(given) < len(SLOTS):
        body = ('<p>The archive will not discuss this entry until the case board is complete.</p>'
                '<p><a class="button" href="/">Back to the board</a></p>')
        return _page(title, subtitle, body, role)
    if role.strip().lower() != REQUIRED_ROLE:
        body = (
            '<div class="blocked">RELEASE WITHHELD\n\n'
            'This recording is released to one role only.\n\n'
            '  required role: ' + html.escape(REQUIRED_ROLE) + '\n'
            '  your role:     ' + html.escape(role) + '   (read from the "role" cookie in your browser)\n\n'
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
