#!/usr/bin/env python3
"""Generate the house server snapshot handed to players in the Ghost Admin task.

Usage: make_server.py [output_dir]

Writes the snapshot tree under blackthorn-server/ (account files, six months of auth.log,
three home folders, Adrian's sealed findings.zip, and scenery system files), plus a plaintext copy of the sealed
findings under organizer/ that is never distributed.

Standard library only. The build is reproducible: the filler logins come from a seeded
generator, and the zip is written here by hand (legacy ZipCrypto, which Windows Explorer
can open) so that its bytes do not depend on the local zip tool.

Values below must stay in sync with canon/canon.md.
"""
import random
import struct
import sys
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

FLAG = "THM{RED_HERRING_ROOT}"
TZ = timezone(timedelta(hours=-4))  # the whole log falls inside daylight time
HOST = "blackthorn-srv"
GHOST = "hvac-sync"  # Marcus's hidden second root account
LAST_USED = "2026-10-29"  # the ghost's final login. Also the zip password.

IP_ADRIAN = "10.13.0.10"
IP_MARCUS = "10.13.0.22"  # the ghost only ever logs in from here
IP_THEO = "10.13.0.31"
IP_NOISE = "10.13.0.77"

UID = {"a.vale": 1001, "m.vale": 1002, "t.grant": 1003, "svc-backup": 997, GHOST: 0}

LOG_START = datetime(2026, 5, 1, tzinfo=TZ)
HALLOWEEN = datetime(2026, 10, 31, tzinfo=TZ)
SEALED = datetime(2026, 10, 30, 21, 40, 0)  # Adrian seals his findings

TASK_DIR = Path(__file__).resolve().parent.parent
SNAPSHOT = "blackthorn-server"

README = """\
BLACKTHORN HOUSE SERVER: EVIDENCE SNAPSHOT
==========================================

This folder is a copy of part of the house server, "blackthorn-srv", taken by
the investigation at 01:25 on 1 November 2026. It is only files. Nothing here
runs, and nothing here touches the internet.

It is laid out the way the server was, so paths look like Linux paths:

  etc/passwd          Every account on the server, one per line.
  etc/group           Which accounts belong to which groups.
  var/log/auth.log    Every login and admin command since 1 May 2026.
  home/               Files from the three people who had a login here.

The rest (boot, opt, usr, the other files in etc and var) is the ordinary
furniture of a Linux server: settings, scripts, and smaller logs. You are
welcome to look around. Some folders begin with nothing but a dot-file, so
use "ls -a" if a folder looks empty.


READING etc/passwd
------------------

Each line is one account, with fields separated by colons:

  name : x : user ID : group ID : description : home folder : shell

The user ID is the number that matters. The system decides what an account
may do by its number, not its name.


SEARCHING
---------

The log is far too long to read. Search it instead.

  Linux, macOS, AttackBox:

    grep "something" var/log/auth.log       search one file
    grep -r "something" .                   search every file in this folder

  Windows (PowerShell):

    Select-String "something" var\\log\\auth.log
    Get-ChildItem -Recurse -File | Select-String "something"

Any editor with "find in files" works just as well.

All times in the log are local house time (UTC-04:00).
"""

PASSWD = f"""\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver:/run/systemd:/usr/sbin/nologin
messagebus:x:102:105::/nonexistent:/usr/sbin/nologin
sshd:x:103:65534::/run/sshd:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
mosquitto:x:105:111:Mosquitto MQTT Broker:/var/lib/mosquitto:/usr/sbin/nologin
{GHOST}:x:0:0:HVAC Sync Service:/var/lib/{GHOST}:/bin/bash
blackthorn-hub:x:998:998:Blackthorn Hub:/var/lib/blackthorn-hub:/usr/sbin/nologin
svc-backup:x:997:997:Nightly Backup:/var/lib/svc-backup:/usr/sbin/nologin
a.vale:x:1001:1001:Adrian Vale:/home/a.vale:/bin/bash
m.vale:x:1002:1002:Marcus Vale:/home/m.vale:/bin/bash
t.grant:x:1003:1003:Theo Grant:/home/t.grant:/bin/bash
"""

GROUP = """\
root:x:0:
daemon:x:1:
adm:x:4:syslog,a.vale
sudo:x:27:a.vale,m.vale
www-data:x:33:
backup:x:34:
ssh:x:110:
mosquitto:x:111:
blackthorn-hub:x:998:
svc-backup:x:997:
a.vale:x:1001:
m.vale:x:1002:
t.grant:x:1003:
nogroup:x:65534:
"""

ADRIAN_NOTE = f"""\
AUDIT NOTE
30 October 2026
Subject: the account called {GHOST}

This house has no HVAC sync service. I designed the heating myself. It syncs
with nothing, and it resents being asked.

{GHOST} is a second root account wearing a boiler suit. Look at its user ID
in /etc/passwd. My son made it, and auth.log will tell you the night he did.

I have known since June. I left it alone because I wanted to see what he
would do with it. So far he restarts things, and reads logs he was allowed
to read anyway.

I check on it every day. Tonight I wrote down what I think it means and
sealed it in findings.zip, beside this note.

The password is the date {GHOST} was last used, written the way the log
writes it: YYYY-MM-DD.

If you are reading this and I am not available to gloat, do one thing before
you open it. Check that the date is still the last one.

A.V.
"""

FINDINGS = f"""\
FINDINGS
Sealed 30 October 2026

If this opened, you know when {GHOST} was last used. Good. Hold on to that
date, because somebody will try to talk you out of it.

Here is what is true. The account is real. Marcus built it in secret, it can
do anything on this server, and it breaks every rule I ever wrote for this
family. He is guilty of exactly that, and he will be hearing about it.

Here is what is also true. An account does nothing while nobody is using it.
A login leaves a line in the log, and no line means no login. If something
has happened in this house, look at that night before you look at my son.
If {GHOST} is not there, it did not do it.

A secret is not the same thing as a crime. Whoever points you at this
account is either a poor reader of logs or is hoping that you are.

{FLAG}

A.V.

P.S. Marcus, if it is you reading this: we need to talk. Bring the thermostat.
"""

MARCUS_TODO = f"""\
TODO (Marcus)

- Porch sensor is counting pumpkins again. Teach it what a pumpkin is.
- Wine cellar lock battery. Still 18 percent. Somehow.
- Renew the hub certificate before it expires and Dad notices.
- Remove {GHOST} before Dad's next audit. He will never find it, but still.
- Tell nobody about {GHOST}.
"""

THEO_ROTA = """\
HALLOWEEN DINNER, STAFF ROTA (T. Grant)

Grounds:  07:00 until late afternoon. Pumpkins on the porch by 16:00.
Kitchen:  09:00 until the last plate is washed.
Guests:   19:00, front door. I will let them in myself.
Dinner:   19:30. Dessert 21:30.

Do not let Mr Vale near the organ music settings again.
"""

BASHRC = """\
# ~/.bashrc
case $- in
    *i*) ;;
      *) return;;
esac
HISTCONTROL=ignoreboth
HISTSIZE=1000
PS1='\\u@\\h:\\w\\$ '
alias ll='ls -alF'
"""

PROFILE = """\
# ~/.profile
if [ -n "$BASH_VERSION" ] && [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
fi
PATH="$HOME/bin:$PATH"
"""

# Scenery: ordinary system files so the snapshot reads like a real server. None of it is
# part of the solve path, and none of it may mention the ghost account or the flag.
SCENERY = {
    "etc/os-release": """\
PRETTY_NAME="Ubuntu 24.04.2 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.2 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
""",
    "etc/hosts": f"""\
127.0.0.1   localhost
127.0.1.1   {HOST}
10.13.0.1   gateway
10.13.0.2   {HOST}
""",
    "etc/timezone": "America/New_York\n",
    "etc/shells": "# /etc/shells: valid login shells\n/bin/sh\n/bin/bash\n/usr/bin/bash\n/usr/sbin/nologin\n",
    "etc/resolv.conf": "nameserver 10.13.0.1\nsearch blackthorn.thm\n",
    "etc/motd": """\

  BLACKTHORN HOUSE SERVER

  Everything you type here is logged.
  Everything you do not type here is suspected.

  A.V.

""",
    "etc/fstab": """\
# <file system>  <mount point>  <type>  <options>          <dump>  <pass>
/dev/sda2        /              ext4    errors=remount-ro  0       1
/dev/sda1        /boot          ext4    defaults           0       2
/dev/sdb1        /var/backups   ext4    defaults,noatime   0       2
/swapfile        none           swap    sw                 0       0
""",
    "etc/crontab": """\
# /etc/crontab: system-wide crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m  h  dom mon dow user        command
17 *  *   *   *   root        cd / && run-parts --report /etc/cron.hourly
25 6  *   *   *   root        test -x /usr/sbin/anacron || run-parts --report /etc/cron.daily
""",
    "etc/cron.d/svc-backup": "# Nightly backup of the hub configuration and logs\n30 2 * * * svc-backup /usr/local/bin/backup.sh\n",
    "etc/sudoers": """\
# This file MUST be edited with the 'visudo' command as root.
Defaults        env_reset
Defaults        mail_badpass
Defaults        logfile=/var/log/auth.log

root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
""",
    "etc/ssh/sshd_config": """\
# Blackthorn House server: sshd configuration
Port 22
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication yes
KbdInteractiveAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
""",
    "etc/mosquitto/mosquitto.conf": """\
# Message broker for the house sensors
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
listener 1883 10.13.0.2
allow_anonymous false
""",
    "etc/systemd/system/blackthorn-hub.service": """\
[Unit]
Description=Blackthorn Hub (doors, lights, sensors)
After=network-online.target mosquitto.service

[Service]
User=blackthorn-hub
ExecStart=/opt/blackthorn-hub/bin/hub --config /opt/blackthorn-hub/config.yaml
Restart=on-failure

[Install]
WantedBy=multi-user.target
""",
    "opt/blackthorn-hub/VERSION": "4.1.2\n",
    "opt/blackthorn-hub/config.yaml": """\
# Blackthorn Hub configuration
house: Blackthorn House
timezone: America/New_York

doors:
  - FRONT-DOOR
  - SERVICE-ENTRANCE
  - GARAGE
  - GATEHOUSE
  - WINE-CELLAR
  - SERVER-ROOM
  - STUDY
  - LIBRARY
  - CONSERVATORY

autolock_seconds: 30
log_rotation: daily

scenes:
  dinner:
    dining_room_lights: 40
    music: organ
  lockdown:
    seal_exterior_doors: true

# Paired devices are kept in the hub database, which is not part of this snapshot.
""",
    "opt/blackthorn-hub/CHANGELOG.txt": """\
4.1.2  Porch sensor no longer reports the postman as "recurring intruder".
4.1.1  Wine cellar battery reading fixed. (It was not fixed.)
4.1.0  Lockdown scene added at the owner's request.
4.0.0  Rewrite. Doors now relock themselves.
""",
    "usr/local/bin/backup.sh": """\
#!/bin/sh
# Nightly backup, run by cron as svc-backup.
set -e
STAMP=$(date +%Y-%m-%d)
tar -czf "/var/backups/hub-$STAMP.tar.gz" /opt/blackthorn-hub/config.yaml /var/log
echo "$(date -Iseconds) backup ok hub-$STAMP.tar.gz" >> /var/log/backup.log
find /var/backups -name 'hub-*.tar.gz' -mtime +14 -delete
""",
    "usr/local/bin/pumpkin-count.sh": """\
#!/bin/sh
# Asks the porch sensor how many pumpkins it can see. Seasonal.
mosquitto_sub -h 10.13.0.2 -t house/porch/objects -C 1 | grep -c pumpkin
""",
    "var/log/backup.log": "".join(
        f"2026-10-{day}T02:3{minute}-04:00 backup ok hub-2026-10-{day}.tar.gz\n"
        for day, minute in (("25", "1:52"), ("26", "2:10"), ("27", "1:47"), ("28", "2:31"), ("29", "1:58"), ("30", "2:05"), ("31", "2:44"))),
    "var/log/dpkg.log": """\
2026-04-18 10:41:07 status installed openssh-server:amd64 1:9.6p1-3ubuntu13.5
2026-04-18 10:44:52 status installed mosquitto:amd64 2.0.18-1build3
2026-04-18 10:45:30 status installed rsyslog:amd64 8.2312.0-3ubuntu9
2026-07-02 09:12:11 status installed openssl:amd64 3.0.13-0ubuntu3.5
2026-09-14 09:03:48 status installed tzdata:all 2026a-0ubuntu0.24.04
""",
    "var/log/syslog": f"""\
2026-10-31T19:30:00-04:00 {HOST} blackthorn-hub[812]: scene "dinner" active
2026-10-31T22:19:03-04:00 {HOST} blackthorn-hub[812]: scene "lockdown" active
2026-10-31T22:19:41-04:00 {HOST} systemd-networkd[604]: eth0: Lost carrier
2026-10-31T22:35:01-04:00 {HOST} systemd[1]: Restarting systemd-networkd.service
2026-10-31T22:35:02-04:00 {HOST} systemd-networkd[19410]: eth0: Link DOWN
2026-10-31T23:39:57-04:00 {HOST} systemd[1]: Restarting systemd-networkd.service
2026-10-31T23:39:58-04:00 {HOST} systemd-networkd[19688]: eth0: Link DOWN
""",
    "var/log/mosquitto/mosquitto.log": f"""\
2026-10-31T16:40:03-04:00 house/porch/objects: pumpkin x14
2026-10-31T17:41:30-04:00 mosquitto version 2.0.18 starting
2026-10-31T17:41:31-04:00 Opening ipv4 listen socket on port 1883.
2026-10-31T22:19:41-04:00 Socket error on client porch-sensor, disconnecting.
""",
    "var/www/html/index.html": """\
<!DOCTYPE html>
<html>
<head><title>blackthorn-srv</title></head>
<body>
<h1>It works.</h1>
<p>There is nothing to see on this page. The portal lives elsewhere.</p>
</body>
</html>
""",
    "var/backups/README.txt": "Backup archives live on a separate disk and were not copied into this snapshot.\n",
    "boot/grub/grub.cfg": """\
set default=0
set timeout=3
menuentry 'Ubuntu' {
    linux /vmlinuz root=/dev/sda2 ro quiet
    initrd /initrd.img
}
""",
    "tmp/README.txt": "Temporary files were not copied into this snapshot.\n",
    "root/.bashrc": BASHRC,
    "root/.profile": PROFILE,
    "home/a.vale/.bashrc": BASHRC + "alias trust='sha256sum'\n",
    "home/a.vale/.profile": PROFILE,
    "home/m.vale/.bashrc": BASHRC + "alias hublog='journalctl -u blackthorn-hub'\n",
    "home/m.vale/.profile": PROFILE,
    "home/t.grant/.bashrc": BASHRC,
    "home/t.grant/.profile": PROFILE,
}

# The ghost's sessions: (start, minutes). The first is the night it was created.
GHOST_SESSIONS = [
    ("2026-05-12 23:52:30", 6),
    ("2026-05-30 22:15:04", 21),
    ("2026-06-21 23:40:17", 12),
    ("2026-07-04 21:05:48", 33),
    ("2026-08-09 22:31:26", 15),
    ("2026-09-02 23:10:09", 9),
    ("2026-09-27 21:47:52", 27),
    ("2026-10-11 22:20:35", 14),
    (f"{LAST_USED} 23:12:40", 18),
]

MARCUS_SUDO = [
    "/usr/bin/systemctl restart blackthorn-hub",
    "/usr/bin/systemctl status blackthorn-hub",
    "/usr/bin/journalctl -u blackthorn-hub",
    "/usr/bin/systemctl restart mosquitto",
    "/usr/bin/apt update",
    "/usr/bin/tail -n 200 /var/log/syslog",
]
ADRIAN_SUDO = [
    "/usr/bin/less /var/log/auth.log",
    "/usr/bin/grep -c Accepted /var/log/auth.log",
    "/usr/bin/lastlog",
]


class Log:
    def __init__(self, rng):
        self.rng = rng
        self.lines = []
        self.processes = 0

    def next_pid(self):
        """Hand out a placeholder. Real process IDs are assigned in time order by text()."""
        self.processes += 1
        return f"<pid{self.processes}>"

    def add(self, when, proc, pid, message):
        self.lines.append((when, f"{when.isoformat(timespec='seconds')} {HOST} {proc}[{pid}]: {message}"))

    def sudo(self, when, user, command):
        self.lines.append((when, f"{when.isoformat(timespec='seconds')} {HOST} sudo:   {user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND={command}"))

    def ssh(self, start, minutes, user, ip, method="publickey", commands=()):
        pid = self.next_pid()
        end = start + timedelta(minutes=minutes, seconds=self.rng.randrange(60))
        self.add(start, "sshd", pid, f"Accepted {method} for {user} from {ip} port {self.rng.randint(40000, 60999)} ssh2")
        self.add(start, "sshd", pid, f"pam_unix(sshd:session): session opened for user {user}(uid={UID[user]}) by (uid=0)")
        for index, command in enumerate(commands, start=1):
            self.sudo(start + (end - start) * index / (len(commands) + 1), user, command)
        self.add(end, "sshd", pid, f"pam_unix(sshd:session): session closed for user {user}")

    def console(self, start, end, user, commands=()):
        pid = self.next_pid()
        self.add(start, "login", pid, f"pam_unix(login:session): session opened for user {user}(uid={UID[user]}) by LOGIN(uid=0)")
        self.add(start, "login", pid, f"LOGIN ON tty1 BY {user}")
        for index, command in enumerate(commands, start=1):
            when = start + (end - start) * index / (len(commands) + 1)
            self.lines.append((when, f"{when.isoformat(timespec='seconds')} {HOST} sudo:   {user} : TTY=tty1 ; PWD=/home/{user} ; USER=root ; COMMAND={command}"))
        self.add(end, "login", pid, f"pam_unix(login:session): session closed for user {user}")

    def cron(self, day):
        pid = self.next_pid()
        start = day + timedelta(hours=2, minutes=30, seconds=1)
        self.add(start, "CRON", pid, f"pam_unix(cron:session): session opened for user svc-backup(uid={UID['svc-backup']}) by (uid=0)")
        self.add(start + timedelta(seconds=self.rng.randint(40, 190)), "CRON", pid, "pam_unix(cron:session): session closed for user svc-backup")

    def text(self):
        self.lines.sort(key=lambda line: line[0])  # stable, so lines sharing a second keep their order
        pids, last = {}, 1200
        out = []
        for _, line in self.lines:
            if "[<pid" in line:
                placeholder = line[line.index("[<pid") + 1:line.index(">]") + 1]
                if placeholder not in pids:
                    last += self.rng.randint(3, 60)
                    pids[placeholder] = str(last)
                line = line.replace(placeholder, pids[placeholder])
            out.append(line + "\n")
        return "".join(out)


def local(text):
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ)


def build_auth_log():
    rng = random.Random(1031)
    log = Log(rng)

    # Six months of ordinary life. Halloween itself is fully scripted further down.
    day = LOG_START
    while day < HALLOWEEN:
        log.cron(day)
        if rng.random() < 0.85:
            for _ in range(rng.choice((1, 1, 2))):
                start = day + timedelta(seconds=rng.randrange(8 * 3600, 23 * 3600))
                log.ssh(start, rng.randint(4, 70), "m.vale", IP_MARCUS, commands=rng.sample(MARCUS_SUDO, rng.randint(0, 2)))
        if rng.random() < 0.4:
            start = day + timedelta(seconds=rng.randrange(7 * 3600, 21 * 3600))
            log.ssh(start, rng.randint(5, 25), "a.vale", IP_ADRIAN, commands=rng.sample(ADRIAN_SUDO, rng.randint(1, 2)))
        if rng.random() < 0.15 and day >= local("2026-05-05 00:00:00"):
            start = day + timedelta(seconds=rng.randrange(9 * 3600, 18 * 3600))
            log.ssh(start, rng.randint(2, 10), "t.grant", IP_THEO, method="password")
        if rng.random() < 0.08:
            start = day + timedelta(seconds=rng.randrange(86400))
            for attempt, name in enumerate(rng.sample(["admin", "pi", "test", "ubnt", "oracle", "guest"], rng.randint(2, 4))):
                pid = log.next_pid()
                log.add(start + timedelta(seconds=3 * attempt), "sshd", pid, f"Failed password for invalid user {name} from {IP_NOISE} port {rng.randint(40000, 60999)} ssh2")
        day += timedelta(days=1)

    # Theo's account: created openly by Adrian. A fair comparison for what follows.
    when = local("2026-05-04 10:02:11")
    log.ssh(when - timedelta(minutes=3), 9, "a.vale", IP_ADRIAN)
    log.sudo(when, "a.vale", "/usr/sbin/useradd -m -s /bin/bash -c Theo Grant t.grant")
    log.add(when, "useradd", log.next_pid(), "new user: name=t.grant, UID=1003, GID=1003, home=/home/t.grant, shell=/bin/bash, from=/dev/pts/0")
    log.add(when + timedelta(seconds=19), "passwd", log.next_pid(), "pam_unix(passwd:chauthtok): password changed for t.grant")

    # Marcus creates the ghost, late at night, then tries it out.
    when = local("2026-05-12 23:48:09")
    log.ssh(when - timedelta(minutes=6), 11, "m.vale", IP_MARCUS)
    log.sudo(when, "m.vale", f"/usr/sbin/useradd -o -u 0 -g 0 -M -d /var/lib/{GHOST} -s /bin/bash -c HVAC Sync Service {GHOST}")
    log.add(when, "useradd", log.next_pid(), f"new user: name={GHOST}, UID=0, GID=0, home=/var/lib/{GHOST}, shell=/bin/bash, from=/dev/pts/0")
    log.add(when + timedelta(seconds=24), "passwd", log.next_pid(), f"pam_unix(passwd:chauthtok): password changed for {GHOST}")
    for start, minutes in GHOST_SESSIONS:
        log.ssh(local(start), minutes, GHOST, IP_MARCUS, method="password")

    # The evening Adrian seals his findings.
    log.ssh(local("2026-10-30 21:27:44"), 16, "a.vale", IP_ADRIAN, commands=["/usr/bin/lastlog", "/usr/bin/less /var/log/auth.log"])

    # Halloween. Marcus's console sessions follow his phone's server room unlocks in the Smart Lock task.
    log.cron(HALLOWEEN)
    log.ssh(local("2026-10-31 09:12:40"), 27, "m.vale", IP_MARCUS, commands=["/usr/bin/systemctl status blackthorn-hub"])
    log.ssh(local("2026-10-31 14:05:16"), 14, "a.vale", IP_ADRIAN, commands=["/usr/bin/less /var/log/auth.log"])
    log.ssh(local("2026-10-31 17:30:02"), 22, "m.vale", IP_MARCUS, commands=["/usr/bin/systemctl restart mosquitto"])
    log.console(local("2026-10-31 19:54:10"), local("2026-10-31 20:06:33"), "m.vale")
    log.console(local("2026-10-31 22:03:31"), local("2026-10-31 22:15:48"), "m.vale", ["/usr/bin/journalctl -u blackthorn-hub"])
    log.console(local("2026-10-31 22:22:04"), local("2026-10-31 22:41:30"), "m.vale",
                ["/usr/bin/systemctl status systemd-networkd", "/usr/bin/systemctl restart systemd-networkd"])
    log.console(local("2026-10-31 22:48:22"), local("2026-10-31 23:11:09"), "m.vale", ["/usr/bin/journalctl -u systemd-networkd"])
    log.console(local("2026-10-31 23:27:15"), local("2026-10-31 23:52:40"), "m.vale", ["/usr/bin/systemctl restart systemd-networkd"])
    return log.text()


def check(auth_log, files):
    ghost_lines = [line for line in auth_log.splitlines() if GHOST in line]
    assert ghost_lines[-1].startswith(LAST_USED) and "session closed" in ghost_lines[-1]
    assert not any(line.startswith(("2026-10-30", "2026-10-31", "2026-11")) for line in ghost_lines)
    assert sum("Accepted password for " + GHOST in line for line in ghost_lines) == len(GHOST_SESSIONS)
    assert all(IP_MARCUS in line for line in ghost_lines if "Accepted" in line)
    assert auth_log.count("new user:") == 2
    assert not any("THM{" in text for text in files.values())
    assert sorted(path for path, text in files.items() if GHOST in text) == [
        "etc/passwd", "home/a.vale/audit/hvac-sync.txt", "home/m.vale/TODO.txt", "var/log/auth.log"]


def zipcrypto(data, password, crc, rng):
    """Encrypt with the legacy PKWARE stream cipher, including its 12-byte header."""
    table = []  # raw CRC-32 table
    for i in range(256):
        for _ in range(8):
            i = (i >> 1) ^ 0xEDB88320 if i & 1 else i >> 1
        table.append(i)
    keys = [0x12345678, 0x23456789, 0x34567890]

    def update(byte):
        keys[0] = (keys[0] >> 8) ^ table[(keys[0] ^ byte) & 0xFF]
        keys[1] = ((keys[1] + (keys[0] & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        keys[2] = (keys[2] >> 8) ^ table[(keys[2] ^ (keys[1] >> 24)) & 0xFF]

    for byte in password:
        update(byte)
    header = bytes(rng.randrange(256) for _ in range(11)) + bytes([crc >> 24])  # last byte lets tools test the password
    out = bytearray()
    for byte in header + data:
        temp = keys[2] | 2
        out.append(byte ^ (((temp * (temp ^ 1)) >> 8) & 0xFF))
        update(byte)
    return bytes(out)


def build_zip(name, content, password):
    rng = random.Random(1029)
    crc = zlib.crc32(content)
    deflater = zlib.compressobj(9, zlib.DEFLATED, -15)
    body = zipcrypto(deflater.compress(content) + deflater.flush(), password.encode("ascii"), crc, rng)
    dos_time = SEALED.hour << 11 | SEALED.minute << 5 | SEALED.second // 2
    dos_date = (SEALED.year - 1980) << 9 | SEALED.month << 5 | SEALED.day
    encoded = name.encode("ascii")
    # version 2.0, flag bit 0 (encrypted), deflate
    common = struct.pack("<HHHHHIIIHH", 20, 0x0001, 8, dos_time, dos_date, crc, len(body), len(content), len(encoded), 0)
    local_header = b"PK\x03\x04" + common + encoded
    central = b"PK\x01\x02" + struct.pack("<H", 20) + common + struct.pack("<HHHII", 0, 0, 0, 0x20, 0) + encoded
    end = b"PK\x05\x06" + struct.pack("<HHHHIIH", 0, 0, 1, 1, len(central), len(local_header) + len(body), 0)
    return local_header + body + central + end


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else TASK_DIR
    auth_log = build_auth_log()
    files = {
        "README.txt": README,
        "etc/passwd": PASSWD,
        "etc/group": GROUP,
        "etc/hostname": HOST + "\n",
        "var/log/auth.log": auth_log,
        "home/a.vale/audit/hvac-sync.txt": ADRIAN_NOTE,
        "home/m.vale/TODO.txt": MARCUS_TODO,
        "home/t.grant/staff-rota.txt": THEO_ROTA,
        **SCENERY,
    }
    check(auth_log, files)

    outputs = {out / SNAPSHOT / path: text.encode("ascii") for path, text in files.items()}
    outputs[out / SNAPSHOT / "home/a.vale/audit/findings.zip"] = build_zip("findings.txt", FINDINGS.encode("ascii"), LAST_USED)
    outputs[out / "organizer" / "findings.txt"] = FINDINGS.encode("ascii")
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
