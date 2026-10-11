BLACKTHORN HOUSE PORTAL: RECOVERED SNAPSHOT
===========================================

The house portal went dark during the lockdown. This is the last nightly
snapshot it took of itself, plus a small script that brings it back to life
on your own computer. Nothing here touches the internet.


WHAT IS IN THIS FOLDER
----------------------

  README.txt               This file.
  serve.py                 Starts the portal on your machine.
  portal.blackthorn.thm/   The snapshot itself.


WHAT YOU NEED
-------------

Python 3.7 or newer. Nothing to install beyond that.

To check, open a terminal and run:

  python3 --version

On Windows the command may be "python" or "py" instead of "python3".
No Python? Get it from https://www.python.org/downloads/ or use the
TryHackMe AttackBox, which already has it.


HOW TO START THE PORTAL
-----------------------

1. Unzip the download. Keep everything together, exactly as it came.

2. Open a terminal in this folder (the one holding this README).

3. Run:

     python3 serve.py

   Windows:

     python serve.py

4. Open http://localhost:8000/ in your browser.

5. When you are done, go back to the terminal and press Ctrl+C.


FINDING YOUR WAY AROUND
-----------------------

The portal used to live at http://portal.blackthorn.thm/ and that address
is gone for good. While the script is running, the same site lives at
http://localhost:8000/ instead.

So when a clue gives you a portal address, swap the front of it and keep
the rest:

  http://portal.blackthorn.thm/some/page/
  becomes
  http://localhost:8000/some/page/


IF SOMETHING GOES WRONG
-----------------------

"Could not start on port 8000"
  Something else is using that port. Pick another:

    python3 serve.py 8080

  Then use http://localhost:8080/ wherever this file says 8000.

"Cannot find the 'portal.blackthorn.thm' folder"
  serve.py was moved away from the snapshot. Unzip the download again and
  run it from there.

"python3 is not recognized" or "command not found"
  Try "python serve.py" or "py serve.py".

The browser says the page was not found
  Check the address. The portal does not list its folders, so you need the
  full path to a page, including the last slash.
