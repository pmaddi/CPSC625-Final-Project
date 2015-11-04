import collections
import pickledb

Queue = collections.deque()
LastPopped = [None]

class Log(collections.deque):
    pass

class Runtime(object):
    def __init__(self, db, upcalls):
        self.db = db
        self.local_horizon = collections.defaultdict(lambda : 0)
        self.upcalls = upcalls
    def global_horizon(self, id):
        h = self.get(str(id) + ':' + 'count')
        if h:
            return h
        else:
            return 0
    def set(self, key, value):
        return db.set(hash(key), value)
    def set_entry(self, id, index, value):
        return self.set(str(id) + ':' + str(index), value)
    def get(self, key):
        return db.get(hash(key))
    def get_entry(self, id, index):
        return self.get(str(id) + ':' + str(index))
    def read(self, id, index):
        # print id, index, self.local_horizon[id]
        if self.local_horizon[id] >= index:
            return None
        # follow dependencies
        val = self.get_entry(id, index)
        # print val
        if val != None:
            for n_id, n_index in val[0]:
                self.read(n_id, n_index)
            self.local_horizon[id] += 1
            # upcall
            print 'make upcall', id, 'with arg', val[1]
            self.upcalls[id](val[1])
        else:
            return None
# API
    def append(self, id, dependencies, data):
    # id is a column id
    # dependencies are [(id, index)]
    # data are of the datatype
    # return an index
        horizon = self.global_horizon(id)
        # print "(dependencies, data)", (dependencies, data)
        self.set_entry(id, horizon + 1, (dependencies, data))
        # Check if false?
        self.set(str(id) + ':' + 'count', horizon + 1)
        db.dump()
        return horizon + 1
    def read_next(self, id):
        seen = self.local_horizon[id]
        return self.read(id, seen + 1)
    def play_forward(self, id):
        while self.local_horizon[id] < self.global_horizon(id):
            self.read_next(id)

# id : (index, dependencies, data)
# id+

if __name__ == '__main__':
    db = pickledb.load('runtime.db', False)
    def upcallE(data):
        Queue.append(data)
    def upcallD(data):
        LastPopped[0] = Queue.popleft()
        # print "LastPopped", LastPopped
    upcalls = (upcallE, upcallD)
    runtime = Runtime(db, upcalls)
    def enqueue(data):
        # print "append to E"
        runtime.append(0, (), data)
    def dequeue():
        runtime.play_forward(1)
        runtime.read_next(0)
        if not Queue:
            # print 'ret none'
            return None
        else:
            pass
            # print list(Queue)
        last_seen_d = runtime.local_horizon[1]
        to_dequeue = runtime.local_horizon[0]
        # print "append to D"
        d_loc = runtime.append(1, ((0, to_dequeue),), 0)
        runtime.read_next(1)
        if d_loc == last_seen_d + 1:
            return LastPopped[0]
    enqueue(1)
    enqueue(2)
    enqueue(3)
    print dequeue()
    print dequeue()
    enqueue(4)
    print dequeue()
    print dequeue()
    print dequeue()
