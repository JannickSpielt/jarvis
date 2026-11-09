#!/usr/bin/env python3
"""Jarvis on the Mac: serves the GitHub version at http://localhost:4180.

Safari never lets an https page (GitHub Pages) reach Ollama on http://127.0.0.1,
but a page from localhost may. This server fetches every file fresh from GitHub,
so the app stays up to date, and keeps a copy for when you are offline.

It also passes /mage-api/v1/... on to the Mage.space API, which refuses calls
made straight from a browser.
"""
import http.server
import mimetypes
import pathlib
import urllib.error
import urllib.request

ORIGIN = "https://jannickspielt.github.io/jarvis"
MAGE = "https://api.mage.space"
PORT = 4180
CACHE = pathlib.Path.home() / "Library/Application Support/Jarvis/cache"
mimetypes.add_type("application/manifest+json", ".webmanifest")


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/mage-api/v1/"):
            return self.mage()
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
        self.reply(200, mimetypes.guess_type(path)[0] or "application/octet-stream", body)

    def do_POST(self):
        if self.path.startswith("/mage-api/v1/"):
            return self.mage()
        self.send_error(404)

    def mage(self):
        # Only the Mage API, only with the caller's own key; nothing is stored here.
        if ".." in self.path:
            return self.send_error(400)
        length = int(self.headers.get("Content-Length") or 0)
        data = self.rfile.read(length) if length else None
        headers = {k: self.headers[k] for k in ("Authorization", "Content-Type", "Idempotency-Key") if self.headers.get(k)}
        req = urllib.request.Request(MAGE + self.path[len("/mage-api"):], data=data, headers=headers, method=self.command)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                self.reply(r.status, r.headers.get("Content-Type", "application/json"), r.read())
        except urllib.error.HTTPError as e:
            self.reply(e.code, e.headers.get("Content-Type", "application/json"), e.read())
        except Exception:
            self.reply(502, "application/json", b'{"error":{"code":"unreachable","message":"Mage.space ist nicht erreichbar."}}')

    def reply(self, status, ctype, body):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
