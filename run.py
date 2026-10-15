#!/usr/bin/env python3
"""Local preview of the TryHackMe room. ORGANIZER ONLY, never ship this to players.

    python3 run.py          # http://localhost:9000/
    python3 run.py 9001     # pick another port

Serves index.html, which lays out every challenges/NN-name/task.md the way the
room will look on TryHackMe. Task text and answers are read from disk on every
request, so edit a task.md or solution.md and refresh the page.

Answers are checked here, against each task's organizer/solution.md, so no flag
ever reaches the page. Needs Python 3.7 or newer and nothing else.
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHALLENGES = ROOT / "challenges"
DEFAULT_PORT = 9000

# Entries in a task folder that players never receive.
NOT_FOR_PLAYERS = {"task.md", "build", "organizer", "__pycache__"}

# Web apps hosted on Vercel. Players open them by URL, so they are not task files.
HOSTED = {"blackthorn-portal", "counsel-portal", "case-board"}


def task_folders():
    return sorted(p for p in CHALLENGES.iterdir() if (p / "task.md").is_file())


def answers_for(folder):
    """Expected answers in question order: checkpoint answers, then the flag."""
    solution = folder / "organizer" / "solution.md"
    if not solution.is_file():
        return []
    text = solution.read_text(encoding="utf-8")
    answers = []
    checkpoint = re.search(r"^Checkpoint answers?\b.*$", text, re.MULTILINE)
    if checkpoint:
        answers += re.findall(r"`([^`]+)`", checkpoint.group(0))
    flag = re.search(r"^Flag:\s*`([^`]+)`", text, re.MULTILINE)
    if flag:
        answers.append(flag.group(1))
    return answers


def player_files(folder):
    names = []
    for entry in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if entry.name in NOT_FOR_PLAYERS or entry.name in HOSTED or entry.name.startswith("."):
            continue
        names.append(entry.name + "/" if entry.is_dir() else entry.name)
    return names


def room():
    return [
        {
            "id": folder.name,
            "markdown": (folder / "task.md").read_text(encoding="utf-8"),
            "files": player_files(folder),
            "answers": len(answers_for(folder)),
        }
        for folder in task_folders()
    ]


def check(task_id, question, answer):
    for folder in task_folders():
        if folder.name == task_id:
            expected = answers_for(folder)
            if 0 <= question < len(expected):
                return answer.strip() == expected[question]
    return False


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        self.send(status, json.dumps(data).encode("utf-8"), "application/json")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            page = (ROOT / "index.html").read_bytes()
            self.send(200, page, "text/html; charset=utf-8")
        elif path == "/api/room":
            self.send_json(200, room())
        else:
            self.send(404, b"Not found\n", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/check":
            self.send(404, b"Not found\n", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            correct = check(str(data["task"]), int(data["question"]), str(data["answer"]))
        except (ValueError, KeyError, TypeError):
            self.send_json(400, {"error": "bad request"})
            return
        self.send_json(200, {"correct": correct})

    def log_message(self, fmt, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:
        sys.exit(f"Port {port} is busy. Try another one: python3 run.py {port + 1}")
    print(f"Room preview running at http://localhost:{port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
