**HALLOWEEN CYBERSECURITY**  
**MURDER MYSTERY CTF**

Designed for GWC × Cybersecurity Club × TryHackMe

Two completely different tones: a wealthy-family mansion whodunit, and a modern ransomware investigation inspired by a documented real-world attack.

| Story | Tone | Cyber Focus |
| :---- | :---- | :---- |
| 02 — The Inheritance Protocol | Mansion / family / betrayal | Smart-home forensics, stego, Git, access logs |
| 03 — Code Blue | High-stakes incident response | Credentials, MFA, lateral movement, exfiltration, ransomware |

# **STORYLINE 02 — THE INHERITANCE PROTOCOL**

*“Everyone in the house has a secret. Only one of them needed the logs erased.”*

# **Concept**

A wealthy cybersecurity founder dies during an invitation-only Halloween dinner at his isolated smart mansion. The house automatically locks down, the family turns on one another, and a newly signed digital will appears to change control of a multimillion-dollar security company. Participants play as outside digital investigators. Every suspect is hiding something, but the winning team must separate embarrassing secrets from evidence of murder.

The tone is inspired by modern ensemble whodunits: eccentric relatives, inheritance disputes, unreliable statements, shifting alliances, and a house full of physical and digital evidence. It should feel theatrical and funny in places, but the plot and characters below are original.

# **Opening Scenario**

At 10:17 PM on Halloween, security-company founder ADRIAN VALE is found dead in the library of Blackthorn House, his private smart mansion. Minutes earlier, he had announced that he would reveal a new succession plan for Blackthorn Security. The mansion’s network then dropped offline, the front gates locked, and the digital copy of Vale’s will was replaced by a newer version.

Five people were inside the house. All five had motive. All five lied during their first interview. One of them also altered the digital evidence.

Your team has 75 minutes to collect eight flags, reconstruct the timeline, identify the killer, and prove which evidence was manipulated.

# **The Victim**

Adrian Vale, 67 — founder of Blackthorn Security, famous for building high-security systems and for treating family arguments like penetration tests. He planned to step down as CEO after the Halloween dinner. Before dessert, he told the room: “By midnight, none of you will own what you think you own.”

# **Suspects**

| Suspect | What They Are Hiding | Why They Look Guilty |
| :---- | :---- | :---- |
| Evelyn Vale — Daughter / CFO | Expected to inherit voting control. Secretly moved company money to cover a failed acquisition. | Financial motive; she argued with Adrian in front of everyone. |
| Marcus Vale — Son / CTO | Built the mansion’s smart-home system. Secretly kept an unauthorized administrator account. | Technical access; his credentials appear in house logs. |
| Nina Park — Niece / Red-Team Lead | Adrian’s favorite protégé. Secretly copied an unreleased product prototype to prove it was vulnerable. | Possessed exploit code and knew how to bypass several sensors. |
| Celeste Ward — Family Attorney | Prepared the new will and serves as trustee for the Vale family holdings. Secretly drafted two conflicting versions. | Would gain temporary control over the trust if the heirs were disqualified. |
| Theo Grant — Estate Manager | Controls staff badges, cameras, and physical keys. Secretly disabled one hallway camera to hide an unrelated meeting. | Had physical access to every room and initially lies about the camera outage. |

# **Organizer-Only Truth**

The killer is CELESTE WARD, the family attorney. Adrian discovered that Celeste had quietly rewritten trust language so that she would temporarily control Blackthorn Security if the heirs were judged incapable of serving. He planned to revoke her authority that night. Celeste killed Adrian during a short gap in the house timeline, then used access she already had as legal counsel to replace the signed will and manipulate smart-home evidence so the investigation would point toward Marcus.

The murder method itself should stay deliberately non-technical and non-instructional in the game. The cyber component is about covering tracks, forging digital evidence, and proving the timeline — not about teaching a physical method of harm.

# **CTF Progression**

| Challenge | Skill | What Players Discover | Flag |
| :---- | :---- | :---- | :---- |
| FLAG 1 — The Invitation | QR / simple web forensics | A QR code on Adrian’s printed dinner invitation leads to a hidden event page. Inspecting the page source reveals the first flag and a timestamp showing the guest list was changed after invitations were printed. | THM{THE\_GUEST\_LIST\_CHANGED} |
| FLAG 2 — Portrait in the Hall | Steganography / metadata | A digital portrait file contains embedded metadata pointing to a hidden note: “Trust the signed hash, not the filename.” This introduces the idea that one will file may be counterfeit. | THM{TRUST\_THE\_HASH} |
| FLAG 3 — The Smart Lock | Log analysis | Teams compare smart-lock entries. Marcus’s account appears to open the library, but the device identifier belongs to a legal-office tablet registered to Celeste. | THM{ACCOUNT\_IS\_NOT\_IDENTITY} |
| FLAG 4 — Ghost Admin | Linux / grep | A small VM or log bundle contains a hidden admin account Marcus created months earlier. It is real misconduct — but timestamps prove it was not used during the murder window. | THM{RED\_HERRING\_ROOT} |
| FLAG 5 — The Two Wills | Hashing / integrity | Teams hash two PDF or text artifacts. The “new” will has a later creation chain and a mismatched signature manifest. The older copy matches Adrian’s archived checksum. | THM{THE\_WILL\_WAS\_REPLACED} |
| FLAG 6 — Family Secrets | OSINT-style correlation | Fake social posts, board bios, calendar entries, and photos reveal each suspect lied about something. Only Celeste’s lie intersects with the library timeline. | THM{SECRETS\_ARE\_NOT\_MURDER} |
| FLAG 7 — Commit History | Git forensics | A local Git repository for the smart-home dashboard shows someone changed event-label code so a legal-office device would display as “MARCUS-ADMIN.” The commit author was scrubbed, but the signing key maps to Celeste’s workstation. | THM{FOLLOW\_THE\_COMMIT} |
| FLAG 8 — The Last Testament | Multi-clue final | Combining the hashes, access logs, device ID, and commit history unlocks Adrian’s final recorded message: he was revoking Celeste’s trustee authority at midnight. | THM{CELESTE\_WARD} |

# **Final Accusation Requirements**

* WHO killed Adrian Vale?  
* WHAT was changed or forged after his death?  
* WHICH account appears guilty at first, and why is that misleading?  
* WHAT four pieces of digital evidence connect the killer to the cover-up?  
* WHAT was the killer’s motive?