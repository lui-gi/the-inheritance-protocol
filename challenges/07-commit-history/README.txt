BLACKTHORN DASHBOARD: EVIDENCE COPY
===================================

This download holds two things, copied by the investigation at 01:55 on
1 November 2026:

  blackthorn-dashboard/    The code for the wall display in the front hall, as a
                           Git repository. Start here.
  signing-record.zip       A record the hub sealed about one commit in that
                           repository. Locked. Open it second.

Nothing here runs, and nothing here touches the internet. You only need Git.
The AttackBox has it. On your own machine, type "git --version" to check.


WHAT GIT IS, IN FOUR LINES
--------------------------

Git keeps every saved version of a project. Each saved version is a "commit".
A commit records what changed, when, a message, and who the author claims to be.
Every commit has a hash, a long string of letters and digits that names it.
The first 7 characters of a hash are its "short hash", and Git accepts those too.


LOOKING THROUGH THE HISTORY
---------------------------

Open a terminal inside the blackthorn-dashboard folder first. The commands are
the same on Linux, macOS, the AttackBox, and Windows.

  git log                         every commit, newest first, with author and date
  git log --oneline               the same, one line each, with short hashes
  git show SHORTHASH              exactly what one commit changed
  git log -p                      every commit together with what it changed
  git log -S "SOME TEXT"          only the commits that added or removed that text

If the history fills the screen, press space for the next page and q to leave.


THE SEALED RECORD
-----------------

One commit taught the display to call a device MARCUS-ADMIN.
signing-record.zip opens with the short hash of that commit: the first 7
characters, in lowercase, exactly as "git log --oneline" prints them.

All times are local house time (UTC-04:00).
