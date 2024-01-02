import numpy as np

test = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

###.##.##
##.####.#
##.#..#.#
####..###
....##...
##.#..#.#
...#..#..
##..###.#
##......#
##......#
..#.##.#.
...#..#..
##.####.#
....##...
...####..
....##...
##.####.#


.##.##...##...##.
#####..##..##..##
.....##..##..##..
.##.#.#.####.#.#.
.##...#.#..#.#...
....#..........#.
#..#..#......#..#
....###.....####.
.##...#.#..#.#...
.....#..####..#..
#..#...##..##...#
....#...#..#...#.
#..#.##########.#
#..##...####...##
#####.##.##.##.##
"""
test2 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

.#.##.#.#
.##..##..
.#.##.#..
#......##
#......##
.#.##.#..
.##..##.#

#..#....#
###..##..
.##.#####
.##.#####
###..##..
#..#....#
#..##...#

#.##..##.
..#.##.#.
##..#...#
##...#..#
..#.##.#.
..##..##.
#.#.##.#.
"""

def smudge_dist(str1, str2):
    """
    str * str -> int
    compare two string and returns
    - 1 if they are equal
    - 2 if there are at an hamming dist of1
    - 0 otherwise
    """
    ndiff = sum([c1 != c2 for c1, c2 in zip(str1, str2)])
    if ndiff == 0:
        return 1
    elif ndiff == 1:
        return 2
    else:
        return 0

def classic_dist(str1, str2):
    """
    """
    return int(str1 == str2)

def matrix_dist_rows(l_str, dist_func = classic_dist):
    """
    list[str] -> np.array[bool]
    construct the matrix of all strings pairwise comparisons
    per row
    """
    nrows = len(l_str)
    m_diff = np.full((nrows, nrows), 0)
    for i in range(nrows):
        for j in range(i):
            m_diff[i,j] = dist_func(l_str[i], l_str[j])
            m_diff[j,i] = dist_func(l_str[i], l_str[j])
            # m_diff[i,j] = int(l_str[i] == l_str[j])
            # m_diff[j,i] = int(l_str[i] == l_str[j])
    return m_diff

def matrix_dist_cols(l_str, dist_func = classic_dist):
    """
    list[str] -> np.array[bool]
    construct the matrix of all strings pairwise comparisons
    per col
    """
    l_transpose = ["".join(s) for s in zip(*l_str)]
    return matrix_dist_rows(l_transpose, dist_func)



def test_symetry_vert(l_str):
    """
    list[str] -> bool
    test if all the strings in the list are equal to their reversed
    string
    """
    for s in l_str:
        if s != s[::-1]:
            return False
    return True

def test_symetry_horiz(l_str):
    """
    list[str] -> bool
    """
    return test_symetry_vert(["".join(s) for s in zip(*l_str)])

def checkSymAxis(l_str):
    """
    list[str] -> int
    returns either:
     - the number of column at which the symmetry axis works
     - 100 * the number of rows at which the symmetry works
    """
    nrows = len(l_str)
    ncols = len(l_str[0])
    print("dims are ", nrows, ncols)
    row_starts = range(nrows % 2, nrows-2, 2)
    col_starts = range(ncols % 2, ncols-2, 2)
    # hrow = nrows // 2
    # hcol = ncols // 2
    # lr = hrow * 2
    # lc = hcol * 2
    for cs in col_starts:
        if test_symetry_vert([x[cs:] for x in l_str]):
            hcol = cs + (ncols - cs) // 2
            print("even - Symetry at col", hcol)
            return hcol
    for rs in row_starts:
        if test_symetry_horiz(l_str[rs:]):
            hrow = rs + (nrows - rs) // 2
            print("Even - Symetry at row", hrow)
            return 100*hrow
    print("Error")
    return None

def testPerfectLine(loi):
    """
    list[int] -> bool
    test if all the values in the line are 1
    """
    return all([x == 1 for x in loi])

def testSmudgeLine(loi):
    """
    list[int] -> bool
    test that there are exactly two values to 1 and the
    rest to 2
    """
    n2 = sum([x == 2 for x in loi])
    allNot0 = all([x != 0 for x in loi])
    return n2 == 2 and allNot0

def detectAntidiagonal(M, f_test = testPerfectLine):
    """
    np.array[(int,in)] -> int
    From a square matrix M, detects where there is an antidiagonal 
    of values != 0 spanning the matrix
    It has to touch 2 borders
    returns -1 if there is no result
    """
    n = M.shape[0]
    matches = np.argwhere(M != 0)
    row_matches = matches[np.logical_or(matches[:,0] == 0 , 
                                        matches[:,0] == n-1)]
    col_matches = matches[np.logical_or(matches[:,1] == 0 , 
                                        matches[:,1] == n-1)]
    set_rmatch = set([(x,y) for x,y in row_matches])
    set_cmatch_inv = set([(y,x) for x,y in col_matches])
    set_match_sym= set([tuple(sorted([x,y]))
                        for x,y in set_rmatch & set_cmatch_inv])
    for i,j in set_match_sym:
        lantidiag = [M[i+k, j-k] for k in range(j-i+1)]
        if f_test(lantidiag):
            ##There can be only one full diagonal
            return i + 1 + (j-i) // 2
    return -1

def checkSymAxisMat(l_str, mode = "classic"):
    """
    list[str] -> int
    same as checkSymAxis but using a matrix representation of the 
    distances
    """
    if mode == "classic":
        Mr = matrix_dist_rows(l_str)
        resr = detectAntidiagonal(Mr)
        Mc = matrix_dist_cols(l_str)
        resc = detectAntidiagonal(Mc)
    elif mode == "smudge":
        Mr = matrix_dist_rows(l_str, smudge_dist)
        resr = detectAntidiagonal(Mr, testSmudgeLine)
        Mc = matrix_dist_cols(l_str, smudge_dist)
        resc = detectAntidiagonal(Mc, testSmudgeLine)
    else:
        print("Error param unknown")
        return None
    if resr >= 0:
        return resr * 100

    if resc >= 0:
        return resc
    print("Error")
    return None



l_test = [[y for y in x.split("\n") if len(y)> 0] for x in test.split("\n\n") if len(x)>0]
l_test2 = [[y for y in x.split("\n") if len(y)> 0] for x in test2.split("\n\n") if len(x)>0]

filename = "./input_day13.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

l_text = [[y for y in x.split("\n") if len(y)> 0] 
            for x in textfull.split("\n\n") if len(x)>0]

# vals = [checkSymAxisMat(x, "classic") for x in l_text]
# vals_test =[checkSymAxisMat(x, "classic") for x in l_test]


vals = [checkSymAxisMat(x, "smudge") for x in l_text]
vals_test =[checkSymAxisMat(x, "smudge") for x in l_test]

test_dists = [[matrix_dist_rows(x, smudge_dist), 
               matrix_dist_cols(x, smudge_dist)] 
               for x in l_test]
test_dists2 = [[i+1,matrix_dist_rows(x, smudge_dist), 
                matrix_dist_cols(x, smudge_dist)] 
               for i,x in enumerate(l_test2)]
all_dists = [[i, matrix_dist_rows(x, smudge_dist), 
              matrix_dist_cols(x, smudge_dist)] 
             for i,x in enumerate(l_text)]

