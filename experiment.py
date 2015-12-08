import zookeeper as zkp
import zookeeper_server as zkps
import timeit

# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# server = HTTPServer(('', 8000), ZookeeperServer)

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

zk = zkp.Zookeeper('http://127.0.0.1:8000', 10000, None)
def writes():
    print zk.create('/apple', 'lol ', None)
    for i in range(10):
        print zk.create('/apple/' + str(i), 'lol '+str(i), None)

def writes_1():
    print zk.create('/apple/1000000', 'lol ', None)

# print timeit.timeit(writes, number=1)
print timeit.timeit(writes_1, number=1)

