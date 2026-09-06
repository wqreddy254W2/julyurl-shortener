from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import path
from os import path
from config import HOST, PORT
from storage import URLStorage
from cache import Cache
from rate_limiter import RateLimiter
from statistics import Statistics 
from http.server import BasedHTTPRequestHandler, ThreadingHTTPServer
from models import URLRecord
from statistics import Statistics  
from storage import URLStorage
import json
import secrets
from urllib.parse import urlparse

from cache import Cache
from config import(
    HOST,
    PORT,
    SHORT_CODE_LENGTH,
    CACHE_TTL_SECONDS,
    RATE_LIMIT,
    RATE_WINDOW_SECONDS,
    MAX_URL_LENGTH
)
HOST = "localhost"
PORT = 8080

# In-memory storage
storage=URLStorage()
cache=Cache(CACHE_TTL_SECONDS)
rate_limiter=RateLimiter(RATE_LIMIT, RATE_WINDOW_SECONDS)
statistics=Statistics()


def generate_code(length=6):
    while True:
        code = secrets.token_urlsafe(8)[:SHORT_CODE_LENGTH]
         
        if not storage.exists(code):
            return code

def is_valid_url(url):
    if not isinstance(url,str):
        return False
    
    if len(url)>MAX_URL_LENGTH:
        return False
    
    parsed = urlparse(url)
   
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

class URLShortenerHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)
    
    def client_id(self):
        return self.client_address[0]

    def do_GET(self):
        if not rate_limiter.allow(self.client_id()):
            statistics.increment_rate_limited()
            
            self.send_json(429,{
                "error":"rate limit exceeded"
            })
            return
            
            path = urlparse(self.path).path

        # GET /
            if path == "/":
              self.send_json(200, {
                "service": "URL Shortener",
                "status": "running"
            })
            return

            if path=="/status":
                self.send_json(200, statistics.snapshot())
                return
            

        # GET /<short_code>
            code = path.strip("/")

            if not code:
                self.send_json(404, {
                "error": "Short URL not found"
            })
            return

            record=cache.get(code)
            
            if record is not None:
                statistics.increment_cache_hits()
            else:
               statistics.increment_cache_misses()

            record=storage.get(code)
            
            if record is None:
                     self.send_json(404, {
                         "error":"short URL not found"
                         }) 
                     return
        # self.send_response(302)
        # self.send_header("Location", original_url)
        # self.end_headers()
            cache.set(code,record)
            if(
                record.expires_at is not None and 
                datetime.now()>=record.expires_at
            ):
                cache.delete(code)
                self.send_json(404, {
                    "error":"short URL not found"
                })
                return
        
        statistics.increment_redirects()
        
        self.send_response(302)
        self.send_header("Location", record.original_url)
        self.end_headers()
        
            
    def do_POST(self):
        if not rate_limiter.allow(self.client_id()):
            statistics. increment_rate_limited()
            self.send_json(429,{
                "error":"rate limit exceeded"
            })
            return
        
        path = urlparse(self.path).path

        if path != "/shorten":
            self.send_json(404, {
                "error": "Endpoint not found"
            })
            return
    
    
        try:
              content_length = int(
                  self.headers.get("Content-Length", 0)
                  )
        except ValueError:
            self.send_json(400,{
                "error":"invalid content length"
            })
        if content_length <=0 :
            self.send_json(400, {
              "error":"request body is required"
        })
        return 

        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json(400, {
                "error": "Invalid JSON"
            })
            return

        original_url = data.get("url")

        if not is_valid_url(original_url):
            self.send_json(400, {
                "error": "Invalid URL"
            })
            return

        code = generate_shortcode()
        # urls[code] = original_url
        record=URLRecord(
            short_code=code,
            original_url=original_url,
            created_at=datetime.now(),
        )
        
        storage.save(record)
        cache.set(code, record)
        
        statistics.increment_urls_created()
        
        self.send_json(201, {
            "short_code": code,
            "url": f"http://{HOST}:{PORT}/{code}"
        })


def main():
    server = ThreadingHTTPServer(
        (HOST, PORT),
        URLShortenerHandler,
    )

    print(f"URL Shortener running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cache.clear()
        server.server_close()
        print("server stopped.")


if __name__ == "__main__":
    main()
