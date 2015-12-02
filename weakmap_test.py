from weakmap import *
import pickledb

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

