import collections
import pickledb
import runtime
import requests

class Znode:
# three types
    def __init__(self):
        pass
    def __init__(self, string):
        pass
    def serialize(self):
        pass



class Stat:
    pass


# the client uses this to access the server.
class Zookeeper:
    def __init__(self, connectString, sessionTimeout, watcher):
        self.connectString = connectString
        self.sessionTimeout = sessionTimeout
        self.watcher = watcher
        '''
    def __init__(self, connectString, sessionTimeout, watcher, sessionId, sessionPasswd):
        self.connectString = connectString
        self.sessionTimeout = sessionTimeout
        self.watcher = watcher
        '''
    def create(self, path, data, createMode):
        '''
        no acl
        returns actual path of created node
        '''
        data_param = {
                'command' : 'create',
                'path' : path,
                'data' : data,
                'createMode' : createMode,
                }
        r = requests.post(self.connectString, data=data_param)
        print r.url
        print 'in create', (r.status_code, r.reason, r.json())
    def delete(self, path, version):
        '''
        deletes
        '''
        data_param = {
                'command' : 'delete',
                'path' : path,
                'version' : version,
                }
        r = requests.post(self.connectString, data=data_param)
        print (r.status_code, r.reason, r.json())
    def exists(self, path, watcher):
        '''
        returns stat
        '''
        r = requests.get('http://github.com', allow_redirects=False)
        pass
    def get_data(self, path, watcher):
        '''
        returns (data, stat)
        '''
        r = requests.get('http://github.com', allow_redirects=False)
        pass
    def set_data(self, path, data, version):
        '''
        returns stat
        '''
        pass
    def get_children(self, path, watcher):
        '''
        returns (list of child paths, stat)
        '''
        pass
    def sync(self, path, callback):
        '''
        flush channel
        '''
        pass
'''
create
    creates a node at a location in the tree
delete
    deletes a node
exists
    tests if a node exists at a location
get data
    reads the data from a node
set data
    writes data to a node
get children
    retrieves a list of children of a node
sync
    waits for data to be propagated
'''


class Map:
    def __init__(self, db):
        self.db = db
        self.map_view = {}
        self.last_popped = [None]
        upcalls = (self.upcall,)
        self.runtime = runtime.Runtime(self.db, upcalls)
    def upcall(self, data):
        self.map_view[data[0]] = data[1]
    def get(self, key):
        self.runtime.play_forward(0)
        return self.map_view[key]
    def set(self, key, value):
        self.runtime.append(0, (), (key, value))

if __name__ == '__main__':
    zk = Zookeeper('http://127.0.0.1:8000', 10000, None)
    path = zk.create('/apple', 'pie', None)

