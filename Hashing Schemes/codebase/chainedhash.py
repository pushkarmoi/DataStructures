import utils as util
from main import universe_size as univ_size


class ChainedHashMap(object):
    def __init__(self, size):
        self.size = int(size)
        self.store = [util.LinkedList()] * self.size
        self.seed = 19

    def getindex(self, key):
        key = int(key, 16)
        hashed = ((self.seed * key) % univ_size) / (univ_size / self.size)
        return int(hashed) % self.size

    def reset(self):
        self.store = [util.LinkedList()] * self.size

    def search(self, key):  # false, or a (k, v) tuple
        bucket = self.store[self.getindex(key)]
        return bucket.search(key)

    def insert(self, k_v_tuple):  # put / update
        bucket = self.store[self.getindex(k_v_tuple[0])]
        if not bucket.search(k_v_tuple[0]):  # doesn't exist in the hash table
            bucket.insert(k_v_tuple)
        else:  # just update
            bucket.update(k_v_tuple)
        return True

    def delete(self, key):
        bucket = self.store[self.getindex(key)]
        bucket.delete(key)
