import collections
import pickledb
import runtime
import requests
import logging

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
    def __init__(self, connectString, sessionTimeout, watcher=None):
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
        if r.status_code == 200:
            return r.json().get('path', None)
        else:
            return None

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
        if r.status_code == 200:
            return True
        else:
            return None

    def exists(self, path, watcher=None):
        '''
        returns stat
        '''
        data_param = {
                'command' : 'exists',
                'path' : path,
                }
        r = requests.post(self.connectString, data=data_param)
        if r.status_code == 200:
            return r.json().get('stat', None)
        else:
            return None

    def get_data(self, path, watcher=None):
        '''
        returns (data, stat)
        '''
        data_param = {
                'command' : 'get_data',
                'path' : path,
                }
        r = requests.post(self.connectString, data=data_param)
        if r.status_code == 200:
            return (r.json().get('data', None), r.json().get('stat', None))
        else:
            return None
    def set_data(self, path, data, version):
        '''
        returns stat
        '''
        data_param = {
                'command' : 'set_data',
                'path' : path,
                'data' : data,
                }
        r = requests.post(self.connectString, data=data_param)
        if r.status_code == 200:
            return r.json().get('stat', None)
        else:
            return None
    def get_children(self, path, watcher=None):
        '''
        returns (list of child paths, stat)
        '''
        data_param = {
                'command' : 'get_children',
                'path' : path,
                }
        r = requests.post(self.connectString, data=data_param)
        if r.status_code == 200:
            return (r.json().get('children', None), r.json().get('stat', None))
        else:
            return None

    def sync(self, path, callback):
        '''
        flush channel
        '''
        data_param = {
                'command' : 'sync',
                }
        r = requests.post(self.connectString, data=data_param)
        if r.status_code == 200:
            return r.json().get('stat', None)
        else:
            return
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    zk = Zookeeper('http://127.0.0.1:8000', 10000, None)
    path = zk.create('/apple', 'pie', None)
    logging.info(path)
    zk.create('/apple/yosemite', '10.11', None)
    zk.create('/apple/mavericks', '10.10', None)
    res = zk.get_data('/apple', None)
    logging.info(res)
    res = zk.get_children('/apple', None)
    logging.info(res)
