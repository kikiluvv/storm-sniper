# redirector.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = self.path[1:] or "https://evil.com"
        self.send_response(302)
        self.send_header('Location', target)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RedirectHandler, port=9999):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"🎯 Serving redirector on http://127.0.0.1:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
