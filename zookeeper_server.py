import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import mimetools
import urlparse

'''
API:


'''
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

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(input_data));
        return
    '''
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('hi')
        return
    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
        except :
            pass
        '''
class Processor:
    def create():
        pass
    def delete():
        pass
    def exists():
        r = requests.get('http://github.com', allow_redirects=False)
        pass
    def get_data():
        r = requests.get('http://github.com', allow_redirects=False)
        pass
    def set_data():
        pass
    def get_children():
        pass
    def sync():
        pass

if __name__  == '__main__':
    try:
        server = HTTPServer(('', 8000), ZookeeperServer)
        print 'server started'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'server shutdown'
        server.socket.close()

