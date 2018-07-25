from main import universe_size as univ_size


class LinearHashMap(object):
    def __init__(self, size):
        self.size = int(size)
        self.store = [None] * self.size
        self.seed = 197  # random odd number

    def reset(self):
        #print("hashmap reset!")
        self.store = [None] * self.size

    def getindex(self, key):
        #hashed = util.HashFunctions.simplehashfunction(key)  # underlying hash function
        #return int(hashed % self.size)
        key = int(key, 16)
        hashed = ((self.seed * key) % univ_size) / (univ_size / self.size)
        return int(hashed) % self.size

    def search(self, key):  # false, or a (k, v) tuple
        index = self.getindex(key)
        increment = 0
        while increment < self.size:
            index_to_use = (index + increment) % self.size  # wrapping around
            if self.store[index_to_use] is None:
                return False
            elif self.store[index_to_use][0] == key:
                return self.store[index_to_use]
            else:
                increment += 1
        return False

    def insert(self, k_v_tuple):  # insert or update  (true on insert success, false on no more capacity)
        index = self.getindex(k_v_tuple[0])
        increment = 0
        while increment < self.size:
            index_to_use = (index + increment) % self.size  # wrapping around
            if self.store[index_to_use] is None:
                self.store[index_to_use] = k_v_tuple
                return True
            elif self.store[index_to_use][0] == k_v_tuple[0]:
                self.store[index_to_use] = k_v_tuple
                return True
            else:
                increment += 1
        return False  # NO more capacity

    def delete(self, key):  # eager-delete
        index = self.getindex(key)
        increment = 0

        i = None

        while increment < self.size:
            index_to_use = (index + increment) % self.size
            if self.store[index_to_use] is None:
                return False
            elif self.store[index_to_use][0] == key:
                self.store[index_to_use] = None
                i = index_to_use
            else:
                increment += 1

        if i is None:
            return False

        j = (i + 1) % self.size
        increment = 0

        while increment < self.size:
            if self.store[j] is None:
                return True

            # not empty, so check if its key lies b/w [i+1, j], if not replace it with i
            index_should_be = self.getindex(self.store[j][0])
            lies_bw = False
            if i < j:
                if (index_should_be >= i+1) and (index_should_be <= j):
                    lies_bw = True
            elif j < i:
                if (index_should_be <= j) or (index_should_be >= i+1):
                    lies_bw = True

            if not lies_bw:
                self.store[i] = self.store[j]
                self.store[j] = None
                i = j
                j = (i+1) % self.size
            else:
                j = (j+1) % self.size

            increment += 1

        return True

