#!/usr/bin/env python3
"""Jarvis on the Mac: serves the GitHub version at http://localhost:4180.

Safari never lets an https page (GitHub Pages) reach Ollama on http://127.0.0.1,
but a page from localhost may. This server fetches every file fresh from GitHub,
so the app stays up to date, and keeps a copy for when you are offline.
"""
import http.server
import mimetypes
import pathlib
import urllib.request

ORIGIN = "https://jannickspielt.github.io/jarvis"
PORT = 4180
CACHE = pathlib.Path.home() / "Library/Application Support/Jarvis/cache"
mimetypes.add_type("application/manifest+json", ".webmanifest")


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/") or "index.html"
        if ".." in path.split("/"):
            return self.send_error(400)
        cached = CACHE / path
        try:
            with urllib.request.urlopen(f"{ORIGIN}/{path}", timeout=5) as r:
                body = r.read()
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(body)
        except Exception:  # offline or not found online: fall back to the last copy
            if not cached.is_file():
                return self.send_error(404)
            body = cached.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(path)[0] or "application/octet-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
