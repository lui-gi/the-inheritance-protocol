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
    "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"
    "dHH59Wg+/QpR+Hr2Yf5mOv/R+/Llx3+ZpPkR"
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
  <p>Search the first-interview statements on file, taken by counsel on the
     night. Guests see filed statements only; counsel's working notes and the
     portal's revision records are sealed.</p>
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
            '<div class="err">Portal error while running your search:\n'
            + html.escape(str(exc))
            + '\n\nquery: '
            + html.escape(sql)
            + '</div>'
        )
    if not rows:
        return '<p><em>No statements match that search.</em></p>'
    cards = []
    for suspect, role, kind, time, body in rows:
        label = {'statement': '', 'note': ' [SEALED COUNSEL NOTE]'}.get(
            kind, ' [SEALED REVISION RECORD]')
        cards.append(
            '<div class="card"><div class="who">'
            + html.escape(suspect)
            + ' <span class="role">(' + html.escape(role) + ')</span>'
            + html.escape(label)
            + '</div><div class="when">filed ' + html.escape(time) + '</div>'
            + '<p>' + html.escape(body) + '</p></div>'
        )
    return "\n".join(cards)


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
