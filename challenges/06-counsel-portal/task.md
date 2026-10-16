# Counsel Portal

Everyone in Blackthorn House lied during their first interview. That is not unusual: people lie to investigators about small, embarrassing things all the time. Your job is not to be shocked that they lied. Your job is to work out whose lie actually matters.

We were not the first to interview them. While the house waited for us to arrive, Celeste Ward, the family attorney, did what attorneys do: she sat everyone down, took their statements, and filed all five in the Legal Office's case portal. Her own is among them. She also keeps her private working notes in the same portal, sealed so that only counsel can read them, and the portal quietly keeps a sealed record of any statement that is edited after it is filed. You have been given a read-only guest login.

This task has no download. The portal is online at:

- https://blackthorn-counsel-portal.vercel.app/

Open it in your browser. The first visit can take a second or two to wake the portal up.

As a guest you can read the five filed statements. The sealed records are where the secrets actually live, and the guest view will not hand those over. The portal was thrown together quickly, though, and it does not keep your words separate from its own: whatever you type in the search box is dropped straight into the question it asks its database.

Bonus hint(s) from Luigi (the GOAT):
- Look up the OWASP Top 10
- What are typical vulnerabilities in webapps with input fields?
- What is actually happening in the backend when a user queries a database?
- Did you guys know that the execs accept bribes? Might get an extra hint, you never know...


A few pointers:

- Read all five statements first. Each one contains a lie. Four of those lies are about something other than the library. Look at when each statement was filed, too: one of them was not left alone.
- The box expects a word to look for. Give it something that is not just a word. A lone apostrophe is a good first thing to try: it is the character the portal uses to mark where your text starts and stops, so feeding it one too many confuses the portal about which part is yours and which part is its own.
- When it breaks, read the error carefully. It prints the whole query it tried to run, with your text already wedged inside it. Once you can see the shape of that query, you can see how to finish it so that it stops filtering and hands back everything, sealed records included. The guest view is only a condition in that query, and a condition can be made always true.
- Once you can see the sealed records, sort them. Four are counsel's notes about other people's secrets, and it is worth noticing what she planned to do with them. The fifth is the portal's own record of a story that changed. Ask which of the five has anything to do with where someone was while the library was open.

## Checkpoint question

How many sealed records does the portal hold in total, counting counsel's notes and revision records together?

Answer format: a number.

## Question

What is the flag in the sealed revision record for Celeste Ward's statement?

Answer format: `THM{...}`
