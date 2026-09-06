from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import secrets
from urllib.parse import urlparse


HOST = "localhost"
PORT = 8080

# In-memory storage
urls = {}


def generate_code(length=6):
    while True:
        code = secrets.token_urlsafe(8)[:length]
        if code not in urls:
            return code


class URLShortenerHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):
        path = urlparse(self.path).path

        # GET /
        if path == "/":
            self.send_json(200, {
                "service": "URL Shortener",
                "status": "running"
            })
            return

        # GET /<short_code>
        code = path.strip("/")

        if code not in urls:
            self.send_json(404, {
                "error": "Short URL not found"
            })
            return

        original_url = urls[code]

        self.send_response(302)
        self.send_header("Location", original_url)
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/shorten":
            self.send_json(404, {
                "error": "Endpoint not found"
            })
            return

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json(400, {
                "error": "Invalid JSON"
            })
            return

        original_url = data.get("url")

        if not original_url:
            self.send_json(400, {
                "error": "url is required"
            })
            return

        code = generate_code()

        urls[code] = original_url

        self.send_json(201, {
            "short_code": code,
            "url": f"http://{HOST}:{PORT}/{code}"
        })


def main():
    server = ThreadingHTTPServer(
        (HOST, PORT),
        URLShortenerHandler
    )

    print(f"URL Shortener running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
