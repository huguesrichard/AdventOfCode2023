import numpy as np
from copy import deepcopy

test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

"""

def transpose(l_str: list[str]) -> list[str]:
    """
    transpose a list of list of str
    """
    return [list(x) for x in zip(*l_str)]

def transpose_back(l_str: list[str]) -> list[str]:
    """
    The transpose operation over the other axis
    """
    #first transpose the reversed list
    l_transpose_rev = [list(x) for x in 
                       zip(*[list(reversed(l)) for l in l_str])]
    # Then reverse it again
    l_transpose_rev_rev = [list(reversed(x)) for x in l_transpose_rev]
    return l_transpose_rev_rev


def slide_on_map_north(l_str: list[str]) -> list[str]:
    """
    list[str] -> list[str]
    reads a map and slides the "O" to the north
    """
    l_transpose = transpose(l_str)
    l_trans_slide = [slide_line(x) for x in l_transpose]
    return transpose(l_trans_slide)

def slide_on_map_west(l_str: list[str]) -> list[str]:
    """
    list[str] -> list[str]
    reads a map and slides the "O" to the west
    """
    return [slide_line(x) for x in l_str]

def slide_on_map_south(l_str: list[str]) -> list[str]:
    """
    reads a map and slides the "O" to the south
    """
    #then reverse it again
    l_transpose_back = transpose_back(l_str)
    l_transback_slide = [slide_line(x) for x in l_transpose_back]
    return transpose_back(l_transback_slide)

def slide_on_map_east(l_str: list[str]) -> list[str]:
    """
    now sliding to the east
    """
    l_reversed = [list(reversed(x)) for x in l_str]
    l_rev_slide = [slide_line(x) for x in l_reversed]
    return [list(reversed(x)) for x in l_rev_slide]

def slide_cycle(l_str: list[str]) -> list[str]:
    """
    performs one slide cycle
    """
    l_cycle = slide_on_map_north(l_str)
    l_cycle = slide_on_map_west(l_cycle)
    l_cycle = slide_on_map_south(l_cycle)
    return slide_on_map_east(l_cycle)

def determine_cycle_period(l_str: list[str]) -> list[list[str]]:
    """
    from a map, performs cycles of slides until we got back to the 
    same configuration
    """
    l_str_cycles = [[list(x) for x in l_str]]
    found_period = False
    cycle = 0
    while not found_period:
        l_new_cycle = slide_cycle(l_str_cycles[-1])
        found_period = l_new_cycle in l_str_cycles
        l_str_cycles += [l_new_cycle]
        cycle += 1
        print ("Cycle", cycle)
    loop = [i for i,x in enumerate(l_str_cycles) if x == l_str_cycles[-1]]
    print("Found period at cycle", cycle)
    print("Positions that are looping:", loop[0], "and", loop[1])

    return l_str_cycles
    


def score_slide_map(l_str:list[list[str]]) -> int:
    """
    scores the slided map

    """
    nO = [sum([c == "O" for c in row]) for row in l_str]
    revnO = list(reversed(nO))
    return sum([(i+1)* revnO[i] for i in range(len(revnO))])

def slide_line(l_chars: list[str]) -> list[str]:
    """
    list[str] -> list[str]
    goes from left to right in a string and slides the 
    "0" characters to the left up to :
        - the last "O"
        - the last "#"
    """
    l_out = []
    l_dots = []
    for c in l_chars:
        if c == "O":
            l_out.append(c)
        if c == ".":
            l_dots.append(c)
        if c == "#":
            l_out = l_out + l_dots + [c]
            l_dots = []
    l_out = l_out + l_dots
    return(l_out)


str_test = [x for x in test.split("\n") if len(x) >0]
test_slided = slide_on_map_north(str_test)
test_score = score_slide_map(test_slided)

filename = "./input_day14.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

str_full = [x for x in textfull.split("\n") if len(x) >0]
full_slided = slide_on_map_north(str_full)
full_score = score_slide_map(full_slided)

ncycles = 1000000000
toto = determine_cycle_period(str_test)

#Found period at cycle 97
#Positions that are looping: 88 and 97
(ncycles - 88) % 9 #3

88 + 3 # 91
score_slide_map(toto[91])


