# GLOBAL CONSTANTS
keylength = 4
universe_size = 16**keylength

import chainedhash
import cuckoohash
import linearhash
import doublehash
import test_cases


def insert(hashmap, cases):
    for i, case in enumerate(cases):
        if not hashmap.insert(case):
            print("Insert unsuccessfull! Stopping at the", i, "/", len(cases), "case.")
            return -1
    return 0


def delete(hashmap, cases):
    for k, v in cases:
        hashmap.delete(k)
    return 0


def delete_success(hashmap, cases):
    for k, v in cases:
        if hashmap.search(k):
            print("DELETE failed. Still present:", k, v)
            return -1
    return 0


def search(hashmap, cases, check):
    # pass in the hashmap, all the cases, and then the actual values are compared with those in the dictionary
    for k, v in cases:
        val_returned = hashmap.search(k)
        if (not val_returned) or (val_returned[0] != k) or (val_returned[1] != check[k]):
            print("Error! Search for:", k, ".Stored in hashmap:", val_returned, "Stored in python dictionary:", check[k])
            return -1
    return 0


def driver(hashmap, distribution, keylength, table_size, max_load_factor):
    """pass in a hash map object, it will give a time for all the various load factors"""
    import time

    results = []
    cases = []

    alpha = 0.1
    increment = 0.1

    samples = 20
    sample_cases = []

    if distribution == 1:
        test_cases.getuniform(keylength, int(max_load_factor * table_size), cases)
        test_cases.getuniform(keylength, samples, sample_cases)  # the actual ones to be tested
    else:
        test_cases.getnormal(keylength, int(max_load_factor * table_size), cases)
        test_cases.getuniform(keylength, samples, sample_cases)  # the actual ones to be tested

    while alpha <= max_load_factor:
        print("Testing for alpha=", alpha)
        intermediate = {"alpha": alpha}

        till_case = min(int(alpha * tablesize), len(cases) - 1)
        hashmap.reset()  # delete all elements in the hashmap first!
        insert(hashmap, cases[:till_case])  # achieve this load factor

        # also insert in the python dictionary
        check = {}
        for k, v in cases[:till_case]:
            check[k] = v

        # measure time for 20 inserts
        worst_case = 0
        amortized_sum = 0
        for i in range(0, samples):
            time_s = time.clock() * 1000000
            insert(hashmap, [sample_cases[i]])
            time_f = time.clock() * 1000000
            worst_case = max(worst_case, time_f-time_s)
            amortized_sum += (time_f-time_s)

            # also insert in the dictionary
            k, v = sample_cases[i]
            check[k] = v

        amortized_case = amortized_sum/samples
        intermediate["ins-wc"] = worst_case
        intermediate["ins-am"] = amortized_case

        # measure time for 20 searches (same elements as you inserted)
        worst_case = 0
        amortized_sum = 0
        for i in range(0, samples):
            time_s = time.clock() * 1000000
            search(hashmap, [sample_cases[i]], check)
            time_f = time.clock() * 1000000
            worst_case = max(worst_case, time_f - time_s)
            amortized_sum += (time_f - time_s)

        amortized_case = amortized_sum / samples
        intermediate["srch-wc"] = worst_case
        intermediate["srch-am"] = amortized_case

        # measure time for 20 deletes
        worst_case = 0
        amortized_sum = 0
        for i in range(0, samples):
            time_s = time.clock() * 1000000
            delete(hashmap, [sample_cases[i]])
            time_f = time.clock() * 1000000
            worst_case = max(worst_case, time_f - time_s)
            amortized_sum += (time_f - time_s)

        amortized_case = amortized_sum / samples
        intermediate["del-wc"] = worst_case
        intermediate["del-am"] = amortized_case

        # check delete success
        delete_success(hashmap, sample_cases)

        results.append(intermediate)
        alpha += increment

    print(results)


if __name__ == "__main__":
    tablesize = 2**10
    hashmap = chainedhash.ChainedHashMap(tablesize)
    #hashmap = linearhash.LinearHashMap(tablesize)
    #hashmap = cuckoohash.CuckooHashMap(tablesize)
    #hashmap = doublehash.DoubleHashMap(tablesize)
    driver(hashmap, 1, keylength, tablesize, 0.9)  # uniform distro. (set second arg to 2 for gaussian)
