import collections
import pickledb

Queue = collections.deque()
LastPopped = None

class Log(collections.deque):
    pass

class Runtime(object):
    def __init__(self, db, upcalls):
        self.db = db
        self.local_horizon = collections.defaultdict(lambda : 0)
        self.upcalls = upcalls

    def global_horizon(self, id):
        h = db.get(hash(str(id) + ':' + 'count'))
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
        if self.local_horizon[id] <= index:
            return None
        # follow dependencies
        val = get_entry(id, index)
        if val != None:
            for n_id, n_index in val[0]:
                read(n_id, n_index)
            self.local_horizon[id] += 1
            # upcall
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
        self.set_entry(id, horizon + 1, (dependencies, data))
        # Check if false?
        db.set(hash(str(id) + ':' + 'count'), horizon + 1)
        db.dump()
        return horizon + 1
    def read_next(self, id):
        # where to store upcalls
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
        LastPopped = Queue.popleft(data)
        print "LastPopped", LastPopped
    upcalls = (upcallE, upcallD)
    runtime = Runtime(db, upcalls)
    def enqueue(data):
        runtime.append(0, (), data)
    def dequeue():
        runtime.play_forward(1)
        runtime.read_next(0)
        if not Queue:
            return None
        last_seen_d = runtime.local_horizon[1]
        to_dequeue = runtime.local_horizon[0]
        d_loc = runtime.append(1, ((0, to_dequeue)), 0)
        if d_loc == last_seen_d + 1:
            return LastPopped
    enqueue(1)
    print Queue
    enqueue(2)
    print Queue
    enqueue(3)
    print Queue
    dequeue()
    print Queue
    dequeue()
    print Queue
    dequeue()
    print Queue




