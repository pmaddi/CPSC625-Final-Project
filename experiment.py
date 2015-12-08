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
zk = zkp.Zookeeper('http://6badf4c6.ngrok.io', 10000, None)


N = 1000
data = 'string'
def writes():
    print zk.create('/writes', data, None)
    for i in range(N):
        p = zk.create('/writes/' + str(i), str(data) + str(i), None)

def writes_1():
    print zk.create('/apple', 'lol ', None)

def combo():
    print zk.create('/combo', data, None)
    for i in range(N/2):
        zk.create('/combo/' + str(i), str(data) + str(i), None)
        zk.get_data('/combo/' + str(i))

def reads():
    print zk.create('/reads', data, None)
    for i in range(N):
        zk.get_data('/reads')

#print timeit.timeit(writes_1, number=1)

print "writes", timeit.timeit(writes, number=1)
print "combo", timeit.timeit(combo, number=1)
print "reads", timeit.timeit(reads, number=1)

