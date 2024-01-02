from collections import OrderedDict
from collections import namedtuple
from collections import Counter
import numpy as np

test1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

test2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

"""

enclose1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

enclose2 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

enclose3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

def move2vec(pos, move):
    """
    (int, int) * str -> (int,int)
    returns the vector of position change according to the
    move
    return None if not compatible
    """
    d_move = {"r": (0,1), "l": (0,-1), 
              "u": (-1,0), "d":(1,0)}
    cm = d_move.get(move, None)
    if cm is None:
        print("--strange move:", move)
    return (pos[0] + cm[0], pos[1] + cm[1])

def readMatrix(text):
    """
    reads the matrix for a single str and returns a list of list of chars 
    with the position where "S" is
    """
    mat = [[y for y in list(x)] for x in text.split("\n") if len(x) > 0]
    for i,row in enumerate(mat):
        for j, xy in enumerate(row):
            if xy == "S":
                sourcepos = (i,j)
                break
    return (sourcepos, np.array(mat))

def nextMove(move, letter):
    """
    str * str -> (int, int)
    returns the next move for the given move and pipe
    if it is not compatible return None
    """
    d_move_letter = {("r", "-"): "r", ("r", "7"): "d", ("r", "J"): "u",
                     ("l", "-"): "l", ("l", "F"): "d", ("l", "L"): "u",
                     ("u", "|"): "u", ("u", "F"): "r", ("u", "7"): "l",
                     ("d", "|"): "d", ("d", "L"): "r", ("d", "J"): "l"
                     }
    return d_move_letter.get((move, letter), None)


def findCompatMoves(spos, Mat):
    """
    (int,int) * np.array[str,str] -> (str, str)
    from a position and a matrix of chars, finds the compatible moves
    """
    l_compat = []
    for move in ["u", "d", "l", "r"]:
        sposnext = move2vec(spos, move)
        nm = nextMove(move, Mat[sposnext])
        #print("FindCompat:", spos, move, sposnext, nm)
        if nm is not None:
            l_compat.append(move)
    return l_compat



def createPath(sourcepos, Mat, getListOfPos = False):
    """
    (int, int) * np.array[str,str] -> np.array[int,int]
    from a source position and a matrix of letters, returns the
    numpy array with all the position counted for the path
    """
    Mpath = np.full(Mat.shape, -1)
    l_pos1, l_pos2 = [], []
    nsteps = 0 
    #First find t
    print("****** Starting searching for a path ***** ")
    m1, m2 = findCompatMoves(sourcepos, Mat)
    p1, p2  = sourcepos, sourcepos
    while p1 != p2 or nsteps == 0 :
        Mpath[p1] = nsteps
        Mpath[p2] = nsteps
        l_pos1.append(p1)
        l_pos2.append(p2)
        #print("Step:", nsteps, ", Pos:", p1, p2, "move", m1, m2)
        #print(Mpath)
        p1n = move2vec(p1, m1)
        p2n = move2vec(p2, m2)
        m1 = nextMove(m1, Mat[p1n])
        m2 = nextMove(m2, Mat[p2n])
        #print("---", p1, p2, p1n, p2n, m1, m2)
        p1 = p1n
        p2 = p2n
        nsteps += 1
    Mpath[p1] = nsteps
    l_pos1.append(p1)
    print("At the end of the loop, nsteps: ", nsteps)
    print(Mpath)
    l_pos = l_pos1 + list(reversed(l_pos2))
    return Mpath, np.array(l_pos)

s1, M1 = readMatrix(test1)
s2, M2 = readMatrix(test2)

se1, Me1 = readMatrix(enclose1)
se2, Me2 = readMatrix(enclose2)
se3, Me3 = readMatrix(enclose3)

p1, lp1 = createPath(s1, M1)
p2, lp2 = createPath(s2, M2)

pe1, lpe1 = createPath(se1, Me1)
pe2, lpe2 = createPath(se2, Me2)
pe3, lpe3 = createPath(se3, Me3)

filename = "./input_day10.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

sfull, Mfull = readMatrix(textfull)
pfull, lpfull = createPath(sfull, Mfull)

### Now we need to fill the regions that are within the area
### first find possible seeds with the analysis of consecutive differences
### then fill them in??

def contour(M):
    """
    np.array -> np.array
    """
    return (M >= 0) * 1

def scalar(u,v):
    """
    (int,int) * (int,int) -> int
    returns the scalar product of u and v
    """
    return u[0]*v[0] + u[1]*v[1]

def findPointsInside(Mvals, lpath):
    """
    np.array[(int,int)] * np.array[(int,int)] -> np.array[(bool, bool)]
    from the array with the path constructed and the array of all 
    positions in the path,
    returns a matrix of binary values 
    of the points of M which are inside the contour
    """
    M = (Mvals >= 0) * 1
    ## Vectors for the 
    v_horiz = np.array([(1,0), (1,1), (-1,1)]).T
    v_vert = np.array([(0,1), (1,1) , (1,-1)]).T
    ##TODO we need to add the last place for the 
    pathgrad = np.row_stack((lpath[1] - lpath[-2], 
                             lpath[2:] - lpath[:-2]))
    ## We take the differences over 2 positions
    left_right = np.any(pathgrad @ v_horiz <= 0 , axis = 1)
    right_left = np.any(pathgrad @ v_horiz >= 0 , axis = 1)
    up_down = np.any(pathgrad @ v_vert <= 0 , axis = 1)
    down_up = np.any(pathgrad @ v_vert >= 0 , axis = 1)
    lrgrad = lpath[ np.where(left_right) ]
    rlgrad = lpath[ np.where(right_left) ]
    udgrad = lpath[ np.where(up_down) ]
    dugrad = lpath[ np.where(down_up) ]
    Mvert = np.zeros(M.shape, dtype = int)
    for i,j in lrgrad: Mvert[i,j] = 1
    Mcrowlr = np.cumsum(Mvert, axis = 1)
    Mvert = np.zeros(M.shape, dtype = int)
    for i,j in rlgrad: Mvert[i,j] = 1
    Mcrowrl = np.flip(np.flip(Mvert,axis = 1).cumsum(axis = 1),axis=1)
    # The points inside cross the boundary an odd number of times
    inside_byrow = np.logical_and(Mcrowlr % 2 == 1, Mcrowrl % 2 == 1, M == 0) 
    Mhoriz = np.zeros(M.shape, dtype = int)
    for i,j in udgrad: Mhoriz[i,j] = 1
    Mccolud = np.cumsum(Mhoriz, axis = 0)
    Mhoriz = np.zeros(M.shape, dtype = int)
    for i,j in dugrad: Mhoriz[i,j] = 1
    Mccoldu = np.flip(np.flip(Mhoriz, axis = 0).cumsum(axis =0), axis =0)
    inside_bycol = np.logical_and(Mccolud % 2 == 1, Mccoldu % 2 == 1, M == 0)
    points_inside = np.logical_and(inside_byrow, inside_bycol)
    return points_inside

inside1 = findPointsInside(p1, lp1)

inside2 = findPointsInside(p2, lp2)

ie1 = findPointsInside(pe1, lpe1)
ie2 = findPointsInside(pe2, lpe2)
ie3 = findPointsInside(pe3, lpe3)

iefull = findPointsInside(pfull, lpfull)