import collections
import pickledb
import logging

class Transaction(object):
    def __init__(self):
        pass
    def commit(self, dependencies, data):
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
        return self.db.set(str(hash(key)), value)
        # return self.db.set(hash(key), value)
    def set_entry(self, id, index, value):
        return self.set(str(id) + ':' + str(index), value)
    def get(self, key):
        # return self.db.get(hash(key))
        return self.db.get(str(hash(key)))
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
            logging.info('Make upcall ' + str(id) + ' with arg ' + str(val[1]))
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
        self.db.dump()
        return horizon + 1
    def read_next(self, id):
        seen = self.local_horizon[id]
        return self.read(id, seen + 1)
    def play_forward(self, id):
        while self.local_horizon[id] < self.global_horizon(id):
            self.read_next(id)
    def start_transaction(self, ids):
        '''
        Read forward the id's
          if all transactions are committed
          then add transaction start entries to the ids, containing the min id
        '''
        return Transaction()

# id : (index, dependencies, data)
# id+
