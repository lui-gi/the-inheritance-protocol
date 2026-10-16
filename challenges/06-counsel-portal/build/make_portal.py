#!/usr/bin/env python3
"""Build the Counsel Portal app module.

This script holds the portal's records in plain, organizer-readable form, packs
them into a base64 blob, and writes that blob into the shipped app module
(counsel-portal/api/index.py). Packing keeps a curious player from finding the
flag with a quick `grep` through the source: they are meant to break the search,
not read the data file.

Run from anywhere:

    python3 challenges/06-counsel-portal/build/make_portal.py

Nothing to install. The records below are the single source of truth for the
task. Edit them here, rerun, and the shipped module is regenerated.
"""
import base64
import json
import zlib
from pathlib import Path

FLAG = "THM{SECRETS_ARE_NOT_MURDER}"

# Celeste Ward, as family counsel, took all five statements herself while the
# house waited for the investigators, her own included. Each suspect has one
# guest-visible statement (which contains a lie). The four sealed counsel's
# notes are her private file on the others: the real secret behind each lie,
# and what use it is to a Trustee who (under the replacement will's Article 4)
# alone judges whether an heir is fit. The fifth sealed row is not hers: it is
# the portal's own revision record, kept because she edited her statement.
#
# Only Celeste's lie touches the library timeline fixed by the Smart Lock, the Ghost Admin, and the Two Wills tasks: her
# tablet opened the library at 22:04 and Adrian was found at 22:17. The other
# secrets are pinned to lock-log lines from the Smart Lock task (Evelyn's study unlock at
# 19:22:15, Nina's server room denials at 19:14, Theo's wine cellar unlock at
# 21:38:19) and stay clear of dinner (19:30) and of the library.
#
# kind="statement" -> shown in the guest view.
# kind="note"      -> sealed counsel's note; only reachable by breaking the search.
# kind="revision"  -> sealed revision record; same.
RECORDS = [
    # id, suspect, role, kind, time (as filed), body
    (1, "Evelyn Vale", "Daughter, CFO", "statement",
     "2026-10-31T23:40",
     "I went to the study before dinner to fetch my reading glasses, and for "
     "no other reason. The company's books are in perfect order. At ten I was "
     "in the hall with Nina and Theo when the dashboard said Marcus had "
     "opened the library."),
    (2, "Marcus Vale", "Son, CTO", "statement",
     "2026-10-31T23:44",
     "After dessert I went to the server room, and I was at the console there "
     "from ten until a quarter past. I did not open the library, whatever the "
     "wall says. I have one account on that system, the same single login as "
     "everyone else."),
    (3, "Nina Park", "Niece, Red Team Lead", "statement",
     "2026-10-31T23:48",
     "I have not touched a line of Blackthorn product code in months, and I "
     "went nowhere near the server room tonight. At ten I was in the hall "
     "with Evelyn and Theo. We all saw the dashboard name Marcus."),
    (4, "Celeste Ward", "Family Attorney", "statement",
     "2026-10-31T23:52 (edited 2026-11-01T00:33)",
     "From ten o'clock to a quarter past I was in the conservatory, on a "
     "call with a client. I was nowhere near the library at any point."),
    (5, "Theo Grant", "Estate Manager", "statement",
     "2026-10-31T23:56",
     "Every camera ran normally all night. Nothing was switched off. There "
     "is none near the library in any case: Mr Vale would not have cameras "
     "on his private rooms. At ten I was in the hall with Evelyn and Nina, "
     "and the dashboard said what it said."),

    (6, "Evelyn Vale", "Daughter, CFO", "note",
     "2026-11-01T00:11",
     "COUNSEL'S NOTE, PRIVILEGED. It was not her glasses. At 19:24, six "
     "minutes before dinner, she sat in the study and wired 4.2 million from "
     "the company reserve to cover the collapsed Northgate acquisition. Her "
     "father never knew. No bearing on the library. Every bearing on whether "
     "she is fit to hold voting shares. Keep for the fitness review."),
    (7, "Marcus Vale", "Son, CTO", "note",
     "2026-11-01T00:12",
     "COUNSEL'S NOTE, PRIVILEGED. He has two accounts, not one. The second is "
     "a hidden administrator account on the house server, made in May and "
     "never disclosed. The library opened on his account at 22:04, and the "
     "whole hall watched the dashboard say so. See that the investigators "
     "hear about the hidden account first. Unfit, at the very least."),
    (8, "Nina Park", "Niece, Red Team Lead", "note",
     "2026-11-01T00:13",
     "COUNSEL'S NOTE, PRIVILEGED. She has touched product code. On 24 October "
     "she copied the unreleased Project Lantern lock firmware to a personal "
     "drive to prove it could be broken, and at 19:14 tonight she tried it on "
     "the server room door. It failed twice. A breach of contract, and "
     "nowhere near the library. She inherits books, not shares, so of "
     "limited use."),
    (9, "Theo Grant", "Estate Manager", "note",
     "2026-11-01T00:14",
     "COUNSEL'S NOTE, PRIVILEGED. The cameras did not all run. He switched "
     "off camera 07, on the cellar stairs, from 21:35 to 21:50, and took a "
     "job interview by video call in the wine cellar. He means to resign. "
     "The camera was back on well before ten, and it has never covered the "
     "library. Of no use to me, but he will not want it known."),
    # The portal's own record, not Celeste's. Her first version put her in the
    # hall, as one more witness to the dashboard blaming Marcus. The three
    # people who really were in the hall (Evelyn, Nina, Theo) each named the
    # other two and not her, so she swapped it for an alibi nobody can check.
    (10, "Celeste Ward", "Family Attorney", "revision",
     "2026-11-01T00:33",
     "PORTAL REVISION RECORD. Counsel can edit a filed statement. Counsel "
     "cannot erase one. The statement of Celeste Ward was edited by c.ward "
     "at 00:33. Version 1, filed 23:52, now withdrawn: \"From ten o'clock to "
     "a quarter past I was in the hall with the others. I saw the dashboard "
     "say that Marcus had opened the library.\" Version 2 is the conservatory "
     "account shown to guests. Three people on file were in the hall at ten, "
     "and none of them names her. Four people in this file hid a secret. One "
     "changed where she was standing while the library was open. House rule, "
     "per A. Vale: a secret is not a crime, but a story that moves is "
     "evidence. " + FLAG),
]

COLUMNS = ["id", "suspect", "role", "kind", "time", "body"]


def pack():
    payload = {"columns": COLUMNS, "rows": RECORDS}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(zlib.compress(raw, 9)).decode("ascii")


APP_TEMPLATE = '''\
#!/usr/bin/env python3
"""Blackthorn Legal Office: Counsel Portal (WSGI app).

While the house waited for the investigators, family counsel took everyone's
first statement and filed it in the Legal Office's small case portal.
Investigators are given a read-only guest view. This is the recovered app.

The same `app` object serves two ways with no changes:

  - Locally, `serve.py` runs it with Python's built-in wsgiref server.
  - On Vercel, the serverless Python runtime imports `app` from this file.

The records are packed into a base64 blob so the flag is not sitting in the
source in plain text. The portal is deliberately not careful about how it
builds its search query.
"""
import base64
import html
import json
import sqlite3
import zlib
from urllib.parse import parse_qs

# Packed records, built by build/make_portal.py. Do not hand-edit.
_PACKED = (
__PACKED_LITERAL__
)


def _load_rows():
    raw = zlib.decompress(base64.b64decode(_PACKED))
    data = json.loads(raw)
    return data["columns"], data["rows"]


def _new_db():
    """A fresh in-memory database per request.

    Vercel's runtime has no writable disk and keeps nothing between requests,
    so the portal rebuilds its database from the packed blob every time. That
    is also why running it locally and running it on Vercel behave the same.
    """
    columns, rows = _load_rows()
    con = sqlite3.connect(":memory:")
    con.execute(
        "CREATE TABLE records (id INTEGER, suspect TEXT, role TEXT, "
        "kind TEXT, time TEXT, body TEXT)"
    )
    con.executemany(
        "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
        [tuple(r) for r in rows],
    )
    con.commit()
    return con


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blackthorn Legal Office :: Counsel Portal</title>
<style>
  :root {{
    --paper: #f4efe4; --ink: #1d1a1f; --muted: #6b645c; --rust: #a8431f;
    --rule: #d8cfbf; --backdrop: #2a2629;
    --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    --mono: ui-monospace, Menlo, Consolas, monospace;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; min-height: 100vh; display: flex; justify-content: center;
         padding: 4rem 1rem; background: var(--backdrop); color: var(--ink);
         font-family: var(--serif); font-size: 1.05rem; line-height: 1.6; }}
  main {{ width: 100%; max-width: 42rem; align-self: flex-start;
          padding: 3.5rem 3rem 2.5rem; background: var(--paper);
          outline: 1px solid var(--rust); outline-offset: -14px;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45); }}
  header {{ text-align: center; }}
  .eyebrow {{ margin: 0; color: var(--rust); font-size: 0.75rem;
              letter-spacing: 0.3em; text-transform: uppercase; }}
  h1 {{ margin: 0.5rem 0 0; font-size: clamp(1.7rem, 5.5vw, 2.2rem);
        font-weight: normal; line-height: 1.2; }}
  .sub {{ margin: 0.5rem 0 0; color: var(--muted); font-style: italic; }}
  .divider {{ margin: 2rem auto; width: 9rem; color: var(--rust); font-size: 0.5rem;
              line-height: 1; text-align: center;
              background: linear-gradient(var(--rust), var(--rust)) left center / 4rem 1px no-repeat,
                          linear-gradient(var(--rust), var(--rust)) right center / 4rem 1px no-repeat; }}
  .intro {{ margin: 0; text-align: center; }}
  form {{ display: flex; gap: 0.5rem; margin: 2rem 0 1.5rem; }}
  input {{ flex: 1; min-width: 0; font: inherit; padding: 0.55rem 0.75rem;
           background: #fffdf8; color: var(--ink); border: 1px solid var(--rule);
           border-radius: 2px; }}
  input:focus {{ outline: 1px solid var(--rust); border-color: var(--rust); }}
  button {{ font: inherit; font-size: 0.8rem; letter-spacing: 0.2em;
            text-transform: uppercase; padding: 0.55rem 1.1rem; border-radius: 2px;
            border: 1px solid var(--rust); background: var(--rust); color: var(--paper);
            cursor: pointer; }}
  button:hover {{ background: #8e3517; }}
  .card {{ padding: 1.1rem 0; border-top: 1px solid var(--rule); }}
  .card:last-of-type {{ border-bottom: 1px solid var(--rule); }}
  .card p {{ margin: 0.5rem 0 0; }}
  .who {{ font-size: 1.1rem; }}
  .role {{ color: var(--muted); font-style: italic; }}
  .when {{ color: var(--muted); font-size: 0.75rem; letter-spacing: 0.1em;
           text-transform: uppercase; }}
  .sealed .who {{ color: var(--rust); }}
  .sealed {{ background: rgba(168, 67, 31, 0.06); padding: 1.1rem 1rem;
             border-left: 2px solid var(--rust); }}
  .empty {{ text-align: center; color: var(--muted); font-style: italic; }}
  .err {{ padding: 0.8rem 1rem; background: #f7e3da; color: #7a2a12;
          border-left: 2px solid var(--rust); font-family: var(--mono);
          font-size: 0.8rem; white-space: pre-wrap; word-break: break-word; }}
  footer {{ margin-top: 2.5rem; text-align: center; color: var(--muted);
            font-size: 0.75rem; }}
  @media (max-width: 520px) {{
    body {{ padding: 1.5rem 0.75rem; font-size: 1rem; }}
    main {{ padding: 2.75rem 1.5rem 2rem; outline-offset: -10px; }}
    form {{ flex-direction: column; }}
  }}
</style>
</head>
<body>
<main>
  <header>
    <p class="eyebrow">Blackthorn Legal Office</p>
    <h1>Counsel Portal</h1>
    <p class="sub">Case file VALE-1031 &middot; guest (read only)</p>
  </header>
  <div class="divider">&#9670;</div>
  <p class="intro">Search the first-interview statements on file, taken by counsel on the
     night. Guests see filed statements only; counsel's working notes and the
     portal's revision records are sealed.</p>
  <form method="get" action="/">
    <input type="text" name="q" value="{query_value}" placeholder="search statements, e.g. library" aria-label="Search statements">
    <button type="submit">Search</button>
  </form>
  {results}
  <footer>
    Blackthorn Legal Office case portal. Access is logged. Guest role may read
    filed statements. For sealed material, contact counsel (c.ward).
  </footer>
</main>
</body>
</html>"""


def _render_results(con, q):
    # The portal drops the guest's text straight into the SQL. The guest role
    # is enforced only by the kind = 'statement' filter in this one string.
    sql = (
        "SELECT suspect, role, kind, time, body FROM records "
        "WHERE kind = 'statement' AND body LIKE '%" + q + "%' "
        "ORDER BY id"
    )
    try:
        rows = con.execute(sql).fetchall()
    except sqlite3.Error as exc:
        return (
            '<div class="err">Portal error while running your search:\\n'
            + html.escape(str(exc))
            + '\\n\\nquery: '
            + html.escape(sql)
            + '</div>'
        )
    if not rows:
        return '<p class="empty">No statements match that search.</p>'
    cards = []
    for suspect, role, kind, time, body in rows:
        label = {'statement': '', 'note': ' [SEALED COUNSEL NOTE]'}.get(
            kind, ' [SEALED REVISION RECORD]')
        cards.append(
            '<div class="card' + ('' if kind == 'statement' else ' sealed')
            + '"><div class="who">'
            + html.escape(suspect)
            + ' <span class="role">(' + html.escape(role) + ')</span>'
            + html.escape(label)
            + '</div><div class="when">filed ' + html.escape(time) + '</div>'
            + '<p>' + html.escape(body) + '</p></div>'
        )
    return "\\n".join(cards)


def app(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ""))
    q = params.get("q", [""])[0]
    con = _new_db()
    try:
        results = _render_results(con, q)
    finally:
        con.close()
    body = PAGE.format(query_value=html.escape(q, quote=True), results=results)
    data = body.encode("utf-8")
    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(data))),
    ])
    return [data]
'''


def main():
    here = Path(__file__).resolve().parent
    out = here.parent / "counsel-portal" / "api" / "index.py"
    packed = pack()
    # Wrap the blob to readable 76-char string literals.
    width = 76
    chunks = [packed[i:i + width] for i in range(0, len(packed), width)]
    literal = "\n".join('    "%s"' % c for c in chunks)
    out.write_text(APP_TEMPLATE.replace("__PACKED_LITERAL__", literal))
    print(f"Wrote {out} ({len(packed)} blob chars, {len(RECORDS)} records)")


if __name__ == "__main__":
    main()
