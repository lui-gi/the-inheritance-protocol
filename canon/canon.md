# Canon (ORGANIZER ONLY)

Shared facts that every task must agree with. Never distribute this file to players.
Add to it whenever a task introduces a new name, timestamp, device ID, hash, or key.

## Conventions

- Timezone: America/New_York. Halloween 2026 falls on a Saturday and is still on daylight time, so every timestamp uses the offset `-04:00`.
- Timestamp format in artifacts: ISO 8601 with offset, for example `2026-10-31T22:17:00-04:00`.
- Account names: first initial, dot, surname (`a.vale`, `m.vale`, `e.vale`, `n.park`, `c.ward`, `t.grant`).
- House portal hostname (offline in the story): `portal.blackthorn.thm`. The room has no VM. Players get a nightly portal snapshot as a folder named after the hostname, and serve it locally with the bundled `serve.py` (default `http://localhost:8000/`).

## Timeline

| When | What | Introduced by |
| :---- | :---- | :---- |
| 2026-10-16T14:05:32-04:00 | Guest list revision 1 saved by `a.vale`: Evelyn, Marcus, Nina, Theo. | Task 1 |
| 2026-10-17 | Invitations printed. The card reads "Printed 17 October 2026". | Task 1 |
| 2026-10-28T23:41:07-04:00 | Guest list revision 2 saved by `a.vale`: Celeste Ward added. Invitations are not reprinted. | Task 1 |
| 2026-10-31T03:00:00-04:00 | Nightly portal snapshot taken. This is the copy players receive. | Task 1 |
| 2026-10-31T19:00:00-04:00 | Guests arrive, cocktails in the hall. | Task 1 |
| 2026-10-31T19:30:00-04:00 | Dinner is served. | Task 1 |
| 2026-10-31T21:30:00-04:00 | Dessert. Adrian says: "By midnight, none of you will own what you think you own." | Design doc |
| 2026-10-31T22:17:00-04:00 | Adrian Vale is found dead in the library. | Design doc |
| 2026-11-01T00:00:00-04:00 | Celeste's trustee authority was due to be revoked. | Design doc (Flag 8) |
| 2026-11-01T00:42:00-04:00 | Investigators scan the invitation found in the library. | Task 1 |

## Task 1 facts

- Event page path: `/rsvp/hallows-eve-1031/` (in `task1-portal.zip`: `blackthorn-portal/portal.blackthorn.thm/rsvp/hallows-eve-1031/index.html`, served locally at `http://localhost:8000/rsvp/hallows-eve-1031/`)
- Decoy event pages with no clues: `founders-day-0606`, `midsummer-0620`, `board-retreat-0912`.
- QR payload: `http://portal.blackthorn.thm/rsvp/hallows-eve-1031/`
- Printed guest list (four): Evelyn Vale, Marcus Vale, Nina Park, Theo Grant.
- Live guest list (five): the four above plus Celeste Ward.
- Why Celeste was added (organizer reasoning): Adrian wanted her in the room when he revoked her authority. The player-facing note only says counsel must be present for the paperwork.
- Flag: `THM{THE_GUEST_LIST_CHANGED}`
