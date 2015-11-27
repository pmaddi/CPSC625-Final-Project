import collections
import pickledb
import runtime

class WeakMap:
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
        return self.map_view.get(key, None)
    def set(self, key, value):
        return self.runtime.append(0, (), (key, value))

if __name__ == '__main__':
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

