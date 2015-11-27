import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import mimetools
import urlparse

import pickledb
import weakmap

db = pickledb.load('zookeeper.db', False)
zoomap = weakmap.WeakMap(db)
class ZookeeperServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('hi')
        return
    def do_POST(self):
        global rootnode
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        clength = self.headers.getheader('content-length')
        data = None
        if clength:
            try:
                bytes = int(clength)
            except ValueError:
                pass
        if bytes > 0:
            data = self.rfile.read(bytes)
        else:
            data = ""
        input_data = urlparse.parse_qs(data, keep_blank_values=1)
        out_data = {}
        print input_data
        command = input_data.get('command', None)
        if command:
            if len(command) == 1:
                command = command[0]
        if command == 'create':
            path = input_data.get('path', None)
            if path:
                if len(path) == 1:
                    path = path[0]
            data = input_data.get('data', None)
            if data:
                if len(data) == 1:
                    data = data[0]
            # check if directory avalable
            if zoomap.set(path, data):
                out_data['path'] = path
            else:
                out_data['path'] = None
        elif command == 'get_data':
            path = input_data.get('path', None)
            if path:
                if len(path) == 1:
                    path = path[0]
            # check if directory avalable
            znode = zoomap.get(path)
            if not znode:
                out_data['stat'] = None
                out_data['data'] = None
            else:
                out_data['stat'] = {'time' : 1}
                out_data['data'] = znode
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(out_data));
        return

if __name__  == '__main__':
    try:
        server = HTTPServer(('', 8000), ZookeeperServer)
        print 'server started'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'server shutdown'
        server.socket.close()
