from functools import reduce
from collections import OrderedDict
import re

test="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def hashing(instructs: str) -> int:
    """
    Hashes a string (s_1, ..., s_n) according to the rule
    h_{n+1} = ((h_n + ord(s_(n+1))) * 17) % 256 
    """
    def hash_next(a,b):
        return ((a+ b) * 17) % 256
    return reduce(hash_next, [0] + [ord(c) for c in instructs])

def init_boxes() -> list[OrderedDict[str:int]]:
    """
    Initialise a list of emoty orderedDict
    """
    return [OrderedDict() for x in range(256)]

def read_instruction(boxes: list[OrderedDict[str:int]], instruction: str) -> None:
    """
    reads an instruction and updates the corresponding list 
     of all commands. 
     It is a list of 256 elements, with each
     element being a dict from label to values
    """
    label, operation, focal_len = re.split("([=-])", instruction)
    box_number = hashing(label)
    if operation == "=":
        boxes[box_number][label] = int(focal_len)
    elif operation == "-":
        if label in boxes[box_number]:
            boxes[box_number].pop(label)
    else:
        print("Error")


vals_test = [hashing(s) for s in test.rstrip().split(",")]
str_test = test.rstrip().split(",")

test_boxes = init_boxes()
for inst in str_test:
    read_instruction(test_boxes, inst)

l_sum = []
for bn,box in enumerate(test_boxes):
    slot = 1
    csum = 0
    for focal_len in box.values():
        csum += (bn+1) * slot * focal_len
        slot += 1
    l_sum.append(csum)


filename = "./input_day15.txt"
fin = open(filename, "r")
textfull = fin.read().rstrip()
fin.close()

vals_tot = [hashing(s) for s in textfull.rstrip().split(",")]
str_tot = textfull.rstrip().split(",")

full_boxes = init_boxes()
for inst in str_tot:
    read_instruction(full_boxes, inst)

tot_sum = []
for bn,box in enumerate(full_boxes):
    slot = 1
    csum = 0
    for focal_len in box.values():
        csum += (bn+1) * slot * focal_len
        slot += 1
    tot_sum.append(csum)

print(sum(tot_sum))

