import random
import numpy


def getuniform(keylength, num, store):  # keylength, number-of-kv-pairs, list-to-store

    dups_store = {}
    cases = 0

    while cases < num:
        max_num = (16**keylength) - 1
        key = random.randint(0, max_num)
        key = "0000" + hex(key)[2:]
        key = key[-keylength:]

        if key in dups_store:
            continue

        value = random.randint(0, 100)
        dups_store[key] = value

        cases += 1
        store.append((key, value))


def getnormal(keylength, num, store):
    from math import sqrt
    maxnum = (16**keylength) - 1

    mean = maxnum/2
    n = mean/2
    sd = sqrt( (n*(n+1)*((2*n) + 1)) / (3 * (maxnum+1)) )
    sd -= (sd/6)

    print("mean is",mean,"sd is",sd)

    nums = numpy.random.normal(mean, sd, num)
    nums = list(map(int, nums))

    for case in nums:
        key = "0000" + hex(case)[2:]
        key = key[-keylength:]
        value = random.randint(0, 100)
        store.append((key, value))

