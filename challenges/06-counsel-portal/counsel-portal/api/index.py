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
    "eNqNVttu2zgQ/ZWBXnYXUAXbSXrxWzZx2wC5FLHbxaItCpoaW6wlUiWpeIWi/75nKCebdIO4LzZF"
    "kTNz5pyZ0fdMu7prbMimHzNTZnkWutCyjlh5VzP+NsbKfjSNPC1d2Wef5eVW7nwc59nshuve0geV"
    "jp+qbl1F9jmdvL4Se1FFbtiKxclo8vzZePTsYLyYHEwPR9g6o60KZCzFiinEruxpa2KVHr91ysNS"
    "3dPKrDvPIe1uK8RFfMPW2HVBf9ZKb2LlvKU5686b2FMFkxYnPC2ZrVhfcoQlCpVquaDjsEmmVFea"
    "6HwogOjjJM8ulNdduEUydxYgFntAHP4PBHvx7J1rSNU1WYN80Ia5RbzpROW6wORsbSyCOUO4N/KI"
    "eLR2nY1Y45yKFPoAt/lgVjX4gQmAr90azuBSMPZyk+vACcVBnl0aq+id8ptM1qw5p2suacGqoXNW"
    "5dN4XiY80ADiEL+7RJPr4i3CtfIl27vIrcNJ1+kKThQJKHKr+7y03pWdjqRdyWKjcTZWoaC/XUda"
    "WcJNPRDiuXVBKDE8kHKYZydcM9JAf8ErYnutGgNFHEecstw/CeZoIhc8iIiQgftN104cOYS50xa1"
    "KkR6wJ92VihUsN/nQoVCkOAxyRLr2sBVsbtj3bZijxyw8ul2bZZe+Z7AnrI9tc7gsCA5yrNFxY7e"
    "eJUinaWw6UJZtWb/NIznWaoymNVQgVcEG3DtG8TV/yeyIah6Ax4klBVzGajpA9criUdyoGx5r4gG"
    "IQqOb51h3L90sRKyZSsAcOLUrVYJwfN9pQ4h8F3w42ej8WI0mo7H2Dq5en85n53/NqfLq8Usp3fX"
    "Zx/OzmdvZqcF7Ww27ga+DosJgd/aIO+rRFxSRaopIU47qa2BprpWbcCdS+djtZZkKg0c0A9uF7QQ"
    "mAbc6BrkiDYjjV9Nj0a54PYBPWHl8PoeawimWSrvVZBCy5Oymw5i9ykBL57oEI9jn+zBvjO34RZy"
    "QeeA9hBn2RhrQvQiwYc94Zay28agPQN3uasoUmuXGB56X2kCBI8MFah/VSOvQeyjEiGUOEi+hApK"
    "NM1dZxrAIm22dNskh/v4X/5Sb3k8Ewd7MpEMa9eanXg761H3Svh9591XTCQ6R+Hw0E6ii33LQyW3"
    "7IOzwFd6A5GA5cloejCWlziJHTNg5X/a2pmolrVMAFoidbqSToWkINc6Dnw/kMNPCXi1r4Yfx364"
    "B3uyqdFfK5TyVt1V+ejFUAOT8XQyEjxYHKVFZdBJAR2IJYCGOaayHVoUolqt5BlRWd0PpSDdIOVh"
    "ib6MCYLXjxXAT4jHo19owI+iPtjH+PHF7PJ0dkrzxfFihvUix5ivEeQSCYDk0bbod11s4fUPYTXZ"
    "LOjKGww/0C2DRijbJtilV1s7pU8yuyK3Leyg87oHPflrh16vVtL2pRfiLRR2MySgVaIjQkLoGEJS"
    "tviUQdotppjk7faT5P5wuCtNtYTMCnorHxiMksSgHD5VMOL7NNjTNK9RmndT5jamXVkPHwmDZxSu"
    "1Ozi7cX3+ezkeraYfzm+nn1BBr9cvL8+nV3/yD5//vEviFwvZw=="
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
        label = '' if kind == 'statement' else ' [SEALED COUNSEL NOTE]'
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
