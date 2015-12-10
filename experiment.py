import zookeeper as zkp
import zookeeper_server as zkps
import timeit
import random
import sys

random.seed(10)

# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# server = HTTPServer(('', 8000), ZookeeperServer)

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

zk = zkp.Zookeeper('http://6badf4c6.ngrok.io', 10000, None)
zk = zkp.Zookeeper('http://127.0.0.1:8000', 10000, None)


N = 1000
data = 'string'
def writes():
    zk.create('/writes', data, None)
    for i in range(N):
        p = zk.create('/writes/' + str(i), str(data) + str(i), None)

def writes_1():
    zk.create('/apple', 'lol ', None)

def combo(p=.5):
    '''
    p = read workload
    returns number of writes
    '''
    q = str(random.random())
    tld = '/combo' + q
    zk.create(tld, data, None)
    j = 1
    k = 0
    for i in range(N):
        if random.random() < p:
            zk.get_data(tld)
            k += 1
        else:
            zk.create(tld + '/' + str(i), str(data) + str(i), None)
            j += 1
    return (k, j)

def reads():
    zk.create('/reads', data, None)
    for i in range(N):
        zk.get_data('/reads')

def my_time(fn, number=1):
    return timeit.timeit(fn, number=number) / N

# i = .0
# while i <= 1.0:
#     print "ratio, " + str(i) + ", " + str(my_time(wrapper(combo, i)))
#     i += .25
if __name__ == '__main__':
    rat = float(sys.argv[1])
    print "ratio, " + str(rat) + ", " + str(my_time(wrapper(combo, rat)))

