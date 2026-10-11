# Task 6: Family Secrets (ORGANIZER ONLY)

Flag: `THM{SECRETS_ARE_NOT_MURDER}`

Checkpoint answer (question 1): `5`

Target solve time: about 8 minutes. Skills: reading a web page, spotting that user input reaches a SQL query, a single classic injection payload. No VM is involved: the portal runs on the player's machine, and the same app can also be hosted on Vercel.

## The story beat

Every suspect lied during their first interview, but only Celeste's lie touches the library timeline fixed by Tasks 3 to 5 (her tablet `BH-TAB-0417` opened the library at 22:04:11, Adrian was found at 22:17). The portal is the Legal Office case file. Guests see the filed statements; counsel's sealed notes hold the real secrets. The flag is the point of the task in words: secrets are not murder.

## How the artifacts are built

One download, `counsel-portal/`, built by `build/make_portal.py`. The records are the single source of truth and live in that script in plain, readable form. Running the script packs them into a base64 + zlib blob and writes `counsel-portal/api/index.py`. The packing is only so a player cannot `grep` the flag out of the source: it is not security, and it is not meant to be.

```
counsel-portal/
  README.txt      player instructions, Windows + troubleshooting
  serve.py        local runner (stdlib wsgiref, no installs)
  vercel.json     rewrites every path to /api/index for hosting
  api/index.py    the WSGI app, generated; holds the packed records
```

`serve.py` and Vercel both import the same `app` object from `api/index.py`, so local and hosted behave identically. The database is a fresh in-memory SQLite built from the blob on every request, which is what Vercel's read-only, stateless runtime needs.

To rebuild after editing records: `python3 challenges/06-counsel-portal/build/make_portal.py`.

## The vulnerability

`api/index.py` builds the search query by string concatenation:

```python
sql = ("SELECT suspect, role, kind, time, body FROM records "
       "WHERE kind = 'statement' AND body LIKE '%" + q + "%' "
       "ORDER BY id")
```

The guest role is enforced only by `kind = 'statement'` inside that one string, so an injection that neutralises the `WHERE` clause returns the sealed `kind = 'note'` rows too. On any `sqlite3.Error` the page prints the exception and the full attempted query, which hands the player the structure they need.

## Records

Ten rows: one filed statement and one sealed note per suspect. Guest view shows the five statements (no flag). The five notes:

| Suspect | Secret | Touches library? |
| :---- | :---- | :---- |
| Evelyn Vale | Moved 4.2M to cover the Northgate acquisition, wire at 19:50 | No |
| Marcus Vale | Undisclosed second admin account, idle during the window | No (this is Flag 4) |
| Nina Park | Copied the Project Lantern prototype at 20:31 | No |
| Theo Grant | Cut hallway camera 07 from 21:20 to 21:50 | No |
| Celeste Ward | Amended statement: withdrew "stepped into the library just after ten" | Yes. Flag is here. |

Celeste's note is an amendment she filed to her own statement at 00:33, withdrawing the library line and replacing it with the conservatory alibi. It is the only secret that lands in the library on the night, and the flag sits in it.

## Intended solution

1. Unzip, run `python3 serve.py`, open `http://localhost:8000/`.
2. Read the five statements. Each contains a lie; four are plainly not about the library.
3. Try to reach the sealed notes. The guest view filters them out, so search normally fails.
4. Put a single quote `'` in the search box. The portal shows a SQL error and the full query, revealing the concatenation.
5. Search `' OR 1=1 --` (the trailing space after `--` matters in SQLite). The `WHERE` clause is neutralised and all ten rows return, including the five sealed notes, each marked `[SEALED COUNSEL NOTE]`.
6. Checkpoint: five sealed notes. Answer `5`.
7. Read Celeste's note. It is the only secret in the library timeline, and it carries the flag `THM{SECRETS_ARE_NOT_MURDER}`.

Other payloads that work: `' OR kind='note' -- `, `%' OR 1=1 -- `, `' UNION SELECT suspect,role,kind,time,body FROM records -- `.

## Hosting note

The app is stdlib only, so no `requirements.txt` is needed. Deploying `counsel-portal/` to Vercel serves the portal from `api/index.py` with `vercel.json` routing every path to it. Not hosted yet. When it is, the task text's `http://localhost:8000/` can be swapped for the hosted URL, and the local download can still ship as a fallback.

## What this proves and does not prove

It proves every suspect had something to hide and that only Celeste's secret intersects the library. It does not prove she is the killer on its own: the device (Flag 3), the will (Flag 5), and the commit (Flag 7) do that. Do not tell players the sealed notes prove murder; the flag text says the opposite.
