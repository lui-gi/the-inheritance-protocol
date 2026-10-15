# Portrait in the Hall (ORGANIZER ONLY)

Flag: `THM{TRUST_THE_HASH}`

Target solve time: about 4 minutes. Skills: reading image metadata, decoding a short Base64 string. No VM is involved: everything is in the task download.

## How the artifact is built

`portrait.jpg` is an ordinary JPEG. Nothing is hidden in the pixels and nothing is appended to the file. Adrian's note sits in the EXIF UserComment in plain English, as one line. Only the flag inside the note is Base64, and the sentence just before it tells the reader it is encoded and hints at the encoding ("Its alphabet has sixty-four letters").

| EXIF field | Value |
| :---- | :---- |
| ImageDescription | `Adrian Vale, founder. Oil on canvas, digitised for the east hall frame. Catalogue no. BH-1959-AV` |
| Artist | `Commissioned by the sitter, who also chose the lighting, the chair, and the expression.` |
| Software | `Blackthorn Gallery Frame 2.3` |
| Copyright | `Blackthorn Security. Do not hang crooked.` |
| DateTime (modified) | `2026:10:27 21:15:44`, offset `-04:00` |
| DateTimeOriginal | `2024:04:13 11:20:00` |
| UserComment | Plain English, 922 characters, starting `If you are reading this`. Holds the Base64 string `VEhNe1RSVVNUX1RIRV9IQVNIfQ==` |

The catalogue number is flavour only. It is not a password for anything.

## Intended solution

1. Download and unzip the task file.
2. Read the metadata: `exiftool portrait.jpg`. Without exiftool, `strings -n 8 portrait.jpg | head` shows the same fields, and so does any online EXIF viewer.
3. Read the User Comment. It is Adrian's note, and all of it is readable except one short string near the end: `VEhNe1RSVVNUX1RIRV9IQVNIfQ==`.
4. Take the nudge in the sentence before it ("put it in a costume", "Its alphabet has sixty-four letters", "any decoder will take it off") and decode the string as Base64. Either of these works:
   - `echo 'VEhNe1RSVVNUX1RIRV9IQVNIfQ==' | base64 -d`
   - Paste the string into CyberChef and apply "From Base64".
5. The output is the flag.

## The note as stored

The comment is a single line: the paragraphs below are joined by spaces in the file.

```
If you are reading this, you looked behind the portrait. Nobody in this family ever has. They walk past me every day and not one of them has checked.

27 October. I spent tonight rereading my own will, and I no longer trust a document just because it has my name on the cover. Anyone can call a file "final". Several people in this house would like to.

So here is the one rule I still believe. Trust the signed hash, not the filename. On the day I signed the real will, I filed its checksum in the estate archive. If two wills ever turn up, that number settles it. Nothing else does, including whoever sounds most certain.

Tomorrow I change the guest list. I want everyone in the room when I say this out loud.

The next thing I write is the part worth stealing, so I have put it in a costume. It is not locked. Its alphabet has sixty-four letters, and any decoder will take it off for you.

VEhNe1RSVVNUX1RIRV9IQVNIfQ==

A.V.
```

## Shortcuts

`grep "THM{"` and `strings | grep THM` find nothing, because the flag only exists in encoded form. Players have to decode the string.

`strings portrait.jpg | head` does expose the note without an EXIF tool. That is fine: it still leads to the decode step.

## What players should take away

- Adrian's rule: "Trust the signed hash, not the filename." One of the will files may be a counterfeit with a convincing name.
- Adrian filed a checksum of the genuine will in the estate archive on the day he signed it. The Two Wills task relies on this.
- The note is dated 27 October, and the file was last modified at 21:15:44 that evening. "Tomorrow I change the guest list" matches the 28 October edit from the Invitation task.

The note does not name anyone, and it does not say a counterfeit will already exists. Do not tell players who Adrian suspected.

## Hints, in order of generosity

1. "Pictures carry labels the eye cannot see. `exiftool`, or any online EXIF viewer, will read them to you."
2. "Read Adrian's note in the User Comment to the end. One piece is not English, and he tells you how many letters its alphabet has."
3. "The string ending in `==` is Base64. Decode it with `base64 -d` or CyberChef's From Base64."

## Publishing to the room

- Zip `portrait.jpg` into `task2-portrait.zip` and upload the zip as the task file. This is done by hand once the task is final: no zip is kept in the repo.
- Do not upload `portrait.jpg` on its own. An image upload may be recompressed, which would strip the metadata and with it the whole challenge.
- Paste `task.md` into the task body and set the answer to the flag above.

## Rebuilding

Run this after changing the note, the metadata, or the painting. The build is reproducible: the same sources and Pillow version give a byte-identical file. Keep `canon/canon.md` in sync.

```
python3 -m venv .venv
.venv/bin/pip install -r challenges/02-portrait/build/requirements.txt
.venv/bin/python challenges/02-portrait/build/make_portrait.py
```
