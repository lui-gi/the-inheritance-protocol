# The Inheritance Protocol

A 75-minute Halloween murder-mystery CTF for GWC x Cybersecurity Club x TryHackMe.

Adrian Vale, founder of Blackthorn Security, is found dead in his library at 10:17 PM on Halloween. Players are outside digital investigators at Blackthorn House. They work through eight tasks, collect eight flags, and identify who killed him.

**Spoiler warning:** this repository is for organizers. It contains the full solution, every flag, and the answer to the mystery. Do not share it with players.

## How the room works

The CTF runs as a custom TryHackMe room with no VM. Each flag is its own task with its own text, download, and answer field. Most artifacts are files the player downloads and examines on their own machine, so nothing depends on a machine IP.

Three tasks use something hosted on Vercel, which players open by URL: the Invitation's portal snapshot (https://blackthorn-portal.vercel.app), and the Counsel Portal (https://blackthorn-counsel-portal.vercel.app) and Last Testament (https://blackthorn-case-board.vercel.app) web apps. Each also runs locally with its bundled `serve.py` as a fallback.

Flags use the format `THM{UPPER_SNAKE_CASE}`.

## A note on AI (room rule)

Players may use an AI assistant to learn a tool or explain a concept, the way they would use any tutorial. They must not hand our challenge files to an AI and ask it to solve them. Every question is solvable with the toolset introduced at the start of the room, and the point is to do the forensics yourself. Use AI as a guide, not as the investigator.

This is its own room task (`challenges/00d-ai-disclosure/`): players must answer `I understand` to complete it, before the investigation starts.

## Setup tasks

Four short tasks open the room. Each has its own folder, named so it sorts before the investigation tasks. None has a download.

| Room task | Task | Folder | Answer |
| :-- | :-- | :-- | :-- |
| 0 | Welcome to Blackthorn House | `challenges/00a-welcome/` | no answer needed |
| 1 | New to This? TryHackMe and CTFs | `challenges/00b-tryhackme/` | `THM{UPPER_SNAKE_CASE}` |
| 2 | Assemble Your Investigators | `challenges/00c-team/` | no answer needed |
| 3 | House Rule: AI Is a Guide | `challenges/00d-ai-disclosure/` | `I understand` |

The team task assumes the room is team-based. Turn that on in the room's **General Settings** tab when creating it, and tell players the team size limit on the night (TryHackMe allows up to 20).

## Tasks

| # | Task | Folder | What the player downloads |
| :-- | :-- | :-- | :-- |
| 1 | The Invitation | `challenges/01-invitation/` | `invitation.png` (the portal snapshot is hosted) |
| 2 | Portrait in the Hall | `challenges/02-portrait/` | `portrait.jpg` |
| 3 | The Smart Lock | `challenges/03-smart-lock/` | `lock-controller.log` and `device-record.zip` |
| 4 | Ghost Admin | `challenges/04-ghost-admin/` | the `blackthorn-server/` snapshot |
| 5 | The Two Wills | `challenges/05-two-wills/` | the two will PDFs, `archive-entry.txt`, and `replacement-record.zip` |
| 6 | Counsel Portal | `challenges/06-counsel-portal/` | nothing: the hosted Counsel Portal |
| 7 | Commit History | `challenges/07-commit-history/` | the `blackthorn-dashboard/` Git repository, `README.txt`, and `signing-record.zip` |
| 8 | The Last Testament | `challenges/08-last-testament/` | nothing: the hosted case board |

The tasks build on each other: evidence found in earlier tasks is needed in later ones, and the Last Testament task asks for answers from the Smart Lock, the Ghost Admin, the Two Wills, and the Commit History tasks.

## Repository layout

```
Halloween_Cybersecurity_Murder_Mystery_Master_3_Storylines.docx.md   design document
canon/canon.md                                                       shared facts every task must agree with
challenges/NN-name/
    task.md        player-facing task text for the TryHackMe room
    build/         script that generates the task's artifacts
    organizer/     solution and plaintext copies of sealed files
    ...            the artifacts themselves
```

Only the artifacts and `task.md` go to players. The design document, `canon/`, every `build/` folder, and every `organizer/` folder stay with the organizers.

## Rebuilding the artifacts

Each task except the Invitation has one build script that regenerates its artifacts. The Invitation's `invitation.png` is a hand-made image with no build step. The builds are reproducible, so rerunning one without changing it gives the same output.

```
python3 challenges/02-portrait/build/make_portrait.py
python3 challenges/03-smart-lock/build/make_logs.py
python3 challenges/04-ghost-admin/build/make_server.py
python3 challenges/05-two-wills/build/make_wills.py
python3 challenges/06-counsel-portal/build/make_portal.py
python3 challenges/07-commit-history/build/make_repo.py
python3 challenges/08-last-testament/build/make_board.py
```

Requirements:

- The Smart Lock, the Ghost Admin, the Two Wills, the Counsel Portal, and the Last Testament tasks need only Python 3 and its standard library.
- The Portrait in the Hall task needs the packages in its `build/requirements.txt`.
- The Commit History task needs `git` and `ssh-keygen`.

The Commit History task's `blackthorn-dashboard/` folder holds its own `.git`, so this repository ignores it. Run `make_repo.py` to recreate it after cloning and before publishing.

## Hosting

Each hosted folder is linked to its own Vercel project (the `.vercel/` link is gitignored). To redeploy after a change:

```
cd challenges/01-invitation/blackthorn-portal/portal.blackthorn.thm   # project blackthorn-portal
cd challenges/06-counsel-portal/counsel-portal                        # project blackthorn-counsel-portal
cd challenges/08-last-testament/case-board                            # project blackthorn-case-board

npx vercel deploy --prod
```

On a fresh clone, link first with `npx vercel link --project <name>`. The two apps' `.vercelignore` keeps `serve.py` and `README.txt` off the hosted site.

## Running the web apps locally (fallback)

```
cd challenges/01-invitation/blackthorn-portal      # or
cd challenges/06-counsel-portal/counsel-portal     # or
cd challenges/08-last-testament/case-board

python3 serve.py          # http://localhost:8000/
python3 serve.py 8080     # pick another port
```

Each needs Python 3.7 or newer and nothing else. The `README.txt` in each folder is the player-facing version of these instructions.

## Publishing a task

1. Rebuild the task's artifacts with its build script.
2. For a hosted task (6 and 8, and task 1's portal), redeploy to Vercel (see Hosting) and check the live URL. Do not upload the app folder as a task file.
3. Zip the player-facing files listed in the table above, if any. Leave out `build/`, `organizer/`, and `task.md`.
4. Upload the zip as the task file in the TryHackMe room, paste in the text from `task.md`, and set the flag as the task answer.

## Changing a task

- Read the design document and `canon/canon.md` first. Names, timestamps, device IDs, hashes, and keys are shared between tasks.
- Edit the build script, not the generated files, then rerun it.
- Update `canon/canon.md` whenever a task adds or changes a shared fact. In the Two Wills task, changing the wording of either will changes its hash, which also changes the zip password and the answer the Last Testament task expects.
- Keep organizer notes and solutions out of anything distributed to players.
