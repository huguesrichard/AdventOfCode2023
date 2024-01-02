import numpy as np
from numpy import ndarray
from collections import OrderedDict

test = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

d_move = {'l\\': 'u', 'l/': 'd', 'r\\': 'd', 'r/': 'u',
          'u\\': 'l', 'u/': 'r', 'd\\': 'r', 'd/': 'l',
          'u|' : 'u', 'd|' : 'd', 'l-': 'l', 'r-': 'r',
          'u-': 'lr', 'd-': 'lr', 'l|': 'ud', 'r|': 'ud'}

for m in "udrl": d_move[m + "."] = m


def move_beam(pos: (int, int), dir: str, shape: (int, int)) -> (int, int):
    """
    moves a beam at pos according to dir: "l", "r", "u", "d" and tests if 
    if goes outside of the square
    """
    new_x, new_y = pos
    if dir == "u":
        new_x -= 1
    elif dir == "d":
        new_x += 1
    elif dir == "l":
        new_y -= 1 
    elif dir == "r":
        new_y += 1
    else:
        print("Error move beam:", dir)
    if new_x <0 or new_x >= shape[0] or new_y < 0 or new_y >= shape[1]:
        return (-1,-1)
    else:
        return (new_x, new_y)


def beam_cell(contraption: ndarray[str,str], 
              pos: (int,int), dir: str) -> list[((int,int), str)]:
    """
    Read a position and an incoming direction and returns a 
    list of positions and outgoing directions
    """
    cur_mirror = contraption[pos]
    cur_shape = contraption.shape
    # apply the mirror at the position
    cur_move = d_move[dir + cur_mirror]
    # move the beam
    l_pos = []
    for c in cur_move:
        new_pos = move_beam(pos, c, cur_shape)
        if new_pos[0] >= 0 and new_pos[1] >= 0:
            l_pos.append((new_pos, c))
    return l_pos
    
def read_contraption(text: str) -> np.ndarray[str,str]:
    """
    read the text as a matrix
    """
    mat = [[y for y in list(x)] for x in text.split("\n") if len(x) > 0]
    return np.array(mat)

def list_beam_unique(l_beams: list[(int,int, str)]) -> list[((int,int), str)]:
    """
    consider only unique values in the list of beams
    """
    unique_beams = OrderedDict()
    for x in l_beams:
        unique_beams.setdefault(x, 0)
        unique_beams[x] += 1
    return list(unique_beams.keys())


def beam_contraption(contraption = ndarray[str,str], 
                     start_pos = (0,0), start_dir = 'r') -> ndarray[int,int]:
    """
    run the beam light through the contraption using an ndarray
    """
    M_e = np.zeros(contraption.shape)
    M_e_old = np.zeros(contraption.shape) 
    n_cells = contraption.shape[0] * contraption.shape[1]
    n_steps = 1
    l_running_beams = [(start_pos, start_dir)]
    while len(l_running_beams) > 0:
        # Keep a copy of the old energized cells
        if n_steps % 10 == 0 :
            #print("Step", n_steps, "n. running beams:", len(l_running_beams))
            #print("Energized cells: ", np.sum(M_e != 0, axis = None))
            #print(M_e)
            if np.all((M_e_old != 0) == (M_e != 0)):
                print("Found it, n energized cells:", np.sum(M_e != 0, axis = None))
                #print(M_e_old)
                #print(M_e)
                break 
            #print("Copy of M_e_old")
            M_e_old = np.copy(M_e)
        #Get current beam
        new_beams = []
        for cur_pos, cur_dir in l_running_beams:
            #Energize current cell
            M_e[cur_pos] += 1
            #Apply the beam for the whole list
            new_beams += beam_cell(contraption, cur_pos, cur_dir)
        l_running_beams = list_beam_unique(new_beams)
        n_steps += 1
    return M_e

M_test = np.array([[y for y in list(x)] for x in test.split("\n")])

for x in range(M_test.shape[0]):
    E_test = beam_contraption(M_test, start_pos=(x,0), start_dir = "r")
    E_test = beam_contraption(M_test, start_pos=(x,M_test.shape[1]-1), start_dir = "l")

for y in range(M_test.shape[1]):
    E_test = beam_contraption(M_test, start_pos=(0,y), start_dir = "d")
    E_test = beam_contraption(M_test, start_pos=(M_test.shape[0]-1, y), start_dir = "u")

filename = "./input_day16.txt"
fin = open(filename, "r")
textfull = fin.read().rstrip()
fin.close()

M_full = np.array([[y for y in list(x)] for x in textfull.split("\n")])

l_E = []
for x in range(M_full.shape[0]):
    E_full = beam_contraption(M_full, start_pos=(x,0), start_dir = "r")
    l_E.append(E_full)
    E_full = beam_contraption(M_full, start_pos=(x,M_full.shape[1]-1), start_dir = "l")
    l_E.append(E_full)

for y in range(M_full.shape[1]):
    E_full = beam_contraption(M_full, start_pos=(0,y), start_dir = "d")
    l_E.append(E_full)
    E_full = beam_contraption(M_full, start_pos=(M_full.shape[0]-1, y), start_dir = "u")
    l_E.append(E_full)

N_energy = [np.sum(E != 0, axis = None) for E in l_E]
#E_full = beam_contraption(M_full)