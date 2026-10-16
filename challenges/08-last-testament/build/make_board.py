#!/usr/bin/env python3
"""Build the Case Board app module for the Last Testament task.

This script holds the timeline, the four evidence answers, and Adrian's last
message in plain, organizer-readable form, and writes the shipped app module
(case-board/api/index.py).

Nothing that would spoil the ending is left readable in that module:

  - each evidence answer is stored only as a hash,
  - the note that appears when a row is solved is sealed with that row's answer,
  - Adrian's message (and the flag) is sealed with all four answers together.

So a player who opens the source instead of the page still has to bring the
four answers from the Smart Lock, the Ghost Admin, the Two Wills, and the Commit History tasks. The sealing is a keystream made from
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
     "Commit History: what is the short hash of the commit that did it?", "lower",
     "4fc4f25",
     "Commit 4fc4f25, \"Tidy label formatting\". The author was scrubbed, but the commit is "
     "signed by the key on BH-WS-0418, the Legal Office workstation registered to Celeste "
     "Ward. It relabels the Legal Office tablet. The frame was built two days before the dinner."),
    ("slot", "29 Oct, 23:12",
     "A hidden root account on the house server logs in for the last time.",
     "Ghost Admin: what is the name of that account?", "lower",
     "hvac-sync",
     "hvac-sync, created by Marcus in May. Real misconduct, and Adrian knew about it. It did "
     "not log in on 30 or 31 October, and Marcus was at the server room console under his own "
     "name from 22:03 to 22:15. A red herring, with root."),
    ("fixed", "31 Oct, 21:30",
     "Dessert. Adrian tells the table: \"By midnight, none of you will own what you think you own.\""),
    ("slot", "31 Oct, 22:04",
     "The library door unlocks on Marcus Vale's account.",
     "The Smart Lock: what is the ID of the device that opened it?", "upper",
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
     "The Two Wills: what is the SHA-256 of the will Adrian did NOT sign?", "lower",
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

The papers that end your authority as Trustee of the Vale Family Trust are
drawn up and waiting on my desk in the library. They need one signature, and
it is mine. At midnight on the first of November I sign them in front of the
family, and this recording reaches you at the same moment. An independent
trustee takes over in the morning. You keep your fee and your parking space,
and nothing else.

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
the Trustee, and by midnight there was nobody left to sign the papers it
describes. Unsigned, they end nothing.

She had been preparing before Adrian ever suspected her. On 26 October she
took Marcus's password from the envelope: the first step of a forgery she
meant to take her time over, with his account ready to carry the blame. Then
her name appeared on the guest list, on a page that promised paperwork at
midnight. The next evening she drafted her own will for Adrian and taught the
dashboard to blame Marcus. Over dessert Adrian confirmed the deadline out
loud. A forgery that could wait became a murder that could not.

At 22:04 her tablet opened the library under Marcus's name. At 22:26 her
workstation filed a will that made her authority permanent. She was
ninety-four minutes ahead of this recording.

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
  :root {
    --cork: #b48552; --paper: #fbf8ef; --manila: #ecd7a3; --ink: #221d17; --muted: #6e6457;
    --red: #c3231b; --red-dk: #7e140f; --envelope: #2b2421;
    --type: "Courier Prime", "Courier New", Courier, monospace;
    --hand: "Bradley Hand", "Segoe Print", "Chalkboard SE", "Comic Sans MS", cursive;
    --serif: "Iowan Old Style", Palatino, Georgia, serif;
  }
  * { box-sizing: border-box; }
  html { background: #3d2716; }
  body {
    margin: 0; min-height: 100vh; color: var(--ink); font-family: var(--serif); line-height: 1.5;
    background:
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .32 0 0 0 0 .2 0 0 0 0 .09 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"),
      radial-gradient(ellipse at 30% 20%, #c79a64, transparent 60%),
      radial-gradient(ellipse at 80% 90%, #9c6f41, transparent 55%),
      var(--cork);
  }
  /* Wooden frame and vignette, fixed over the edges of the viewport. */
  body::after {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 50;
    box-shadow: inset 0 0 0 12px #5b3b20, inset 0 0 0 14px #2f1d0f, inset 0 0 140px rgba(0, 0, 0, .55);
  }
  main { max-width: 1240px; margin: 0 auto; padding: 48px 36px 64px; }

  /* Masthead: a typed title card and a sticky note. */
  .masthead { display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 28px; margin-bottom: 28px; }
  .title-card { position: relative; background: var(--paper); padding: 22px 30px 18px; transform: rotate(-1.2deg);
    box-shadow: 0 12px 24px -8px rgba(0, 0, 0, .5); }
  .title-card::before, .title-card::after { content: ""; position: absolute; top: -12px; width: 90px; height: 26px;
    background: rgba(240, 228, 196, .78); box-shadow: 0 1px 2px rgba(0, 0, 0, .15); }
  .title-card::before { left: -20px; transform: rotate(-24deg); }
  .title-card::after { right: -20px; transform: rotate(22deg); }
  .kicker { margin: 0; font-family: var(--type); font-size: .78rem; letter-spacing: .3em; text-transform: uppercase; color: var(--red-dk); }
  h1 { margin: 4px 0 2px; font-family: var(--type); font-size: clamp(1.6rem, 4.5vw, 2.5rem); letter-spacing: .04em; text-transform: uppercase; line-height: 1.1; }
  .sub { margin: 0; font-family: var(--hand); font-size: 1.1rem; color: var(--muted); }
  .sticky { max-width: 330px; padding: 18px 20px 16px; background: linear-gradient(170deg, #fff59d, #f6e27a);
    font-family: var(--hand); font-size: 1.05rem; line-height: 1.4; transform: rotate(1.8deg);
    box-shadow: 0 14px 22px -10px rgba(0, 0, 0, .55); }
  .sticky p { margin: 0 0 8px; }
  .progress { display: flex; gap: 6px; margin-top: 8px; }
  .progress i { width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--red-dk); }
  .progress i.on { background: radial-gradient(circle at 35% 30%, #ff8a80, var(--red) 45%, var(--red-dk)); border-color: transparent; }

  /* The board. Strings and pin heads are drawn in one SVG over the cards. */
  .board { position: relative; display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 64px 44px; padding: 28px 4px 16px; }
  .strings, .pins { position: absolute; left: 0; top: 0; overflow: visible; pointer-events: none; }
  .strings { z-index: 0; }
  .pins { z-index: 5; }
  .strings path { fill: none; stroke: var(--red); stroke-width: 2.4; stroke-linecap: round; filter: drop-shadow(0 4px 2px rgba(0, 0, 0, .35)); }
  .strings path.loose { stroke-width: 1.5; opacity: .35; }
  .pins .pin { animation: pop .35s cubic-bezier(.3, 1.6, .5, 1) both; transform-box: fill-box; transform-origin: center; }

  .card { position: relative; z-index: 1; align-self: start; padding: 34px 20px 18px; background: var(--paper);
    transform: rotate(var(--tilt, 0deg)); transform-origin: 50% 14px;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .15), 0 14px 22px -10px rgba(0, 0, 0, .55);
    transition: transform .5s cubic-bezier(.2, .9, .3, 1.3), box-shadow .3s;
    animation: drop .6s cubic-bezier(.2, .8, .3, 1) both; animation-delay: var(--d, 0s); }
  .card:hover { transform: rotate(0deg); box-shadow: 0 1px 1px rgba(0, 0, 0, .15), 0 22px 30px -12px rgba(0, 0, 0, .6); z-index: 3; }
  .settled .card { animation: none; }
  /* Without script, each card carries its own pin. */
  .card::before { content: ""; position: absolute; top: 7px; left: calc(50% - 7px); width: 14px; height: 14px; border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #ff8a80, var(--red) 45%, var(--red-dk)); box-shadow: 0 3px 3px rgba(0, 0, 0, .4); }
  .js .board .card::before { display: none; }

  .when { font-family: var(--type); font-size: .78rem; font-weight: bold; letter-spacing: .12em; text-transform: uppercase; color: var(--red-dk); }
  .what { margin: 6px 0 0; font-size: 1.02rem; }
  .fixed { background: linear-gradient(var(--paper) 0 30px, transparent 30px),
    repeating-linear-gradient(var(--paper) 0 23px, #cfdcea 23px 24px); }
  .fixed .what { font-family: var(--hand); font-size: 1.15rem; line-height: 24px; }

  .tag { display: inline-block; margin-bottom: 8px; padding: 2px 8px; font-family: var(--type); font-size: .7rem; letter-spacing: .2em;
    text-transform: uppercase; border: 1px solid currentColor; color: var(--red-dk); }
  .locked { background: linear-gradient(160deg, #f1dea9, var(--manila) 60%, #dfc68b); }
  .locked form { margin-top: 12px; }
  .locked label { display: block; font-family: var(--type); font-size: .82rem; color: var(--muted); }
  .field { display: flex; gap: 8px; margin-top: 8px; }
  .field input { flex: 1; min-width: 0; padding: 6px 2px; font: .9rem var(--type); color: var(--ink); background: transparent;
    border: 0; border-bottom: 2px dashed rgba(34, 29, 23, .45); border-radius: 0; }
  .field input:focus { outline: none; border-bottom-color: var(--red); }
  button, .button { font: bold .75rem var(--type); letter-spacing: .15em; text-transform: uppercase; padding: 8px 14px;
    color: #fff; background: var(--red); border: 0; border-radius: 3px; cursor: pointer; text-decoration: none; display: inline-block;
    box-shadow: 0 3px 0 var(--red-dk), 0 6px 10px -4px rgba(0, 0, 0, .5); transition: transform .12s, box-shadow .12s; }
  button:hover, .button:hover { transform: translateY(-1px); }
  button:active, .button:active { transform: translateY(2px); box-shadow: 0 1px 0 var(--red-dk); }
  button[disabled] { opacity: .6; cursor: wait; }
  .wrong { margin: 10px 0 0; font-family: var(--hand); color: var(--red); }

  .solved .stamp { position: absolute; top: 12px; right: 12px; padding: 2px 8px; font: bold .85rem var(--type); letter-spacing: .2em;
    text-transform: uppercase; color: var(--red); border: 3px double var(--red); transform: rotate(-12deg); opacity: .85; }
  .answer { margin-top: 10px; padding: 4px 8px; font: .8rem var(--type); background: #fff; border: 1px solid #ddd2bd; overflow-wrap: anywhere; }
  .note { margin: 10px 0 0; font-size: .92rem; color: #3b342b; }
  .flash .stamp { animation: thump .5s cubic-bezier(.3, 1.5, .5, 1) both; }
  .flash { animation: glow 1.6s ease-out; }
  .shake { animation: shake .45s; }

  .final { color: #efe6d6; background: linear-gradient(160deg, #3a302b, var(--envelope)); }
  .final::after { content: ""; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(to bottom right, transparent 49.6%, rgba(255, 255, 255, .06) 50%, transparent 50.4%),
                linear-gradient(to bottom left, transparent 49.6%, rgba(255, 255, 255, .06) 50%, transparent 50.4%); }
  .final .when { color: #f0a59f; }
  .final .note { color: #cfc4b2; font-style: italic; }
  .seal { position: absolute; right: 16px; bottom: 14px; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center;
    font: bold .85rem var(--serif); color: rgba(255, 220, 210, .8);
    background: radial-gradient(circle at 35% 30%, #e0473c, #9d1810 60%, #5e0b07); box-shadow: 0 3px 6px rgba(0, 0, 0, .5); }
  .final.open { box-shadow: 0 0 0 2px var(--red), 0 0 40px rgba(195, 35, 27, .55), 0 14px 22px -10px rgba(0, 0, 0, .55); }
  .final .button { position: relative; z-index: 1; margin-top: 4px; }

  /* Archive pages: one sheet pinned to the board. */
  .sheet { position: relative; max-width: 780px; margin: 10px auto 0; padding: 44px 40px 32px; background: var(--paper);
    box-shadow: 0 18px 34px -12px rgba(0, 0, 0, .6); transform: rotate(-.4deg); animation: drop .6s cubic-bezier(.2, .8, .3, 1) both; }
  .sheet::before, .sheet::after { content: ""; position: absolute; top: 12px; width: 16px; height: 16px; border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #ff8a80, var(--red) 45%, var(--red-dk)); box-shadow: 0 3px 3px rgba(0, 0, 0, .4); }
  .sheet::before { left: 24px; } .sheet::after { right: 24px; }
  .sheet p { margin: 0 0 16px; }
  .blocked, pre.transcript { margin: 0 0 22px; white-space: pre-wrap; overflow-wrap: anywhere; font: .9rem/1.55 var(--type); }
  .withheld { border-top: 6px solid var(--red); }
  .withheld .stamp { position: absolute; top: 54px; right: 34px; padding: 4px 12px; font: bold 1.1rem var(--type); letter-spacing: .2em; text-transform: uppercase;
    color: var(--red); border: 4px double var(--red); transform: rotate(-9deg); opacity: .85; animation: thump .5s .4s cubic-bezier(.3, 1.5, .5, 1) both; }

  footer { margin: 48px auto 0; max-width: 520px; padding: 14px 18px; text-align: center; font-size: .82rem; color: #3b342b;
    background: rgba(251, 248, 239, .92); transform: rotate(.6deg); box-shadow: 0 10px 18px -8px rgba(0, 0, 0, .5); }
  footer a { color: var(--red-dk); }

  @keyframes drop { from { opacity: 0; transform: translateY(-18px) rotate(calc(var(--tilt, 0deg) * 3)); } }
  @keyframes pop { from { transform: scale(0); } }
  @keyframes thump { from { opacity: 0; transform: rotate(-12deg) scale(2.4); } }
  @keyframes glow { 0% { box-shadow: 0 0 0 3px var(--red), 0 0 50px rgba(195, 35, 27, .7); } }
  @keyframes shake { 20%, 60% { translate: -7px 0; } 40%, 80% { translate: 7px 0; } }

  @media (max-width: 600px) {
    body::after { box-shadow: inset 0 0 0 6px #5b3b20, inset 0 0 0 7px #2f1d0f, inset 0 0 80px rgba(0, 0, 0, .5); }
    main { padding: 28px 18px 40px; }
    .board { grid-template-columns: 1fr; gap: 48px; padding-inline: 10px; }
    .sheet { padding: 40px 20px 24px; }
    .withheld .stamp { position: static; display: inline-block; margin-bottom: 14px; }
  }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
  }
"""

# Draws the red string between pins, and pins answers without a page reload.
# Progressive: with script off, the forms and links work as plain pages.
SCRIPT = """
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';

  function el(name, attrs) {
    var node = document.createElementNS(NS, name);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    return node;
  }

  function draw(animate) {
    var board = document.querySelector('.board');
    if (!board) return;
    board.querySelectorAll('svg.strings, svg.pins').forEach(function (n) { n.remove(); });
    var cards = Array.prototype.slice.call(board.querySelectorAll('.card'));
    var pts = cards.map(function (c) {
      return { x: c.offsetLeft + c.offsetWidth / 2, y: c.offsetTop + 14, firm: !c.classList.contains('locked'), card: c };
    });
    var size = { width: board.scrollWidth, height: board.scrollHeight };
    var svg = el('svg', Object.assign({ 'class': 'strings' }, size));
    var top = el('svg', Object.assign({ 'class': 'pins' }, size));
    var defs = el('defs', {});
    var grad = el('radialGradient', { id: 'pinhead', cx: '35%', cy: '30%', r: '70%' });
    [['0%', '#ff8a80'], ['45%', '#c3231b'], ['100%', '#6e0f0b']].forEach(function (s) {
      grad.appendChild(el('stop', { offset: s[0], 'stop-color': s[1] }));
    });
    defs.appendChild(grad);
    top.appendChild(defs);
    var paths = [];
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1];
      var dist = Math.hypot(b.x - a.x, b.y - a.y);
      var sag = Math.min(90, 18 + dist * 0.1);
      var d = 'M' + a.x + ' ' + a.y + ' Q' + (a.x + b.x) / 2 + ' ' + ((a.y + b.y) / 2 + sag) + ' ' + b.x + ' ' + b.y;
      var p = el('path', { d: d, 'class': a.firm && b.firm ? 'firm' : 'loose' });
      svg.appendChild(p);
      paths.push({ node: p, from: a.card, to: b.card });
    }
    pts.forEach(function (pt, i) {
      var g = el('g', { 'class': 'pin' });
      if (animate === 'all') g.style.animationDelay = (0.25 + i * 0.07) + 's';
      else g.style.animation = 'none';
      g.appendChild(el('ellipse', { cx: pt.x + 3, cy: pt.y + 5, rx: 7, ry: 4, fill: 'rgba(0,0,0,.35)' }));
      g.appendChild(el('circle', { cx: pt.x, cy: pt.y, r: 7.5, fill: 'url(#pinhead)' }));
      g.appendChild(el('circle', { cx: pt.x - 2.5, cy: pt.y - 2.5, r: 2, fill: 'rgba(255,255,255,.55)' }));
      top.appendChild(g);
    });
    board.insertBefore(svg, board.firstChild);
    board.appendChild(top);
    if (reduce || !animate) return;
    paths.forEach(function (p, i) {
      if (animate !== 'all' && p.from !== animate && p.to !== animate) return;
      var len = p.node.getTotalLength();
      p.node.style.strokeDasharray = len;
      p.node.style.strokeDashoffset = len;
      p.node.getBoundingClientRect();
      var delay = animate === 'all' ? 0.5 + i * 0.12 : 0.15;
      p.node.style.transition = 'stroke-dashoffset .7s ease ' + delay + 's';
      p.node.style.strokeDashoffset = 0;
    });
  }

  function spotlight(hash) {
    var target = hash && document.getElementById(hash.slice(1));
    if (!target) {
      var wrong = document.querySelector('.wrong');
      target = wrong && wrong.closest('.card');
    }
    if (!target) return null;
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    if (target.classList.contains('solved')) {
      target.classList.add('flash');
    } else if (target.querySelector('.wrong')) {
      target.classList.add('shake');
      var input = target.querySelector('input[type=text]');
      if (input) input.focus({ preventScroll: true });
    }
    return target;
  }

  var pending = 0;
  function redrawSoon() {
    cancelAnimationFrame(pending);
    pending = requestAnimationFrame(function () { draw(false); });
  }
  window.addEventListener('resize', redrawSoon);
  if (document.fonts) document.fonts.ready.then(redrawSoon);

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.closest('.board') || !window.fetch) return;
    e.preventDefault();
    var button = form.querySelector('button');
    if (button) button.disabled = true;
    var url = form.getAttribute('action') + '?' + new URLSearchParams(new FormData(form));
    fetch(url, { credentials: 'same-origin' }).then(function (res) {
      return res.text().then(function (text) { return { text: text, url: new URL(res.url) }; });
    }).then(function (r) {
      var fresh = new DOMParser().parseFromString(r.text, 'text/html').querySelector('main');
      fresh.classList.add('settled');
      document.querySelector('main').replaceWith(fresh);
      history.replaceState(null, '', '/' + r.url.hash);
      draw(false);
      var target = spotlight(r.url.hash);
      if (target && target.classList.contains('solved')) draw(target);
    }).catch(function () { form.submit(); });
  });

  function start() {
    draw(document.querySelector('.board') ? 'all' : false);
    spotlight(location.hash);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
"""

TILTS = ["-2.2", "1.6", "-1.1", "2.3", "-1.7", "0.9", "-2.5", "1.4", "-0.8", "2"]


def _page(title, subtitle, body, role, aside=""):
    return (
        '<!doctype html>\\n<html lang="en">\\n<head>\\n<meta charset="utf-8">\\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\\n'
        '<title>' + html.escape(title) + '</title>\\n<style>' + STYLE + '</style>\\n'
        '<script>' + SCRIPT + '</script>\\n</head>\\n<body>\\n<main>\\n'
        '<header class="masthead"><div class="title-card"><p class="kicker">Case file VALE-1031</p>'
        '<h1>' + html.escape(title) + '</h1><p class="sub">' + html.escape(subtitle) + '</p></div>'
        + aside + '</header>\\n'
        + body +
        '\\n<footer>You are signed in as: <strong>' + html.escape(role) + '</strong>. '
        'This site keeps no accounts. It remembers you with cookies, and takes their word for it. '
        '<a href="/reset">Clear the board and start again</a>.</footer>\\n</main>\\n</body>\\n</html>'
    )


def _board(given, role, wrong):
    solved = len(given)
    dots = ''.join('<i class="on"></i>' if n <= solved else '<i></i>' for n in range(1, len(SLOTS) + 1))
    aside = ('<aside class="sticky"><p>The night Adrian Vale died, in order. Four moments are missing their evidence. '
             'You found all four in earlier tasks: bring them here.</p>'
             '<p>Pinned: %d of %d</p><div class="progress">%s</div></aside>' % (solved, len(SLOTS), dots))
    parts = ['<section class="board">']
    for index, row in enumerate(ROWS):
        style = ' style="--tilt:%sdeg;--d:%.2fs"' % (TILTS[index % len(TILTS)], index * 0.06)
        when = '<div class="when">' + html.escape(row["when"]) + '</div>'
        what = '<p class="what">' + html.escape(row["text"]) + '</p>'
        if row["kind"] == "fixed":
            parts.append('<article class="card fixed"' + style + '>' + when + what + '</article>')
        elif row["kind"] == "slot":
            number = row["number"]
            answer = given.get(number)
            anchor = ' id="row%d"' % number
            if answer is not None:
                parts.append(
                    '<article class="card slot solved"' + anchor + style + '>'
                    + '<span class="stamp">Pinned</span><span class="tag">Exhibit %d</span>' % number
                    + when + what
                    + '<div class="answer">' + html.escape(answer) + '</div>'
                    + '<p class="note">' + html.escape(_unseal(row["sealed_note"], answer)) + '</p></article>')
            else:
                oops = ('<p class="wrong">That does not match the evidence. Check the task it came from and try again.</p>'
                        if wrong == number else '')
                parts.append(
                    '<article class="card slot locked"' + anchor + style + '>'
                    + '<span class="tag">Exhibit %d &middot; missing</span>' % number
                    + when + what
                    + '<form method="get" action="/submit">'
                    + '<label for="answer%d">' % number + html.escape(row["question"]) + '</label>'
                    + '<input type="hidden" name="row" value="%d">' % number
                    + '<div class="field"><input type="text" id="answer%d" name="answer" autocomplete="off" spellcheck="false">' % number
                    + '<button type="submit">Pin it</button></div></form>' + oops + '</article>')
        else:
            if solved == len(SLOTS):
                tail = ('<p class="note">The board is complete. The archive still holds this message.</p>'
                        '<p class="note"><a class="button" href="/testament">Ask the archive to release it</a></p>')
                state = ' open'
            else:
                tail = ('<p class="note">Locked. %d of %d pieces of evidence pinned.</p>'
                        % (solved, len(SLOTS)))
                state = ''
            parts.append('<article class="card final' + state + '" id="final"' + style + '>'
                         + when + what + tail + '<div class="seal">AV</div></article>')
    parts.append('</section>')
    return _page("Case Board", "Blackthorn House, the night of 31 October 2026",
                 "\\n".join(parts), role, aside)


def _testament(given, role):
    title, subtitle = "Estate Archive", "Scheduled release EA-0043: \\"For the Trustee, at midnight\\""
    back = '<p><a class="button" href="/">Back to the board</a></p>'
    if len(given) < len(SLOTS):
        body = ('<section class="sheet"><p>The archive will not discuss this entry until the case board is complete.</p>'
                + back + '</section>')
        return _page(title, subtitle, body, role)
    if role.strip().lower() != REQUIRED_ROLE:
        body = (
            '<section class="sheet withheld"><span class="stamp">Withheld</span>'
            '<div class="blocked">RELEASE WITHHELD\\n\\n'
            'This recording is released to one role only.\\n\\n'
            '  required role: ' + html.escape(REQUIRED_ROLE) + '\\n'
            '  your role:     ' + html.escape(role) + '   (read from the "role" cookie in your browser)\\n\\n'
            'Release page built by the Legal Office. Not reviewed by A. Vale.</div>'
            + back + '</section>')
        return _page(title, subtitle, body, role)
    text = _unseal(_DATA["sealed_testament"], *[given[slot["number"]] for slot in SLOTS])
    body = '<section class="sheet"><pre class="transcript">' + html.escape(text) + '</pre>' + back + '</section>'
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
