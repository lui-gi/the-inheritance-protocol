#!/usr/bin/env python3
"""Serve the Blackthorn Counsel Portal on your own machine.

Usage: python3 serve.py [port]

Needs Python 3.7 or newer and nothing else. The portal is only reachable from
this computer. Press Ctrl+C to stop.
"""
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

# The portal app lives in api/index.py so the same file also runs on Vercel.
sys.path.insert(0, str(Path(__file__).resolve().parent / "api"))

try:
    from index import app
except ImportError:
    sys.exit("Cannot find the portal app. Keep serve.py next to the 'api' folder, exactly as unzipped.")

DEFAULT_PORT = 8000


def main():
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    except ValueError:
        sys.exit("Usage: python3 serve.py [port]")

    try:
        server = make_server("127.0.0.1", port, app)
    except OSError as error:
        sys.exit(f"Could not start on port {port} ({error.strerror}). Try another one: python3 serve.py {port + 1}")

    print(f"The Counsel Portal is up at http://localhost:{port}/")
    print()
    print("Open that address in your browser and search the statements.")
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
