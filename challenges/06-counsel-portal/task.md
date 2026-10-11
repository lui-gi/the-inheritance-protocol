# Task 6: Family Secrets

Everyone in Blackthorn House lied during their first interview. That is not unusual: people lie to investigators about small, embarrassing things all the time. Your job is not to be shocked that they lied. Your job is to work out whose lie actually matters.

The Legal Office ran a small case portal where the five first-interview statements were filed. Celeste Ward, the family attorney, keeps her own working notes in the same portal, sealed so that only counsel can read them. You have been given a read-only guest login.

This task has one download:

- `task6-counsel-portal.zip`, the recovered portal, with a script that serves it locally and a README that explains how.

Unzip it, open a terminal in the `counsel-portal` folder, and run `python3 serve.py`. The portal will come up at `http://localhost:8000/`. The README covers Windows and troubleshooting.

As a guest you can read the five filed statements. The sealed counsel's notes are where the secrets actually live, and the guest view will not hand those over. The portal was thrown together quickly, though, and it is not careful about what you type into its one search box.

A few pointers:

- Read all five statements first. Each one contains a lie. Four of those lies are about something other than the library.
- Try a search that the portal was not expecting. If it breaks, read what it tells you: it will show you the query it was trying to run.
- Once you can see the sealed notes, the question is which secret puts someone in the library on the night Adrian died.

## Checkpoint question

How many sealed counsel's notes does the portal hold?

Answer format: a number.

## Question

What is the flag in Celeste Ward's sealed note?

Answer format: `THM{...}`
