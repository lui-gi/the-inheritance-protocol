# Introduction: Welcome to Blackthorn House

It is Halloween at Blackthorn House, and the host has made the evening awkward by dying.

Adrian Vale, founder of Blackthorn Security, was found dead in his library at 10:17 PM. The house went into lockdown, the guests went into the drawing room, and every one of them has since explained, in detail, why it could not have been them.

You are an outside digital investigator. Nobody here can charm you, because you are only going to talk to their devices. The house logs everything: its doors, its server, its archive, even the portrait in the hall. Work through eight tasks, collect eight flags, and name the person who killed Adrian Vale.

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

## House rule: AI is a guide, not the investigator

You may use an AI assistant to learn a tool or explain a concept, the way you would use any tutorial. You must not hand the challenge files to an AI and ask it to solve them. Every question in this room can be answered with the toolkit above, and the point is to do the forensics yourself.

## Questions

1. I have my toolkit ready.

2. I have read the house rule on AI, and I will do my own investigating.
