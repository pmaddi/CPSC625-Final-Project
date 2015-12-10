import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import mimetools
import urlparse
import logging
import time

import pickledb
import weakmap
import enums as e

db = pickledb.load('zookeeper.db', False)
zoomap = weakmap.WeakMap(db)

class ZookeeperServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('hi')
        return

    def log_message(self, format, *args):
        return

    def do_POST(self):
        # start timer
        start_time = time.time()
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
        logging.info(input_data)
        command = input_data.get('command', None)
        if command:
            if len(command) == 1:
                command = command[0]
        path = input_data.get('path', None)
        if path:
            if len(path) == 1:
                path = path[0]
        data = input_data.get('data', None)
        if data:
            if len(data) == 1:
                data = data[0]
        if command == 'create':
            # check if directory avalable
            if zoomap.get(path) is not None:
                out_data['path'] = path
                out_data['status'] = e.KeeperState.NODEEXISTS
            elif zoomap.set(path, data):
                out_data['path'] = path
                out_data['status'] = e.KeeperState.OK
            else:
                out_data['path'] = None
                out_data['status'] = e.KeeperState.SYSTEMERROR
        elif command == 'delete':
            if zoomap.get(path) is not None:
                zoomap.set(path, None)
                out_data['path'] = path
                out_data['status'] = e.KeeperState.OK
            elif zoomap.get(path) is None:
                out_data['path'] = path
                out_data['status'] = e.KeeperState.NONODE
            else:
                out_data['path'] = None
                out_data['status'] = e.KeeperState.SYSTEMERROR
        elif command == 'exists':
            if zoomap.get(path) is not None:
                out_data['path'] = path
                out_data['stat'] = {'time' : 1}
                out_data['status'] = e.KeeperState.OK
            else:
                out_data['path'] = None
                out_data['stat'] = None
                out_data['status'] = e.KeeperState.NONODE
        elif command == 'get_data':
            # check if directory avalable
            znode = zoomap.get(path)
            if not znode:
                out_data['stat'] = None
                out_data['data'] = None
                out_data['status'] = e.KeeperState.NONODE
            else:
                out_data['stat'] = {'time' : 1}
                out_data['data'] = znode
                out_data['status'] = e.KeeperState.OK
        elif command == 'set_data':
            znode = zoomap.get(path)
            if not znode:
                out_data['stat'] = None
                out_data['data'] = None
                out_data['status'] = e.KeeperState.SYSTEMERROR
            else:
                out_data['stat'] = {'time' : 1}
                out_data['data'] = znode
                out_data['status'] = e.KeeperState.OK
        elif command == 'get_children':
            children = zoomap.get_children(path)
            if not children:
                out_data['children'] = None
                out_data['stat'] = None
                out_data['status'] = e.KeeperState.NONODE
            else:
                out_data['children'] = children
                out_data['stat'] = {'time' : 1}
                out_data['status'] = e.KeeperState.OK
        elif command == 'sync':
            pass
        self.send_response(200)
        self.end_headers()
        logging.info("Returning {}".format(json.dumps(out_data)))
        self.wfile.write(json.dumps(out_data));
        print command + ' , ' + str(time.time() - start_time)
        return

if __name__  == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    try:
        server = HTTPServer(('', 8000), ZookeeperServer)
        logging.info('server started')
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('server shutdown')
        server.socket.close()
