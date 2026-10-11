#!/usr/bin/env python3
"""Build the Counsel Portal app module for Task 6.

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

# Each suspect has one guest-visible statement (which contains a lie) and one
# sealed counsel's note (which records the real secret behind the lie). Only
# Celeste's secret touches the library timeline fixed by Tasks 3 to 5: her
# tablet opened the library at 22:04 and Adrian was found at 22:17.
#
# kind="statement" -> shown in the guest view.
# kind="note"      -> sealed; only reachable by breaking the search.
RECORDS = [
    # id, suspect, role, kind, time (as filed), body
    (1, "Evelyn Vale", "Daughter, CFO", "statement",
     "2026-10-31T23:40",
     "I was in the study with the quarterly figures the whole evening. "
     "Blackthorn Security has never been in better shape. Ask the auditors."),
    (2, "Marcus Vale", "Son, CTO", "statement",
     "2026-10-31T23:44",
     "I was in the server room all night keeping the house online. I have "
     "one account on that system, the same single login as everyone else."),
    (3, "Nina Park", "Niece, Red Team Lead", "statement",
     "2026-10-31T23:48",
     "I spent the evening out in the garden. I have not touched a line of "
     "Blackthorn product code in months. You can check the repositories."),
    (4, "Celeste Ward", "Family Attorney", "statement",
     "2026-10-31T23:52",
     "From ten o'clock to a quarter past I was in the conservatory, on a "
     "call with a client. I was nowhere near the library at any point."),
    (5, "Theo Grant", "Estate Manager", "statement",
     "2026-10-31T23:56",
     "Every camera ran normally all night. I walked the feeds myself at ten "
     "and the whole house was quiet. Nothing was switched off."),

    (6, "Evelyn Vale", "Daughter, CFO", "note",
     "2026-11-01T00:11",
     "COUNSEL'S NOTE, PRIVILEGED. Evelyn moved 4.2 million from the reserve "
     "to cover the collapsed Northgate acquisition. The wire cleared at "
     "19:50, hours before the library. Embarrassing, not murder."),
    (7, "Marcus Vale", "Son, CTO", "note",
     "2026-11-01T00:12",
     "COUNSEL'S NOTE, PRIVILEGED. Marcus kept a second administrator account "
     "on the house system, created months ago and never disclosed. Real "
     "misconduct. It was idle during the murder window. Not murder."),
    (8, "Nina Park", "Niece, Red Team Lead", "note",
     "2026-11-01T00:13",
     "COUNSEL'S NOTE, PRIVILEGED. Nina copied the unreleased Project Lantern "
     "prototype to a personal drive at 20:31 to prove it was exploitable. "
     "A breach of contract, not the library. Not murder."),
    (9, "Theo Grant", "Estate Manager", "note",
     "2026-11-01T00:14",
     "COUNSEL'S NOTE, PRIVILEGED. Theo cut hallway camera 07 from 21:20 to "
     "21:50 to hide a private meeting with a staffing agency. The feed was "
     "back long before the library. Not murder."),
    # Celeste's own note is an amendment she filed to her own statement. The
    # original line put her in the library just after ten; she replaced it.
    (10, "Celeste Ward", "Family Attorney", "note",
     "2026-11-01T00:33",
     "COUNSEL'S NOTE, PRIVILEGED. AMENDED STATEMENT, filed by counsel "
     "(c.ward) at 00:33. Original line, now withdrawn: \"I stepped into the "
     "library just after ten to leave the papers for Adrian.\" Replaced with "
     "the conservatory account above. Her secret is the only one that lands "
     "in the library on the night Adrian died. " + FLAG),
]

COLUMNS = ["id", "suspect", "role", "kind", "time", "body"]


def pack():
    payload = {"columns": COLUMNS, "rows": RECORDS}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(zlib.compress(raw, 9)).decode("ascii")


APP_TEMPLATE = '''\
#!/usr/bin/env python3
"""Blackthorn Legal Office: Counsel Portal (WSGI app).

The Legal Office kept the first-interview statements in a small case portal.
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
  :root {{ color-scheme: light dark; }}
  body {{ font-family: Georgia, "Times New Roman", serif; max-width: 760px;
         margin: 2.5rem auto; padding: 0 1rem; line-height: 1.5;
         background: #faf7f2; color: #1c1a17; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #15130f; color: #e8e2d6; }}
    .card {{ background: #1e1b16; border-color: #3a342a; }}
    input {{ background: #15130f; color: #e8e2d6; border-color: #3a342a; }}
    .err {{ background: #2a1512; color: #f1c0b4; }}
  }}
  h1 {{ font-size: 1.5rem; margin-bottom: 0.1rem; }}
  .sub {{ color: #8a8275; font-style: italic; margin-top: 0; }}
  form {{ margin: 1.5rem 0; }}
  input {{ font: inherit; padding: 0.45rem 0.6rem; width: 70%;
           border: 1px solid #c9c0b0; border-radius: 4px; }}
  button {{ font: inherit; padding: 0.45rem 0.9rem; border-radius: 4px;
            border: 1px solid #7a2e2e; background: #7a2e2e; color: #fff;
            cursor: pointer; }}
  .card {{ border: 1px solid #ddd3c2; border-radius: 6px; padding: 0.8rem 1rem;
           margin: 0.8rem 0; background: #fff; }}
  .who {{ font-weight: bold; }}
  .role {{ color: #8a8275; font-weight: normal; font-style: italic; }}
  .when {{ color: #8a8275; font-size: 0.85rem; }}
  .err {{ background: #fdecea; color: #7a2e2e; padding: 0.7rem 1rem;
          border-radius: 6px; font-family: ui-monospace, monospace;
          font-size: 0.85rem; white-space: pre-wrap; }}
  footer {{ color: #8a8275; font-size: 0.8rem; margin-top: 2.5rem;
            border-top: 1px solid #ddd3c2; padding-top: 0.8rem; }}
</style>
</head>
<body>
  <h1>Blackthorn Legal Office</h1>
  <p class="sub">Counsel Portal &mdash; case file VALE-1031 &mdash; guest (read only)</p>
  <p>Search the first-interview statements on file. Guests see filed
     statements only; counsel's working notes are sealed.</p>
  <form method="get" action="/">
    <input type="text" name="q" value="{query_value}" placeholder="search statements, e.g. library">
    <button type="submit">Search</button>
  </form>
  {results}
  <footer>
    Blackthorn Legal Office case portal. Access is logged. Guest role may read
    filed statements. For sealed material, contact counsel (c.ward).
  </footer>
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
        return '<p><em>No statements match that search.</em></p>'
    cards = []
    for suspect, role, kind, time, body in rows:
        label = '' if kind == 'statement' else ' [SEALED COUNSEL NOTE]'
        cards.append(
            '<div class="card"><div class="who">'
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
