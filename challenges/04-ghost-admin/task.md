# Task 4: Ghost Admin

Blackthorn House has one server, in one small room, behind one very expensive door. Marcus Vale built it, and talks about it the way other people talk about their children.

The staff have a rumour. They say Marcus has more than one way into that server, and that the second one does not have his name on it. After Task 3, you can see why that would interest us.

We took a snapshot of the server after the lockdown. Download the task file and unzip it. You will find a folder called `blackthorn-server`, laid out like the real machine:

- `README.txt`, which explains the folder and how to search it
- `etc/passwd`, the list of every account on the server
- `var/log/auth.log`, six months of logins
- `home/`, files belonging to the three people who had a login

Start with the list of accounts. Most of them are boring on purpose. One of them is boring on somebody else's purpose.

When you have its name, search the whole snapshot for it. You will learn who made it, when it was used, and that you are not the first person to go looking. That person left something sealed, and left instructions for opening it.

A few pointers:

- In `etc/passwd`, the third field is the user ID. The real administrator is `root`, with user ID `0`. Nobody else should have that number.
- `grep -r "name" .` searches every file in the folder at once. The README has the Windows version.
- The log is in date order, so the last line that mentions an account is the last time it was used.
- Adrian was found at 10:17 PM on 31 October. Notice what the log says about that night, and what it does not say.

## Questions

1. What is the name of the hidden administrator account?

2. On what date was that account last used?

   Answer format: `YYYY-MM-DD`

3. What is the flag in Adrian's sealed findings?

   Answer format: `THM{...}`
