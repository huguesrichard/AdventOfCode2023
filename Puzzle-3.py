import numpy as np
import pandas as pd

test = ["467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598.."]

def getSymbolsPos(text):
    """
    str -> list[int]
    returns a list of values from the string
    - default is -2 for "."
    - the digit values from 0 to 9 otherwise
    - -1 if it is a symbol
    
    """
    res = [-2] * len(text)
    for i,c in enumerate(list(text)):
        if c in "0123456789":
            res[i] = int(c)
        elif c != ".":
            res[i] = -1
    return res

def getGearRatio(text):
    """
    str -> list[int]
    same as getSymbolsPos, instead only * characters are
    considered as a symbol this time
    """
    res = [-2] * len(text)
    for i,c in enumerate(list(text)):
        if c in "0123456789":
            res[i] = int(c)
        elif c == "*":
            res[i] = -1
    return res


def getSymbolsMat(l_text):
    """
    list(str) -> np.array
    """
    return np.array([getSymbolsPos(l) for l in l_text])

def getGearRatioMat(l_text):
    """
    list(str) -> np.array
    """
    return np.array([getGearRatio(l) for l in l_text])


def markParts(mvals):
    """
    np.array -> list[(int,int)]
    from the matrix with values coded for symbols -1 and the digits
    detects the positions in the matrix that can be kept
    """
    imask = np.argwhere(mvals == -1)
    mask_mat = np.full(mvals.shape, False)
    for (ii,jj) in imask:
        for i in (ii-1, ii, ii+1):
            for j in (jj-1, jj, jj+1):
                if i>=0 and j>=0 and i < mask_mat.shape[0] and j < mask_mat.shape[1]:
                    mask_mat[i,j] = True
    posparts = np.argwhere(np.logical_and(mvals >= 0, mask_mat))
    tuple_posparts = [tuple(x) for x in posparts]
    return(tuple_posparts)

def findGear2PartsPos(gvals):
    """
    np.array -> dict[(int, int) : list[(int,int)]]
    from the matrix with gear ratio identified and digits coded
    returns a dictionary of gear ratio to list of part positions
    (this list hasn't been cleaned on redundant parts positions)
    """
    imask = np.argwhere(gvals == -1)
    d_gear2parts = {}
    for ii,jj in imask:
        cgear = (ii,jj)
        l_ovparts = []
        for i in (ii-1, ii, ii+1):
            for j in (jj-1, jj, jj+1):
                if (i>=0 and j>=0 
                    and i < gvals.shape[0] 
                    and j < gvals.shape[1]
                    and gvals[i,j] >= 0):
                    l_ovparts.append((i,j))
        if len(l_ovparts) > 0:
            d_gear2parts[cgear] = l_ovparts
    ##Here we could add the parts deduplication
    return d_gear2parts

def findParts(mvals):
    """
    np.array -> list[Tuple(int, int, list[Tuple[int,int]])]
    from the array of values, return a list of 
    all the parts, as a 3 values Tuple with:
     - the ID of the part
     - the part number
     - the list of positions for the part
    """
    mvals_bin = np.array(mvals >= 0, dtype = int)
    diffscore = np.diff(mvals_bin, axis = 1)
    diffscore = np.column_stack((mvals_bin[:,0],
                                diffscore,
                                -mvals_bin[:,-1]))
    starts = np.argwhere(diffscore == 1)
    ends = np.argwhere(diffscore == -1) #ends are exclusive !!!
    pid = 0
    lparts = []
    for (s, e) in zip(starts, ends):
        partid = "Part.{:06d}".format(pid)
        lpos = [(s[0], x) for x in range(s[1], e[1]) ]
        strpartnum = "".join([str(mvals[p]) for p in lpos])
        if len(strpartnum) == 0:
            print("Problem here:", partid, lpos)
        partnum = int(strpartnum)
        lparts.append((partid, partnum, lpos))
        pid += 1
    return lparts

def getPartSchematics(l_text):
    """
    str -> list[int]
    from the list of str return the list of parts ID with
    values that are in the schematics
    """
    mvals = getSymbolsMat(l_text)
    marked_parts = markParts(mvals)
    id_parts = findParts(mvals)
    #print(id_parts)
    #two dictionnaries: parts coord to part ID
    d_pcoords = dict([(pos, pid) for (pid, pnum, lpos) in id_parts for pos in lpos])
    #parts ID to parts number
    d_pnumber = dict([(pid, pnum) for (pid, pnum, lpos) in id_parts])
    ids = set(d_pcoords[x] for x in marked_parts)
    nums = [d_pnumber[id] for id in ids]
    return(ids, nums, sum(nums))


def getGearsRatios(l_text):
    """
    str -> dict[(int,int): (str, str, int)]
    from the list of str, returns the list of gears ratio with
    the values corresponding around those
    only the gears with 2 values are kept
    """
    gvals = getGearRatioMat(l_text)
    d_gear2parts = findGear2PartsPos(gvals)
    id_parts = findParts(gvals)
    #two dictionnaries: parts coord to part ID
    d_pcoords = dict([(pos, pid) for (pid, pnum, lpos) in id_parts for pos in lpos])
    #parts ID to parts number
    d_pnumber = dict([(pid, pnum) for (pid, pnum, lpos) in id_parts])
    ##now we redo a dic of unique parts
    d_gear2parts_unique = dict()
    for (cgear,listparts) in d_gear2parts.items():
        id_parts = set([d_pcoords[x] for x in listparts])
        if len(id_parts)> 1:
            numvals = [d_pnumber[id] for id in id_parts]
            d_gear2parts_unique[cgear] = ("/".join(id_parts) ,numvals, np.prod(numvals))
    return d_gear2parts_unique


filename = "./input_day3.txt"
with open(filename, "r") as file:
    l_text = [line.rstrip() for line in file]
#l_text = fin.readlines()


mvals = getSymbolsMat(l_text)
pos_marks = markParts(mvals)
parts_id = findParts(mvals)
#pd.DataFrame(mvals).to_csv("./input_day3_conv.csv")

## Test 1 : 456384 --> not high enough, what is missing? 
## First bug: 0 is both the code for symbols and for the digits
## so numbers finishing with 0 were missed
## New total is: 540103
## Now after a last small typo : 554003

## part 2 
a = getGearsRatios(l_text)
res = np.sum([x[2] for x in a.values()])