import numpy as np
from collections import OrderedDict
import itertools

test_unknown = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

test_known = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
"""


def row2str(row):
    """
    np.array[(int)] -> str
    transforms a np.array or list of int into an str
    """
    return ",".join([str(x) for x in row])

def isPrefix(row1, row2):
    """
    np.array[int] * np.array[int] -> bool 
    tests if row1 is a prefix list of row2, using conversion to str
    """
    return row2str(row2).startswith(row2str(row1))

def run_lengths(condition):
    """
    np.array[int] -> list[int]
    return the lengths of the runs of 1/True
    """
    return np.diff(np.where(np.concatenate(([condition[0]],
                                          condition[:-1] != condition[1:],
                                            [True])))[0])[::2]

def read_records(records):
    """
    np.array[(int,int)] -> list[Tuple[int]
    reads a record as a matrix of values 0 and 1 and returns the
    list of "1" runs 
    """
    l_runs = []
    for row in records:
        l_runs.append(run_lengths(row))
    return l_runs

def getTextPatterns(text):
    """
    str -> list[np.array[int]], list[list[int]]
    reads the text and transforms it into records
    """
    l_patterns = []
    l_springs = []

    for l in text.split("\n"):
        if len(l) > 0:
            springs, pattern = l.split(" ")
            l_springs.append(np.array([ int(x) for x in springs.translate(str.maketrans(".#?", "012")) ]))
            l_patterns.append(np.array([int(x) for x in pattern.split(",")]) )
    return l_springs, l_patterns

def enumerateStates(record, pattern):
    """
    np.array[int] * list[int] -> list[np.array[int]]
    From a record with values 0, 1, or 2 (2 is unknown) and a pattern
    of the sequence of springs, construct all the possible placements of 
    the remaining springs in the sequence
    """
    nSpringKnown = sum(record == 1)
    nSpringKnown = sum(record == 1)
    index_unknown = np.argwhere(record == 2).flatten()
    nSpringPattern = sum(pattern)
    nSpring2place = nSpringPattern - nSpringKnown
    l_combinations = []
    for index_select in itertools.combinations(index_unknown, nSpring2place):
        crecord = np.copy(record)
        crecord[list(index_select)] = 1
        crecord[crecord == 2] = 0
        l_combinations.append(crecord)
    return l_combinations

def countCompatStates(record, pattern):
    """
    np.array[int] * list[int] -> int
    returns the number of states that are compatible with the pattern
    """
    l_recs = read_records(enumerateStates(record, pattern))
    return sum([np.all(x == pattern) for x in l_recs])


### Version 2: using Dynamic Programming

## We will keep track of a list of records as we move on in the
## text 
## Each element of the list is a 3 items list with lrun, count, closed
## - lrun : list[int] is the list of the current runs
## - count : int is the number of times we already saw the current run
## - closed: bool tells us if we are currently in a run of "#" (False) or 
## if the run is closed (True)

def extend_rec(lrec, pattern):
    """
    """
    lout = []
    for lrun, count, closed in lrec:
        keep_run = True
        #print("Before", lrun, count, closed)
        if closed:
            lrun.append(1)
            closed = False
        else:
            lrun[-1] += 1
            ##TODO: we could add a test of lrun[-1] being <= pattern_last 
            ## if we want to improve the pruning
            for i, v in enumerate(lrun):
                if i >= len(pattern) or v > pattern[i]:
                    keep_run = False
        if keep_run:
            #print("-- Extend:", lrun, count, closed)
            lout.append([lrun[:], count, closed])
    return lout


def close_rec(lrec, pattern):
    lout = []
    for lrun, count, closed in lrec:
        #print("Before", lrun, count, closed)
        if not closed:
            closed = True
            if isPrefix(lrun, pattern) and len(lrun) > 0:
                ##We only add the cases compatible with the pattern
                lout.append([lrun[:], count, closed])
        else:
            lout.append([lrun[:], count, closed])
        #print("-- Close", lrun, count, closed)

    lout = aggregate_rec(lout)
    return lout

def aggregate_rec(lrec):
    """
    aggregates the counts in the list of records
    if the list of runs and the closed states are the same
    """
    d_rec = {}
    for lrun, count, closed in lrec:
        ck = row2str(lrun) + str(closed)
        d_rec.setdefault(ck,[lrun[:], 0, closed])
        d_rec[ck][1] += count
    return list(d_rec.values())

def enumerateCompatStates_dp(str_record, str_pattern):
    """
    str * list[int] -> (list[int], int)
    from a record as a str and a pattern of the run lengths
    returns the records that is compatible with the 
    pattern and the count of this record
    """
    ## We keep the information of the current runs
    ## in a list with 
    ## - the list of runs (list[int])
    ## - the count for this list of runs (int)
    ## - is the current run closed ? (bool)
    list_of_records = [[[], 1, True]]
    pattern = [int(x) for x in str_pattern.split(",")]
    for i,c in enumerate(str_record):
        if c == ".":
            #close the records
            #print("Closing --", i)
            list_of_records = close_rec(list_of_records, pattern)
        elif c == "#":
            #Extend the records
            #print("Extending --", i)
            list_of_records = extend_rec(list_of_records, pattern)
        elif c == "?":
            #duplicate the record for each case "#" or "."
            #print("Duplicating -- ",i)
            list_1 = close_rec(list_of_records, pattern)
            list_2 = extend_rec(list_of_records, pattern)
            list_of_records = list_1 + list_2
        #print(c, list_of_records)
    return sum([x[1] for x in list_of_records if x[0] == pattern])

# def countCompatStates_dp(list_of_records_patterns):
#     """
#     list[list[str]] -> list[int]
#     return the count of compatible states from of list of 2 elements
#     """
#     for str_run, str_pattern in list_of_records_patterns:
#         l_compat_states = enumerateCompatStates_dp(str_run, str_pattern)
#         [for x in l_compat_states ]

l_testu, l_pattu = getTextPatterns(test_unknown)
str_test = [(x.split(" ")) for x in test_unknown.split("\n") if len(x) >0]

global_testpatt = [np.tile(x, 5) for x in l_pattu]

zetest = l_testu[1]
zepatt = l_pattu[1]
zeglobpatt = global_testpatt[1]
ze_combinations = enumerateStates(zetest, zepatt)


test_combinations = [read_records(enumerateStates(l_testu[i], l_pattu[i])) for i in range(6)]

compatCount = [countCompatStates(l_testu[i], l_pattu[i]) for i in range(6)]

filename = "./input_day12.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

l_full, l_patterns = getTextPatterns(textfull)
str_full = [(x.split(" ")) for x in textfull.split("\n") if len(x) >0]

#allcompatCount = [countCompatStates(l_full[i], l_patterns[i]) for i in range(len(l_full))]
allcompatCount_dp = [enumerateCompatStates_dp(s,p) for s,p in str_full]

testcompatCount_q2_dp = [enumerateCompatStates_dp("?".join([s]*5),",".join([p]*5)) for s,p in str_test]

allcompatCount_q2_dp = [enumerateCompatStates_dp("?".join([s]*5),",".join([p]*5)) for s,p in str_full]