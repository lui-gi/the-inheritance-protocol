# Task 6: Family Secrets (ORGANIZER ONLY)

Flag: `THM{SECRETS_ARE_NOT_MURDER}`

Checkpoint answer (question 1): `5`

Target solve time: about 8 minutes. Skills: reading a web page, spotting that user input reaches a SQL query, a single classic injection payload. No VM is involved: the portal runs on the player's machine, and the same app can also be hosted on Vercel.

## The story beat

Every suspect lied during their first interview, but only Celeste's lie touches the library timeline fixed by Tasks 3 to 5 (her tablet `BH-TAB-0417` opened the library at 22:04:11, Adrian was found at 22:17). The flag is the point of the task in words: secrets are not murder.

The portal is the Legal Office case file. Celeste, as family counsel, took all five statements herself between 23:40 and 23:56, while the house waited for the investigators (whose first action is at 00:42). That is why the interviews sit in the prime suspect's own system. Guests see the filed statements. Two kinds of record are sealed:

- Four counsel's notes, written by Celeste from 00:11 to 00:14. They are her private file on the other four: the real secret behind each lie, and what use it is to her. The replacement will's Article 4 (Task 5) lets the Trustee alone judge an heir "unfit", and these notes are her ammunition. Her note on Marcus says to steer the investigators to his hidden account first, which is exactly what Adrian's sealed findings in Task 4 predicted somebody would do.
- One revision record, written by the portal and not by her. At 23:52 she filed a statement placing herself in the hall, as one more witness to the dashboard blaming Marcus. Evelyn, Nina, and Theo really were in the hall, and each of their statements names the other two and not her. At 00:33 she replaced her statement with an alibi nobody can check (alone in the conservatory, on a call). The portal kept both versions. The flag is on this record, in the same house-system voice as the hub and archive warnings in Tasks 3, 5, and 7.

The three hall witnesses here are the "three people" Task 7's text mentions.

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

The guest role is enforced only by `kind = 'statement'` inside that one string, so an injection that neutralises the `WHERE` clause returns the sealed `kind = 'note'` and `kind = 'revision'` rows too. On any `sqlite3.Error` the page prints the exception and the full attempted query, which hands the player the structure they need.

## Records

Ten rows: five filed statements, four sealed counsel's notes, and one sealed revision record. Guest view shows the five statements (no flag). Celeste's statement is the only one whose filing time reads "(edited 2026-11-01T00:33)". The five sealed rows:

| Suspect | Lie in the statement | Sealed record | Touches library? |
| :---- | :---- | :---- | :---- |
| Evelyn Vale | Went to the study only for her glasses, books in order | Note: wired 4.2M from the study at 19:24 to cover the Northgate acquisition (her phone opened the study at 19:22:15 in Task 3) | No |
| Marcus Vale | Has one account | Note: hidden second admin account since May. Celeste wants the investigators pointed at it | No (this is Flag 4, and he was at the console from 22:03 to 22:15) |
| Nina Park | No product code in months, nowhere near the server room | Note: copied the Project Lantern lock firmware on 24 October and tried it on the server room door at 19:14 (the two denials in Task 3) | No |
| Theo Grant | Every camera ran all night | Note: cut camera 07 on the cellar stairs from 21:35 to 21:50 for a job interview by video call in the wine cellar (his badge opened it at 21:38:19 in Task 3) | No |
| Celeste Ward | In the conservatory on a call from 22:00 to 22:15 | Revision record: her first version said she was in the hall watching the dashboard. Withdrawn at 00:33 | Yes. Flag is here. |

Every secret time sits outside dinner (19:30 to dessert at 21:30) or is pinned to a lock-log line players have already seen, and none is near the library. Those ties are flavour: nothing in the solve needs the Task 3 log open.

No camera covers the library. Theo's statement says so (Adrian would not have cameras on his private rooms) and Celeste's note on him agrees, which closes the question of why no footage shows who went in at 22:04.

Celeste's account of 22:00 to 22:15 is the only one that changed, and both versions put her somewhere other than the library door, where Task 3 put her tablet.

## Intended solution

1. Unzip, run `python3 serve.py`, open `http://localhost:8000/`.
2. Read the five statements. Each contains a lie; four are plainly not about the library. Celeste's is the only one marked as edited.
3. Try to reach the sealed records. The guest view filters them out, so search normally fails.
4. Put a single quote `'` in the search box. The portal shows a SQL error and the full query, revealing the concatenation.
5. Search `' OR 1=1 --` (the trailing space after `--` matters in SQLite). The `WHERE` clause is neutralised and all ten rows return, including the five sealed rows: four marked `[SEALED COUNSEL NOTE]` and one marked `[SEALED REVISION RECORD]`.
6. Checkpoint: five sealed records (four notes and one revision record). Answer `5`.
7. Read the revision record for Celeste's statement. It is the only sealed record about where someone was while the library was open, and it carries the flag `THM{SECRETS_ARE_NOT_MURDER}`.

Other payloads that work: `' OR kind<>'statement' -- `, `%' OR 1=1 -- `, `' UNION SELECT suspect,role,kind,time,body FROM records -- `.

## Hosting note

The app is stdlib only, so no `requirements.txt` is needed. Deploying `counsel-portal/` to Vercel serves the portal from `api/index.py` with `vercel.json` routing every path to it. Not hosted yet. When it is, the task text's `http://localhost:8000/` can be swapped for the hosted URL, and the local download can still ship as a fallback.

## What this proves and does not prove

It proves every suspect had something to hide and that only Celeste's secret intersects the library. It does not prove she is the killer on its own: the device (Flag 3), the will (Flag 5), and the commit (Flag 7) do that. Do not tell players the sealed records prove murder; the flag text says the opposite.
