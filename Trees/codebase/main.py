import random
import time

## USER defined packages
import bst
import avl
import treap
import skiplist

def generatecases(num, cases, order, seed=0):  # pass in a set
    len_new = len(cases) + num  # as we add new cases to existing
    if order == 1:  # randomized
        while len(cases) != len_new:
            cases.add(random.randint(100, 100 + (100*num)))
    elif order == 2:  # increasing order
        i = 0
        while len(cases) != len_new:
            cases.add(seed + i)
            i += 1


def insertall(struct, cases):
    for i, num in enumerate(cases):
        if not struct.insert(num):
            print("Insert unsuccessfull! for num=", num)
    return 0


def deleteall(struct, cases):
    for num in cases:
        struct.delete(num)
    return 0


def checkdelete(struct, cases):
    for num in cases:
        if struct.search(num):
            print("Deleted element still present:", num)
    return 0


def searchall(struct, cases):
    for num in cases:
        if not struct.search(num):
            print("Couldnt retrieve value=", num)
            struct.printlists()
            return
    return 0


def inlatex(xcords, ycords):
    tups = []
    if len(xcords) != len(ycords):
        print("AXIS MIS-MATCH")
        print(xcords)
        print(ycords)
        return
    for i in range(len(xcords)):
        temp = "(" + str(xcords[i]) + "," + str(float(round(ycords[i], 3))) + ")"
        tups.append(temp)
    return "".join(tups)


def driver(struct, maxelts, order):  # order=1, for randomized keys, order=2 for increasing keys

    # run all function apis on this struct and save the graph as a matplotlib file
    cases = set([])
    num_elts = 0
    increment = maxelts//10
    samplesize = 20

    # all the different performance times
    x_axis = []  # the number of elements in the structure (n)
    wc_search = []
    am_search = []
    wc_insert = []
    am_insert = []
    wc_delete = []
    am_delete = []

    while num_elts < maxelts:
        num_elts += increment
        x_axis.append(num_elts)
        generatecases(increment, cases, order, seed=num_elts+1)  # add new cases to existing set.
        #print("cases->", cases, "\n\n\n\n")        
        insertall(struct, list(cases))

        samples = set([])
        if order==1:
            while len(samples) < samplesize:
                randomnum = random.randint(1500, 15000)
                if randomnum not in cases:
                    samples.add(randomnum)
            #print("samples->", samples)
        else:
            generatecases(samplesize, samples, order=2, seed=len(cases)+1)
            #print("samples->", samples)    

        # measure insert time
        wc = 0
        am = 0
        for sample in samples:
            time_s = time.clock() * 1000000
            insertall(struct, [sample])
            time_f = time.clock() * 1000000
            wc = max(wc, time_f-time_s)
            am += (time_f - time_s)
        am = am/samplesize
        wc_insert.append(wc)
        am_insert.append(am)

        # measure search time
        wc = 0
        am = 0
        for sample in samples:
            time_s = time.clock() * 1000000
            searchall(struct, [sample])
            time_f = time.clock() * 1000000
            wc = max(wc, time_f-time_s)
            am += (time_f - time_s)
        am = am/samplesize
        wc_search.append(wc)
        am_search.append(am)


        # measure delete time
        wc = 0
        am = 0
        for sample in samples:
            time_s = time.clock() * 1000000
            deleteall(struct, [sample])
            time_f = time.clock() * 1000000
            wc = max(wc, time_f-time_s)
            am += (time_f - time_s)
        am = am/samplesize
        wc_delete.append(wc)
        am_delete.append(am)

        # check delete success
        checkdelete(struct, list(samples))

    # print latex output
    print("Worstcase Search: ", inlatex(x_axis, wc_search), "\n")
    print("Amortized Search: ", inlatex(x_axis, am_search), "\n")
    print("Worstcase Insert: ", inlatex(x_axis, wc_insert), "\n")
    print("Amortized Insert: ", inlatex(x_axis, am_insert), "\n")
    print("Worstcase Delete: ", inlatex(x_axis, wc_delete), "\n")
    print("Amortized Delete: ", inlatex(x_axis, am_delete), "\n")


if __name__ == "__main__":
    maxelts = 1000 
    struct = bst.BST()
    #struct = avl.AVL()
    #struct = treap.Treap()
    #struct = skiplist.SkipList()
    driver(struct, maxelts, order=1)  # randomized keys, set 2 for increasing order keys













