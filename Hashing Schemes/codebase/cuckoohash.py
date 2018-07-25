from main import universe_size as univ_size


class CuckooStore(object):
    def __init__(self, size, seed):  # pass in a size and a hash-function
        size = int(size)
        self.store = [None] * size  # simply store a (k, v) or None
        self.size = size
        self.seed = seed  # odd number

    def getindex(self, key):
        # key is a 4 digit hex, as a string
        key = int(key, 16)
        hashed = ((self.seed * key) % univ_size) / (univ_size / self.size)
        return int(hashed) % self.size  # no need to take this mod though

    def search(self, key):
        index = self.getindex(key)
        bucket = self.store[index]
        if (bucket is not None) and (bucket[0] == key):
            return bucket[0], bucket[1]
        else:
            return False

    def delete(self, key):
        index = self.getindex(key)
        bucket = self.store[index]
        if (bucket is not None) and (bucket[0] == key):
            self.store[index] = None
            return True  # delete was successfull
        else:
            return False  # delete not successfull

    def insert(self, k_v_tuple):  # put and displace the current item
        index = self.getindex(k_v_tuple[0])
        bucket = self.store[index]

        self.store[index] = k_v_tuple  # store the current inserted value
        if (bucket is None) or (bucket[0] == k_v_tuple[0]):
            return None  # insert successfull.
        else:
            return bucket  # return the displaced tuple


class CuckooHashMap(object):
    def __init__(self, size):
        # generate new seeds (increasing odd numbers)
        size = int(size)
        self.size = size
        self.seed1 = 1
        self.seed2 = 3
        self.store1 = CuckooStore(self.size/2, self.seed1)
        self.store2 = CuckooStore(self.size/2, self.seed2)

    def reset(self):
        self.seed1 = 1
        self.seed2 = 3
        self.store1 = CuckooStore(self.size/2, self.seed1)
        self.store2 = CuckooStore(self.size/2, self.seed2)

    def search(self, key):  # false, or a (k, v) tuple
        k_v_tuple = self.store1.search(key)
        if isinstance(k_v_tuple, tuple):
            return k_v_tuple
        k_v_tuple = self.store2.search(key)
        return k_v_tuple  # returns a tuple or False

    def delete(self, key):
        if not self.store1.delete(key):
            return self.store2.delete(key)
        else:
            return True

    def insert(self, k_v_tuple, rehash=True):
        to_insert = k_v_tuple
        counter = 0
        store = self.store1

        while True:
            if (counter == 1) and (to_insert == k_v_tuple) and (store is self.store1):
                break

            to_insert = store.insert(to_insert)  # ignore this warning!
            if to_insert is None:  # something was set
                return True  # success

            counter = 1
            if store is self.store1: store = self.store2  # toggle the stores
            else: store = self.store1

        if rehash:
            return self.rehash(to_insert)  # rehased! Hence, the insert was successfull
        else:
            return False  # didn't rehash, and insert was not successfull

    def rehash(self, k_v_tuple):
        from random import randint

        values_to_insert = []
        # add values in the prev stores
        for k_v in self.store1.store:
            if k_v:
                values_to_insert.append(k_v)
        for k_v in self.store2.store:
            if k_v:
                values_to_insert.append(k_v)
        if k_v_tuple:
            values_to_insert.append(k_v_tuple)

        while True:
            success = True
            # print("r.", end=" ")
            self.seed1 += 4
            self.seed2 = self.seed1 + 2

            """
            self.seed1 = randint(self.seed1+1, self.seed1+10)
            if self.seed1%2 == 0:
                self.seed1 += 1
            while True:
                self.seed2 = randint(self.seed2+1, self.seed2+10)
                if self.seed2%2 == 0:
                    self.seed2 += 1
                if self.seed1 != self.seed2: break
            """

            self.store1 = CuckooStore(self.size/2, self.seed1)
            self.store2 = CuckooStore(self.size/2, self.seed2)

            # rehash everything values_to_insert
            for k, v in values_to_insert:
                if not self.insert((k, v), rehash=False):  # insert not successful
                    success = False
                    break

            if success:
                # print()
                return True



