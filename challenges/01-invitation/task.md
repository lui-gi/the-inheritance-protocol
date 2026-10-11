# Task 1: The Invitation

Welcome to Blackthorn House, investigator. Mind the cobwebs. Some of them are decorative.

Adrian Vale's dinner invitations were printed on very expensive card stock, which is how we know he meant business. One was recovered from the library floor, and a scan of it is the first file attached to this task.

The invitation carries a QR code that pointed guests to a private event page on the house portal. The mansion's network went dark during the lockdown, so that address no longer resolves. Fortunately, the house takes a snapshot of its own portal every night, and we recovered the most recent one. That is the second file, and you can run it on your own machine.

This task has two downloads:

- `invitation.png`, the scanned invitation
- `task1-portal.zip`, the portal snapshot, with a script that serves it locally and a README that explains how

Unzip the portal, open a terminal in the `blackthorn-portal` folder, and run `python3 serve.py`. The portal will come up at `http://localhost:8000/`. The README covers Windows and troubleshooting.

The portal's front page is not in a talkative mood. The invitation knows a better way in.

A few pointers:

- Decode the QR code to see where it sent the guests. The address will not load as written, but the same path works on your local copy of the portal.
- Hosts rarely say everything out loud. Read what the page says, then read what it is made of.
- Compare the page against the paper. Paper does not update itself.

## Question

What is the flag hidden on the event page?

Answer format: `THM{...}`
