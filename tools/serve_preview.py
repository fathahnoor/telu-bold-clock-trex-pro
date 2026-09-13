#!/usr/bin/env python3
"""Static server kecil untuk preview asset (python tools/serve_preview.py [port])."""
import http.server
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8642


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving at http://127.0.0.1:{PORT}/preview.html")
        httpd.serve_forever()
