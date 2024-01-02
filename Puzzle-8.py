from collections import OrderedDict
from collections import namedtuple
import operator
from collections import Counter
from math import lcm

import re

test = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

vertex = namedtuple('vertex', ['L', 'R'])

def addEdge(d_net, text):
    """
    dict[str: vertex(str,str) ] * str -> None
    Add the edge corresponding to the text to the dictionnary of 
    source : (left edge, right edge)
    """
    search_node = re.search('([A-Z123]{3}) = \(([A-Z123]{3}), ([A-Z123]{3})\)', text )
    source = search_node.group(1)
    edge = vertex(search_node.group(2), search_node.group(3))
    d_net[source] = edge
    return None

def buildNetwork(l_text):
    """
    list[str] -> dict[str: vertex(str,str) ]
    from a text containing all the edges information, 
    constructs the network
    """
    dn = dict()
    for t in l_text:
        addEdge(dn, t)
    return dn

def followInstructions(pattern, d_net, start = "AAA", l_end = ["ZZZ"]):
    """
    str * dict[str: vertex(str,str)] -> int
    follow the pattern of L and R instructions until the target is found (ZZZ)
    and returns the number of steps (old version: path)
    """
    path = []
    cnode = start
    i = 1
    steps = 0
    while not cnode in l_end:
        #print ("Pattern check n.", i)
        for cmove in pattern:
            #print(cnode, cmove)
            path.append((cnode, cmove))
            steps += 1
            cnode = getattr(d_net[cnode], cmove)
            #print("***", cnode)
        i+=1
        if i<0 :
            break 
    print("Finished the loops with a total of steps:", steps)
    #return path
    return steps

def followInstructionsMulti(pattern, d_net):
    """
    str * dict[str: vertex(str,str)] -> int
    """
    l_starts = [x for x in d_net.keys() if x[-1] == "A"]
    l_ends = [x for x in d_net.keys() if x[-1] == "Z"]
    print("The starts", l_starts)
    print("The ends:", l_ends )
    l_steps = [followInstructions(pattern, d_net, start = s, l_end = l_ends) 
               for s in l_starts]
    return lcm(*l_steps)


def followInstructionsMultiold(pattern, d_net):
    """
    str * dict[str: vertex(str,str)] -> int
    """
    l_starts = [x for x in d_net.keys() if x[-1] == "A"]
    l_ends = [x for x in d_net.keys() if x[-1] == "Z"]
    print("The starts", l_starts)
    print("The ends:", l_ends )
    paths = []
    l_cnodes = l_starts[:]
    i = 1
    steps = 0
    while not set(l_cnodes).issubset(l_ends):
        if i%10000 == 0:
            print ("Pattern check n.", i, "n cnodes diff:", len(set(l_cnodes)))
            print ("N nodes ending with Z:", len([x for x in l_cnodes if x[-1]=="Z"]))
            print ("-- n steps:", steps)
        for cmove in pattern:
            #print(l_cnodes, cmove)
            #paths.append((l_cnodes, cmove))
            steps += 1
            l_cnodes = [getattr(d_net[cn], cmove) for cn in l_cnodes]
            if set(l_cnodes).issubset(l_ends):
                print("***** Reach all the end nodes within pattern at step", steps)
        i+=1
        #if i > 10000:
        #    break
    print("Finished the loops with a total of:", steps)
    return steps

#pattern, netdef = test.split("\n\n")
pattern, netdef = test2.split("\n\n")
test_text = [x for x in netdef.split("\n") if len(x) >0]

d_test = buildNetwork(test_text)

filename = "./input_day8.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

all_patt, all_netdef = textfull.split("\n\n")

all_text = [x for x in all_netdef.split("\n") if len(x) >0]

d_all = buildNetwork(all_text)

