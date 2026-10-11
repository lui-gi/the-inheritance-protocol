BLACKTHORN HOUSE: CASE BOARD
============================

This is the investigation's case board: a timeline of the night Adrian Vale
died, with four pieces of evidence missing. It comes with a script that runs
it on your own computer. Nothing here touches the internet.


WHAT IS IN THIS FOLDER
----------------------

  README.txt     This file.
  serve.py       Starts the case board on your machine.
  api/           The case board app itself.
  vercel.json    Hosting config. You can ignore it.


WHAT YOU NEED
-------------

Python 3.7 or newer, a web browser, and your answers from the earlier tasks.
Nothing to install beyond that.

To check, open a terminal and run:

  python3 --version

On Windows the command may be "python" or "py" instead of "python3".
No Python? Get it from https://www.python.org/downloads/ or use the
TryHackMe AttackBox, which already has it.


HOW TO START THE BOARD
----------------------

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

The board lists the night in order. Four rows are locked. Each one asks for
something you already found in an earlier task, and names the task. Type it
in and the row opens with what that evidence proved.

When all four rows are open, the last row lets you ask the estate archive for
a message Adrian recorded the night before he died. The archive will have an
opinion about whether you are allowed to hear it.

The board has no accounts and no passwords. It remembers who you are, and
what you have pinned, with cookies in your browser.


LOOKING AT COOKIES
------------------

A cookie is a small named value a website asks your browser to keep and send
back with every visit. Your browser will show you the cookies a site has set.

  Chrome, Edge:   F12, then the "Application" tab, then Cookies on the left.
  Firefox:        F12, then the "Storage" tab, then Cookies on the left.
  Safari:         turn on the Develop menu in Settings > Advanced, then
                  Develop > Show Web Inspector > Storage.

Double-click a value in that list to edit it. Reload the page afterwards.


IF SOMETHING GOES WRONG
-----------------------

"Could not start on port 8000"
  Something else is using that port (the Task 6 portal, perhaps). Stop it
  with Ctrl+C, or pick another port:

    python3 serve.py 8080

  Then use http://localhost:8080/ instead.

"Cannot find the case board app"
  serve.py was moved away from the api folder. Unzip the download again and
  run it from there.

"python3 is not recognized" or "command not found"
  Try "python serve.py" or "py serve.py".

A row will not accept an answer you are sure of
  Paste it exactly as the earlier task gave it, with no spaces around it.
  Capitals do not matter.

You want a clean start
  Use the "Clear the board and start again" link at the bottom of the page.
