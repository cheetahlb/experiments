from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver  import ThreadingMixIn
import threading
from urllib import parse
import time
import random
import math
def busywait(t):
    start = time.monotonic()
    i=0
    while time.monotonic() -start < t:
        i = i +1
    return

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Connection", "close")
        self.end_headers()
        q = parse.urlsplit(self.path).query
        args = parse.parse_qs(q)
        fsize = 8
        duration = 0
        t = 0
        if "fsize" in args:
            fsize = float(args["fsize"][0])
        if "duration" in args:
            duration = float(args["duration"][0]) / 1000000
        if "time" in args:
            t = int(args["time"][0])
            if "time_max" in args:
                tmax = int(args["time_max"][0])
                t = random.randint(t,tmax)
            t = float(t) / 1000000
        start = time.monotonic()
        if t > 0:
            #pass
            busywait(t)
        work=0
        for i in range(int(fsize * 8)):
            self.wfile.write(bytes('ABCDE123' * 16,"ascii"))
            plan = duration * (float(i) / (fsize*8))

            elapsed = time.monotonic() - start
            #Wait t per seconds
            if duration > 0:
                if work < elapsed:
                    work += 0.1
                    busywait(0.1 * t)
        #            t = t *0.95
                elapsed = time.monotonic() - start

            if plan > elapsed:
                time.sleep(plan - elapsed)
        return

    def log_message(self, format, *args):
        return

class BigServer(HTTPServer):
    def __init__(self, server_address, rhc=Handler):
        self.request_queue_size=65536
        HTTPServer.__init__(self, server_address, rhc)


class ThreadedHTTPServer(ThreadingMixIn, BigServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 80), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    try:
        server.serve_forever()
    except BrokenPipeError:
        pass
