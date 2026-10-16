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
            '<div class="err">Portal error while running your search:\n'
            + html.escape(str(exc))
            + '\n\nquery: '
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
