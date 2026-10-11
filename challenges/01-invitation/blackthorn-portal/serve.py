#!/usr/bin/env python3
"""Serve the recovered Blackthorn House portal snapshot on your own machine.

Usage: python3 serve.py [port]

Needs Python 3.7 or newer and nothing else. The site is only reachable from
this computer. Press Ctrl+C to stop.
"""
import sys
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORTAL_HOST = "portal.blackthorn.thm"
SNAPSHOT_DIR = Path(__file__).resolve().parent / PORTAL_HOST
DEFAULT_PORT = 8000


class PortalHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # The real portal never listed its folders, so the snapshot does not either.
        self.send_error(HTTPStatus.NOT_FOUND, "File not found")
        return None


def main():
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    except ValueError:
        sys.exit("Usage: python3 serve.py [port]")

    if not SNAPSHOT_DIR.is_dir():
        sys.exit(f"Cannot find the '{PORTAL_HOST}' folder. Keep serve.py next to it, exactly as unzipped.")

    handler = partial(PortalHandler, directory=str(SNAPSHOT_DIR))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError as error:
        sys.exit(f"Could not start on port {port} ({error.strerror}). Try another one: python3 serve.py {port + 1}")

    print(f"The portal snapshot is up at http://localhost:{port}/")
    print()
    print(f"Any address on http://{PORTAL_HOST}/ now lives on http://localhost:{port}/ instead.")
    print("Keep the rest of the address exactly the same.")
    print()
    print("Press Ctrl+C to stop.")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Portal stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
