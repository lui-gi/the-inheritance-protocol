# The Smart Lock

Every door in Blackthorn House keeps a diary. Adrian Vale insisted on it. He said a door that cannot remember who opened it is just a wall with ambitions.

The library door remembers this much: a few minutes before Adrian was found, it was opened by Marcus Vale's account. Marcus says it was not him. Marcus also says he has never once touched the thermostat, so we are keeping an open mind.

Download the task file and unzip it. You will find:

- `lock-controller.log`, the hub's record of every door in the house on Halloween
- `device-record.zip`, a sealed record the hub made for one particular device

Start with the log. Find the moment the library opened, and look closely at what did the opening. The hub noticed something odd about it too, and said so.

The zip is locked. Its password is the ID of the device that opened the library, typed exactly as the log writes it.

A few pointers:

- The log is plain text. Open it in any editor, or search it with `grep`. Adrian was found at 10:17 PM, which the log writes as `22:17`.
- Each door line names two things: an account and a device. They are not the same thing, and tonight that matters.
- Marcus opened a lot of doors on Halloween. Check whether he always used the same thing to do it.
- Once the zip is open, read the record inside from top to bottom. It is short, and it knows whose device this is.

## Questions

1. What is the ID of the device that opened the library door just before Adrian was found?

   Answer format: `BH-***-****`

2. What is the flag in the sealed device record?

   Answer format: `THM{...}`
