import collections
import pickledb
import runtime
import logging

import directory

# maintain a directory trie and a hash of paths to data
# just one log for now

class WeakMap:
    def __init__(self, db):
        self.db = db
        self.map_view = {}
        self.last_popped = [None]
        self.fs = directory.Directory()
        upcalls = (self.upcall,)
        self.runtime = runtime.Runtime(self.db, upcalls)
        self.runtime.play_forward(0)

    def upcall(self, data):
        self.map_view[data[0]] = data[1]
        # add to directory
        self.fs.mknode(data[0])

    def get(self, key):
        self.runtime.play_forward(0)
        return self.map_view.get(key, None)

    def set(self, key, value):
        # get lock on log 0
        self.runtime.play_forward(0)
        # verify can add in directory
        if self.fs.can_mknode(key):
            return self.runtime.append(0, (), (key, value))
        else:
            logging.info("Cannot make node")
            return False

    def get_children(self, key):
        self.runtime.play_forward(0)
        return self.fs.ls(key)
            # search in directory
        # return [i for i in self.map_view.keys() if i.startswith(key)]

def testfn1():
    db = pickledb.load('runtime.db', False)
    map1 = WeakMap(db)
    map1.set(1, 'a')
    map1.set(2, 'b')
    map1.set(3, 'c')
    map2 = WeakMap(db)
    map2.set(1, 'aa')
    print map2.get(2)
    print map2.get(1)
    print map2.get(75) # fails

def testfn2():
    db = pickledb.load('runtime.db', False)
    map1 = WeakMap(db)
    print map1.set('/tmp', '1')
    print map1.set('/tmp/a', '2')
    print map1.set('/tmp/b', '3')
    print map1.set('/tmp/a/c', '4')
    print map1.set('/tmp/a/c', '4')
    print map1.set('/', '4')
    print map1.get_children('/tmp')
    print map1.get('/tmp/b')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    testfn2()

