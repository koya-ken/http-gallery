import http.server
import socketserver

import os

PORT = 8000
def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

class Request(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print("HEAD",self.path)
        return super().do_HEAD()
    def do_GET(self):
        root_dir = 'test'
        target = self.path
        if target.startswith('/'):
            target = target[1:]
        if target.endswith('.png'):
            binary = load_binary(os.path.join(root_dir,target))
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.send_header("Cache-Control", "max-age=86400")
            self.end_headers()
            self.wfile.write(binary)
            return
        print(self.path)
        return super(Request, self).do_GET()

Handler = Request

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()