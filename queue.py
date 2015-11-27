import collections
import pickledb
import runtime

class Queue:
    def __init__(self, db):
        self.db = db
        self.queue_view = collections.deque()
        self.last_popped = [None]
        upcalls = (self.upcallE, self.upcallD)
        self.runtime = runtime.Runtime(self.db, upcalls)
    def upcallE(self, data):
        self.queue_view.append(data)
    def upcallD(self, data):
        self.last_popped[0] = self.queue_view.popleft()
    def enqueue(self, data):
        self.runtime.append(0, (), data)
    def dequeue(self):
        self.runtime.play_forward(1)
        self.runtime.read_next(0)
        if not self.queue_view:
            return None
        else:
            pass
        last_seen_d = self.runtime.local_horizon[1]
        to_dequeue = self.runtime.local_horizon[0]
        d_loc = self.runtime.append(1, ((0, to_dequeue),), 0)
        self.runtime.read_next(1)
        if d_loc == last_seen_d + 1:
            return self.last_popped[0]

if __name__ == '__main__':
    db = pickledb.load('runtime.db', False)
    queue = Queue(db)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print queue.dequeue()
    print queue.dequeue()
    queue.enqueue(4)
    print queue.dequeue()
    print queue.dequeue()
    print queue.dequeue()
    queue2 = Queue(db)
    queue.enqueue(1)
    print queue2.dequeue()
