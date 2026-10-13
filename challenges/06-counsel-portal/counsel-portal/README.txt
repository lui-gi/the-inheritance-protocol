BLACKTHORN LEGAL OFFICE: COUNSEL PORTAL
=======================================

While the house waited for investigators, family counsel took everyone's first
statement and filed it in the Legal Office's small web portal.
You have been given a read-only guest login. This is the recovered app, plus
a script that runs it on your own computer. Nothing here touches the internet.


WHAT IS IN THIS FOLDER
----------------------

  README.txt     This file.
  serve.py       Starts the portal on your machine.
  api/           The portal app itself.
  vercel.json    Hosting config. You can ignore it.


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


WHAT YOU ARE LOOKING AT
-----------------------

The portal has one search box. As a guest you can read the five filed
statements, one from each person who was in the house. Counsel's own working
notes are sealed, and so is the portal's record of any statement that was
edited after filing. The guest view will not show you either.

The portal was built in a hurry. It is not careful about what you type into
that search box. If a search makes it unhappy, it will tell you exactly what
went wrong, which is more than it should.


IF SOMETHING GOES WRONG
-----------------------

"Could not start on port 8000"
  Something else is using that port. Pick another:

    python3 serve.py 8080

  Then use http://localhost:8080/ instead.

"Cannot find the portal app"
  serve.py was moved away from the api folder. Unzip the download again and
  run it from there.

"python3 is not recognized" or "command not found"
  Try "python serve.py" or "py serve.py".
