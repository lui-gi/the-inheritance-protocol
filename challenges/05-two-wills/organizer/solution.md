# Task 5: The Two Wills (ORGANIZER ONLY)

Flag: `THM{THE_WILL_WAS_REPLACED}`

Checkpoint answers: question 1 is `Vale_Will_superseded.pdf`, question 2 is `BH-WS-0418`.

Target solve time: about 8 minutes. Skills: computing a SHA-256 hash, comparing it with a known-good checksum, opening a password-protected zip. No VM is involved: everything is in the task download.

## How the artifacts are built

The task has two stages. Stage 1 is the hashing, stage 2 is one short record read top to bottom.

| File | Stage | What it is |
| :---- | :---- | :---- |
| `Vale_Will_superseded.pdf` | 1 | The genuine will, signed 1 October 2026. Its SHA-256 matches the receipt. The archive renamed it from `Vale_Will.pdf` when it was replaced. |
| `Vale_Will_FINAL_signed.pdf` | 1 | The replacement, dated 29 October 2026. Its SHA-256 matches nothing Adrian filed. |
| `archive-entry.txt` | 1 | The estate archive's export of entry `EA-0042`: the two filenames, Adrian's filing receipt with the genuine checksum, and a plain statement of what the zip password is. Contains no flag and never mentions `c.ward` or the workstation. |
| `replacement-record.zip` | 2 | Password-protected zip holding `replacement-record.log`. Password: the SHA-256 of the replacement will (below). Legacy ZipCrypto, so Windows Explorer, macOS, `unzip`, and 7-Zip all open it. |
| `organizer/replacement-record.log` | none | Plaintext copy of the zip's contents for organizers. Never distribute it. |

The hashes:

| File | SHA-256 |
| :---- | :---- |
| `Vale_Will_superseded.pdf` (genuine, in the receipt) | `93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914` |
| `Vale_Will_FINAL_signed.pdf` (replacement, the zip password) | `18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6` |

The password is the replacement's hash on purpose. The genuine hash is printed in the receipt, so using it would let players skip the hashing. The replacement's hash is written nowhere in the download: the only way to get it is to compute it.

The two wills are identical except for Article 4 and the signing date:

| | Genuine | Replacement |
| :---- | :---- | :---- |
| Article 4 | "The Trustee keeps the records and files the paperwork. The Trustee has no vote in Blackthorn Security and no authority over my heirs, under any circumstances." | "If any heir is judged unfit to serve, the Trustee shall hold and vote that heir's shares in Blackthorn Security until the Trustee decides otherwise. The Trustee alone judges fitness." |
| Signed | 1 October 2026 | 29 October 2026 |
| PDF creation date | 2026-10-01 13:05:27 | 2026-10-29 18:47:33 |

Reading the difference is optional and unscored. Both wills keep Article 5 ("Trust the signed hash, not the filename"), so the replacement quotes the rule that catches it.

## Intended solution

1. Download and unzip the task file.
2. Read `archive-entry.txt`. The receipt gives the checksum Adrian filed on 1 October:

   ```
   sha256=93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914
   ```

   The integrity check says one file does not match, and that the zip opens with that file's SHA-256.
3. Hash both wills: `sha256sum *.pdf`

   ```
   18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6  Vale_Will_FINAL_signed.pdf
   93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914  Vale_Will_superseded.pdf
   ```

   On macOS use `shasum -a 256 *.pdf`. On Windows use `certutil -hashfile <file> SHA256`. CyberChef works too: drag the file in and apply "SHA2" with size 256.
4. The file called "superseded" matches the receipt. Answer question 1 with `Vale_Will_superseded.pdf`.
5. Open the zip with the other hash: `unzip -P 18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6 replacement-record.zip`, or double-click it and paste the hash.
6. Read `replacement-record.log`. The header says `BH-WS-0418` is the Legal Office workstation, registered to `c.ward`. The replacement was created on it on 29 October. Answer question 2 with `BH-WS-0418`.
7. The flag is on the archive's warning line at 22:26:18, three lines from the end.

## The sealed record

```
# Blackthorn Estate Archive replacement record
# entry:       EA-0042, Last Will and Testament of Adrian Vale
# sealed:      2026-10-31T22:26:18-04:00 (a file was replaced, and the new file fails the signed manifest)
# workstation: BH-WS-0418 is the Legal Office workstation
# registered:  c.ward (Celeste Ward, family counsel)
#
# Everything that has happened to this entry (all times local, UTC-04:00).
2026-10-01T13:05:27-04:00 file    CREATED name=Vale_Will.pdf account=c.ward workstation_ID=BH-WS-0418
2026-10-01T15:20:00-04:00 file    SIGNED name=Vale_Will.pdf account=a.vale
2026-10-01T15:42:10-04:00 archive FILED name=Vale_Will.pdf account=a.vale sha256=93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914
2026-10-01T15:42:10-04:00 archive MANIFEST signed_by=a.vale signed_sha256=93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914 manifest_signature=VALID
2026-10-01T15:42:11-04:00 archive RECEIPT written for a.vale. Receipts cannot be edited
2026-10-27T20:52:16-04:00 archive READ name=Vale_Will.pdf account=a.vale manifest_signature=VALID
2026-10-29T18:47:33-04:00 file    CREATED name=Vale_Will_FINAL_signed.pdf account=c.ward workstation_ID=BH-WS-0418
2026-10-31T22:26:17-04:00 archive REPLACE-REQUEST old=Vale_Will.pdf new=Vale_Will_FINAL_signed.pdf account=c.ward workstation_ID=BH-WS-0418 result=ACCEPTED (counsel may replace files)
2026-10-31T22:26:17-04:00 archive RENAME old=Vale_Will.pdf new=Vale_Will_superseded.pdf
2026-10-31T22:26:17-04:00 archive FILED name=Vale_Will_FINAL_signed.pdf account=c.ward sha256=18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6
2026-10-31T22:26:18-04:00 archive MANIFEST signed_by=a.vale signed_sha256=93526f56d98475324b148a942241c74eac5e20a7ad8c4d88266957cd07b62914 manifest_signature=MISMATCH
2026-10-31T22:26:18-04:00 archive WARN the file now called FINAL was never signed by a.vale. House rule, per A. Vale: trust the signed hash, not the filename. THM{THE_WILL_WAS_REPLACED}
2026-10-31T22:26:18-04:00 archive NOTICE this record is now sealed with the SHA-256 of the file that failed the manifest
2026-10-31T22:31:40-04:00 archive READ name=Vale_Will_FINAL_signed.pdf account=c.ward workstation_ID=BH-WS-0418 manifest_signature=MISMATCH
2026-11-01T01:40:00-04:00 archive EXPORT entry=EA-0042 for the investigation
```

How this covers the design document:

- "The older copy matches Adrian's archived checksum": the receipt and stage 1.
- "A later creation chain": the genuine will was created, signed, and filed on 1 October. The replacement was created on 29 October and filed on 31 October at 22:26:17, nine minutes after Adrian was found.
- "A mismatched signature manifest": the only manifest Adrian ever signed lists the genuine hash. It was `VALID` until the replacement, and `MISMATCH` after it.

Both wills were created on `BH-WS-0418`, because Celeste drafted the genuine one as family counsel. The workstation alone does not separate them: the dates and the signature do.

## Shortcuts

`grep -r "THM{"` finds nothing in the download, because the flag only exists inside the encrypted zip.

Hashing both files and trying each as the password, without reading the receipt, opens the zip on the first or second try. That still means hashing, and question 1 still needs the receipt.

`exiftool` or `pdfinfo` shows the two creation dates, which is enough to guess question 1. It does not give the password. A player who does this has found the "later creation chain" by another road.

Copying the checksum out of the receipt and trying it as the password fails. That is the reason the password is the other hash.

## Common stumbles

- PowerShell `Get-FileHash` prints the hash in capitals, and the zip rejects it. The task text warns about this. `(Get-FileHash file).Hash.ToLower()` fixes it, and so does `certutil`.
- Re-saving or "printing to PDF" either will changes its bytes and its hash. Players must hash the files exactly as downloaded.
- A trailing space or newline pasted with the hash makes the password fail.

## What players should take away

- The will Adrian signed is the one the archive now calls "superseded". The one called "FINAL" was never signed by him.
- The replacement was filed at 22:26:17 on Halloween by `c.ward`, nine minutes after Adrian was found, from the Legal Office workstation `BH-WS-0418`.
- The replacement gives the Trustee, Celeste Ward, the power to vote any heir's shares if she alone judges that heir unfit.
- A filename is a claim. A hash is evidence.

This shows Celeste replaced the will and what she gained. It does not show who opened the library or why the dashboard blames Marcus: those are Flags 3 and 7. `BH-WS-0418` is introduced here so that Flag 7 can tie the commit's signing key to it. Do not tell players this proves murder.

## Hints, in order of generosity

1. "Open `archive-entry.txt` and find the line that starts `sha256=`. That is the fingerprint of the real will. Now fingerprint both PDFs: `sha256sum *.pdf`."
2. "One PDF matches the receipt and one does not. The zip password is the full hash of the one that does not, in lowercase, pasted with no spaces."
3. "The password is `18a6966de197eb1d0866769e6960ea0fa03eb90daec7cd75c4e67e4fa0cd16c6`. In the record inside, read the header, then the lines dated 31 October."

## Publishing to the room

- Zip the two PDFs, `archive-entry.txt`, and `replacement-record.zip` together into `task5-two-wills.zip` and upload it as the task file. This is done by hand once the task is final: the outer zip is not kept in the repo and has no password.
- Do not upload the PDFs on their own, and do not open and re-save them first. Any change to their bytes breaks the receipt and the password.
- Do not include the `organizer` or `build` folders.
- Paste `task.md` into the task body. Set the three answers to `Vale_Will_superseded.pdf`, `BH-WS-0418`, and the flag above.

## Rebuilding

Run this after changing either will, the receipt, the record, or the flag. The build needs only the Python standard library and is reproducible: the same script gives byte-identical files. It also checks its own output (the two hashes differ, the receipt carries the genuine hash and not the other, nothing outside the zip contains the flag, and `archive-entry.txt` mentions neither `c.ward` nor the workstation ID).

Changing one character of either will changes its hash. The script prints both hashes when it finishes: copy them into this file and into `canon/canon.md`, because Flag 8 reuses them.

```
python3 challenges/05-two-wills/build/make_wills.py
```
