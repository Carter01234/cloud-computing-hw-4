#!/usr/bin/env python3
"""Basic web server built on Python's standard-library http.server module."""
 
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote
from google.cloud import logging as cloud_logging
from google.api_core.exceptions import NotFound
from google.cloud import storage
import mimetypes
import logging

# setting up logging to work with google cloud
client = cloud_logging.Client()
client.setup_logging()

storage_client = storage.Client()


BUCKET_NAME = "html-files-for-class"
PREFIX = "pages"
HOST = "0.0.0.0"  # listen on all interfaces so the VM is reachable from outside
PORT = 8080


def get_file_from_bucket(filename: str) -> None | bytes: 
    blob = storage_client.bucket(BUCKET_NAME).blob(f'{PREFIX}/{filename}')
    try:
        return blob.download_as_bytes()
    except NotFound:
        print(f"The filename {filename} does not exist in GCS")

        logging.warning(
            f"File not found: {filename}",
            extra={"json_fields": {"status": 404, "filename": filename}},
        )

        return None
 
 
class RequestHandler(BaseHTTPRequestHandler):
    """Handles incoming HTTP requests. Add a do_<METHOD> method per verb you support."""
 
    def _send(self, status, body, content_type="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
 
    def do_GET(self):
        filename = unquote(urlsplit(self.path).path).lstrip("/")
        contents = get_file_from_bucket(filename)
        if contents is None:
            self._send(404, f"File not found: {filename}\n") 
        else: 
            content_type = mimetypes.guess_type(filename)[0] or "text/plain"
            self._send(200, contents, content_type)
 
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