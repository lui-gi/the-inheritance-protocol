BLACKTHORN HOUSE SERVER: EVIDENCE SNAPSHOT
==========================================

This folder is a copy of part of the house server, "blackthorn-srv", taken by
the investigation at 01:25 on 1 November 2026. It is only files. Nothing here
runs, and nothing here touches the internet.

It is laid out the way the server was, so paths look like Linux paths:

  etc/passwd          Every account on the server, one per line.
  etc/group           Which accounts belong to which groups.
  var/log/auth.log    Every login and admin command since 1 May 2026.
  home/               Files from the three people who had a login here.

The rest (boot, opt, usr, the other files in etc and var) is the ordinary
furniture of a Linux server: settings, scripts, and smaller logs. You are
welcome to look around. Some folders begin with nothing but a dot-file, so
use "ls -a" if a folder looks empty.


READING etc/passwd
------------------

Each line is one account, with fields separated by colons:

  name : x : user ID : group ID : description : home folder : shell

The user ID is the number that matters. The system decides what an account
may do by its number, not its name.


SEARCHING
---------

The log is far too long to read, refer back to the toolkit we suggested in Task 1.

  Linux, macOS, AttackBox:

    grep "something" var/log/auth.log       search one file
    grep -r "something" .                   search every file in this folder

  Windows (PowerShell):

    Select-String "something" var\log\auth.log
    Get-ChildItem -Recurse -File | Select-String "something"

Any editor with "find in files" works just as well.

All times in the log are local house time (UTC-04:00).
