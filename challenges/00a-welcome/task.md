# Introduction: Welcome to Blackthorn House

It is Halloween at Blackthorn House, and the host has made the evening awkward by dying.

Adrian Vale, founder of Blackthorn Security, was found dead in his library at 10:17 PM. The house went into lockdown, the guests went into the drawing room, and every one of them has since explained, in detail, why it could not have been them.

You are an outside digital investigator. Nobody here can charm you, because you are only going to talk to their devices. The house logs everything: its doors, its server, its archive, even the portrait in the hall. Work through eight investigation tasks, collect eight flags, and name the person who killed Adrian Vale.

## How this room works

- There is no machine to start. Every task comes with a download that you examine on your own computer or on the AttackBox.
- The tasks build on each other. Keep notes as you go: device IDs, dates, hashes, and names found early are needed later, and the last task asks for several of them.
- Every flag looks like `THM{UPPER_SNAKE_CASE}`. Some tasks ask a checkpoint question or two before the flag.
- Three tasks include a small website that runs on your machine with one command. Each comes with a README that covers Windows and troubleshooting.

## Your toolkit

Nothing here needs a paid tool or anything exotic. Before you begin, check that you have:

- A terminal, and Python 3 (`python3 --version`)
- A web browser, including its developer tools (F12)
- A text editor, plus `grep` or any other way to search inside files
- A QR code reader. The camera on your phone counts.
- `exiftool`, or any EXIF metadata viewer
- A Base64 decoder, such as `base64 -d` or CyberChef
- Something that opens password-protected zips: `unzip`, 7-Zip, or your file manager
- A SHA-256 tool: `sha256sum`, `shasum -a 256`, or `certutil` on Windows
- Git (`git --version`)

## Prefer not to install anything? Use the AttackBox

If setting up tools on your own computer sounds like more trouble than the murder, you do not have to. TryHackMe provides the AttackBox: a ready-made Linux machine that runs in the cloud and appears inside your browser, next to the room. It is a full desktop with a terminal, a web browser, and the usual security tools already installed, so everything in the toolkit above should be there waiting for you.

To use it:

- Click the blue **Start AttackBox** button at the top of the room. It takes a minute or two to boot, then opens in a split view beside the tasks.
- Open this room in the browser inside the AttackBox and download each task file there, so the files land on the machine where the tools are.
- Open a terminal on the AttackBox desktop and work exactly as the tasks describe. The Linux commands in each task are the ones to use.
- For the QR code in The Invitation, your phone's camera pointed at the screen works fine.

Two things to know. Free accounts get a limited amount of AttackBox time per day, so start it when you are ready to work, not before. And if a tool ever turns out to be missing, tell an organizer: every task can also be done on your own computer.

## Questions

1. I have my toolkit ready.
