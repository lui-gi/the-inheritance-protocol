# Commit History

There is a display on the wall of the front hall at Blackthorn House. It shows a live feed of every door in the building: which one opened, when, and for whom. The family calls it "the dashboard". Theo calls it "the snitch".

At 22:04 on Halloween, with thirteen minutes left on Adrian Vale's clock, the snitch told the whole hall that the library had been opened by a device called `MARCUS-ADMIN`. Three people saw it. All three have since mentioned it to us, unprompted, at length.

You already know from the Smart Lock task that the device at the library door was the Legal Office tablet, `BH-TAB-0417`. The hub's own log said so. So why did the dashboard call it `MARCUS-ADMIN`?

Because somebody taught it to. The dashboard gets its device names from its own code, and that code lives in a Git repository, which remembers every change anyone has ever made to it.

Download the task file and unzip it. You will find:

- `blackthorn-dashboard/`, the dashboard's code, as a Git repository
- `signing-record.zip`, a record the hub sealed about one commit in that repository
- `README.txt`, a short note on how to look through a Git history

Open a terminal inside `blackthorn-dashboard/` and find the commit that introduced `MARCUS-ADMIN`.

The zip is locked. Its password is the short hash of that commit: the first 7 characters, in lowercase, exactly as `git log --oneline` prints them.

A few pointers:

- You need Git. The AttackBox has it. On your own machine, `git --version` will tell you.
- `git log` lists every commit, newest first. `git log --oneline` does the same in one line each.
- `git show` followed by a short hash shows exactly what that commit changed. Lines starting with `-` were removed, and lines starting with `+` were added.
- `git log -S "MARCUS-ADMIN"` lists only the commits that added or removed that text. This is the fast way.
- Look at who wrote the commit you find, and at what its message claims it does. Then look at what it actually does.
- Adrian left house rules for this repository in `CONTRIBUTING.md`. They are short, and they explain why the hub kept a record at all.
- Once the zip is open, read the record inside from top to bottom. Each line names a commit, a signing key, and the workstation that key lives on.

## Questions

1. What is the short hash of the commit that introduced `MARCUS-ADMIN`?

   Answer format: `*******`

2. According to the sealed record, what is the ID of the workstation that signed that commit?

   Answer format: `BH-**-****`

3. What is the flag in the sealed signing record?

   Answer format: `THM{...}`
