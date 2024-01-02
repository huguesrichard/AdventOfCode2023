import numpy as np

test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def encodeGalaxy(text):
    """
    str -> np.array[(int,int)]
    encodes a 
    """
    l_galaxy = []
    n_planet = 1 
    for row in text.split("\n"):
        if len(row) > 0:
            lr = []
            for c in row:
                if c == ".":
                    lr.append(0)
                elif c == "#":
                    lr.append(-n_planet)
                    n_planet += 1
                else:
                    print ("Error in galaxy parsing")
            l_galaxy.append(lr)
    return np.array(l_galaxy, dtype = int)


def gravitationalLens(Mgal):
    """
    np.array[(int,int)] -> np.array[(int,int)]
    Applies the gravitational lens to the array of galaxies by 
    duplicating the rows that sum to 0 and the columns that sum to 0 as well
    """
    row_empty = np.sum(Mgal, axis = 1) == 0 
    col_empty = np.sum(Mgal, axis = 0) == 0

    Mgal_exprow = np.repeat(Mgal, row_empty + 1, axis = 0)
    Mgal_expcol = np.repeat(Mgal_exprow, col_empty + 1, axis = 1)
    return Mgal_expcol

def gravitationalLensScore(Mgal, score = 999999):
    """
    np.array[(int,int)] -> np.array[(int,int)]
    Applies the gravitational lens by adding a given score on all
    the rows or columns that completely equal to 0
    """
    Mout = np.copy(Mgal)
    row_empty = np.sum(Mgal, axis = 1) == 0 
    col_empty = np.sum(Mgal, axis = 0) == 0
    Mout[row_empty,:] = score
    Mout[:, col_empty] = score
    return Mout


def distManhattan(x,y):
    """
    Manhattan distance
    """
    return np.abs(x[0]-y[0]) + np.abs(x[1]-y[1])

def distManhattanNonEuclid(x,y,M):
    """
    Manhattan distance in a non euclidean space, given a Matrix
    M that has the values of traversing each cell
    We filter out the values that are below 0
    """
    Manhattan = distManhattan(x,y)
    sr, er = sorted([x[0], y[0]])
    sc, ec = sorted([x[1], y[1]])
    scores_row = M[sr+1:er,sc]
    scores_col = M[er, sc+1:ec]
    return(Manhattan + 
           sum(scores_row[scores_row >0]) + 
           sum(scores_col[scores_col>0]))

def computeDistances(Mgal, dist_type = "euclid"):
    """
    np.array * str -> dict[(int,int) : int]
    Compute all the distances between the galaxies in a matrix
    """
    galcoords = np.argwhere(Mgal < 0)
    ngals = len(galcoords)
    d_dist = {}
    for g1 in range(ngals):
        for g2 in range(g1):
            gcoord1 = tuple(galcoords[g1])
            gcoord2 = tuple(galcoords[g2])
            if dist_type == "euclid":
                dist = distManhattan(gcoord1, gcoord2)
            elif dist_type == "noneuclid":
                dist = distManhattanNonEuclid(gcoord1, gcoord2, Mgal)
            else:
                print("Error dist not know:", dist_type)
            d_dist[(Mgal[gcoord1], Mgal[gcoord2])] = dist
    return d_dist


galtest = encodeGalaxy(test)
galtestexp = gravitationalLens(galtest)
testdists = computeDistances(galtestexp)

galtexp2 = gravitationalLensScore(galtest, score = 1)
galtexp10 = gravitationalLensScore(galtest, score = 9)
galtexp100 = gravitationalLensScore(galtest, score = 99)

filename = "./input_day11.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

gal = encodeGalaxy(textfull)
galexp = gravitationalLens(gal)
dists = computeDistances(galexp)

galexp1Mio = gravitationalLensScore(gal)
dists1Mio = computeDistances(galexp1Mio, dist_type = "noneuclid")
