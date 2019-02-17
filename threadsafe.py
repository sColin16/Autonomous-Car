import threading

class threadsafe_iterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return self.iterator.__next__()

def threadsafe_generator(func):
    def g(*args):
        return threadsafe_iterator(func(*args))

    return g
