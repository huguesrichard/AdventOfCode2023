from collections import OrderedDict
from collections import namedtuple
from collections import Counter
import numpy as np

test = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def diffPyramideLast(v):
    """
    np.array[int] -> int
    """
    cvec = v.copy()
    valcum = cvec[-1]

    for i in range(len(v)-1):
        #print(cvec)
        nvec = np.diff(cvec)
        valcum -= nvec[-1]
        cvec = nvec.copy()
        if np.all(nvec ==0):
            break
    return valcum

def diffPyramideFirst(v):
    """
    np.array[int] -> int
    """
    cvec = v.copy()
    l_vals = [cvec[0]]
    for i in range(len(v)-1):
        #print(cvec)
        nvec = np.diff(cvec)
        l_vals.append(nvec[0])
        cvec = nvec.copy()
        if np.all(nvec ==0):
            break
    l_first_vals = [0] * len(l_vals)
    for i in reversed(range(len(l_vals)-1)):
        l_first_vals[i] = l_vals[i] - l_first_vals[i+1] 
    return l_first_vals[0]



l_test = test.split("\n")

l_tvecs = [np.array([int(y) for y in x.split(" ")]) for x in l_test if len(x)>0]
test_first = [diffPyramideFirst(x) for x in l_tvecs]

filename = "./input_day9.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

all_text = [x for x in textfull.split("\n") if len(x) >0]

l_vecs = [np.array([int(y) for y in x.split(" ")]) for x in all_text if len(x)>0]

all_proj_last = [diffPyramideLast(x) for x in l_vecs]

all_proj_first = [diffPyramideFirst(x) for x in l_vecs]