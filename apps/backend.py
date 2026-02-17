# I vibed this with ChatGPT
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "0.0.0.0"
PORT = 3000


class EchoHandler(BaseHTTPRequestHandler):
    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            return self.rfile.read(length)
        return b""

    def _parse_body(self, raw: bytes):
        content_type = self.headers.get("Content-Type", "")
        text = raw.decode("utf-8", errors="replace")

        if not text:
            return {"raw": "", "parsed": None, "byte_length": 0}

        parsed = None
        if "application/json" in content_type:
            try:
                parsed = json.loads(text)
            except Exception:
                parsed = {"_error": "Invalid JSON"}
        elif "application/x-www-form-urlencoded" in content_type:
            parsed = parse_qs(text)
        else:
            parsed = text

        return {
            "raw": text,
            "parsed": parsed,
            "byte_length": len(raw),
        }

    def _handle(self):
        # URL + query params
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        # Body
        raw_body = self._read_body()
        body_info = self._parse_body(raw_body)

        payload = {
            "method": self.command,
            "path": parsed_url.path,
            "query": query,
            "headers": dict(self.headers),
            "body": body_info,
        }

        response = json.dumps(payload, indent=2).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    # Support common verbs
    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_PUT(self):
        self._handle()

    def do_PATCH(self):
        self._handle()

    def do_DELETE(self):
        self._handle()


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), EchoHandler)
    print(f"HTTP echo server listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
