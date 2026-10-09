#!/usr/bin/env python3
"""Basic web server built on Python's standard-library http.server module."""
 
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
 
HOST = "0.0.0.0"  # listen on all interfaces so the VM is reachable from outside
PORT = 8080
 
 
class RequestHandler(BaseHTTPRequestHandler):
    """Handles incoming HTTP requests. Add a do_<METHOD> method per verb you support."""
 
    def _send(self, status, body, content_type="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
 
    def do_GET(self):
        if self.path == "/":
            self._send(200, "<h1>Hello from my VM!</h1>")
        elif self.path == "/health":
            self._send(200, json.dumps({"status": "ok"}), "application/json")
        else:
            self._send(404, "<h1>404 Not Found</h1>")
 
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        self._send(200, json.dumps({"received": body}), "application/json")
 
 
def main():
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    print(f"Serving on http://{HOST}:{PORT} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()
 
 
if __name__ == "__main__":
    main()