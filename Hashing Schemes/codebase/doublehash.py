from main import universe_size as univ_size


class DoubleHashMap(object):
    def __init__(self, size):
        self.size = size//1
        self.store = [None] * self.size
        self.limit = 20  # max chain size.
        self.seed1 = 3
        self.seed2 = 5

    def reset(self):
        self.store = [None] * self.size
        self.seed1 = 3
        self.seed2 = 5

    def getindex(self, key, i):
        key = int(key, 16)
        hashed1 = ((self.seed1 * key) % univ_size) / (univ_size / self.size)
        hashed2 = (((self.seed2 * key) % univ_size) / (univ_size / self.size)) + 1  # so that it is never 0.
        return int(hashed1 + (i*hashed2)) % self.size

    def search(self, key):  # false, or a (k, v) tuple
        # search till max chain limit
        for i in range(0, self.limit):
            index = self.getindex(key, i)
            if (self.store[index] is not None) and(self.store[index][0] == key):
                return self.store[index]

        return False  # not found!

    def insert(self, k_v_tuple, rehash=True):  # insert or update  (true on insert success)
        # just rehash when the chain size increases
        for i in range(0, self.limit):
            index = self.getindex(k_v_tuple[0], i)
            if (self.store[index] is None) or (self.store[index][0] == k_v_tuple[0]):
                self.store[index] = k_v_tuple
                return True

        # wooah! max chain limit reached
        if rehash:
            return self.rehash(k_v_tuple)
        else:
            return False

    def rehash(self, k_v_tuple):
        values_to_insert = self.store
        values_to_insert.append(k_v_tuple)

        while True:
            success = True
            self.seed1 += 4
            self.seed2 = self.seed1 + 2
            self.store = [None] * self.size

            for k_v in values_to_insert:
                if k_v is not None:
                    if not self.insert(k_v, rehash=False):
                        success = False
                        self.seed1 += 50
                        break
            if success:
                return True

    def delete(self, key):  # true on success, false otherwise
        # search till max chain limit
        for i in range(0, self.limit):
            index = self.getindex(key, i)
            if (self.store[index] is not None) and(self.store[index][0] == key):
                self.store[index] = None
                return True
        return False
