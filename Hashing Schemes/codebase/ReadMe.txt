Four hashing schemes have been implemented - 

1) Chained Hashing in file = "chainedhash.py"
2) Linear Probing in file = "linearhash.py"
3) Cuckoo Hashing in file = "cuckoohash.py"
4) Double Hashing in file = "doublehash.py"


Other than that, the linked-list module for use in hash-chaining is in file = "util.py"
The test_cases.py file creates the key-values pairs, according to a uniform or gaussian random distribution.

main.py is the runnable python file, which contains the test cases. 
Edit the __name__ == "__main__" code inside this file, to specify which hashing technique to use, universe size, key-length, etc.


RUNS ON PYTHON 3. 
Command: python main.py
The output is: key-val pairs of the load-factor vs the various runtime for insert/search/delete (for a specific technique and distribution type).


External libraries used: numpy (only to generate the test-cases!).






