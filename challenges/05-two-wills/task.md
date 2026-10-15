# The Two Wills

Adrian Vale wrote one will. He was very clear about that. He was clear about most things, usually twice, and louder the second time.

The estate archive disagrees. When we opened Adrian's entry after the lockdown, there were two wills in it. Both carry his name. Both look official. One of them is called "FINAL", which in this family is less a description than a warning.

Back in the Portrait in the Hall task, Adrian told you what to do if this ever happened: trust the signed hash, not the filename. He also said he filed a checksum of the real will on the day he signed it. We found that receipt.

Download the task file and unzip it. You will find:

- `Vale_Will_FINAL_signed.pdf` and `Vale_Will_superseded.pdf`, the two wills
- `archive-entry.txt`, the archive's own summary of the entry, including Adrian's filing receipt
- `replacement-record.zip`, a sealed record the archive made when something in the entry changed

Start with `archive-entry.txt`. The receipt gives the SHA-256 checksum of the will Adrian actually signed. Work out the SHA-256 of each PDF and see which one agrees with him.

The zip is locked. Its password is the SHA-256 of the will that does **not** match the receipt: all 64 characters, in lowercase.

A few pointers:

- A hash is a fingerprint of a file's exact contents. Change one comma and the whole fingerprint changes. The filename is not part of it, so renaming a file fools nobody who checks.
- Linux: `sha256sum *.pdf`. macOS: `shasum -a 256 *.pdf`. Windows: `certutil -hashfile Vale_Will_FINAL_signed.pdf SHA256`, once per file.
- PowerShell's `Get-FileHash` prints capital letters. The password wants lowercase, so use `certutil`, or lowercase it first.
- Copy and paste the hash. Nobody has ever typed 64 characters correctly while being watched.
- Once the zip is open, read the record inside from top to bottom. It is short, and it knows who created each file, where, and when.
- If you are curious what the fuss was about, read both wills side by side. They differ in one article.

## Questions

1. Which file is the will Adrian actually signed?

   Answer format: `Vale_Will_*.pdf`

2. According to the sealed record, what is the ID of the workstation the replacement will was created on?

   Answer format: `BH-**-****`

3. What is the flag in the sealed replacement record?

   Answer format: `THM{...}`
