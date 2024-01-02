from collections import OrderedDict
import numpy as np
import csv

test_text = """
Time:      7  15   30
Distance:  9  40  200"""

def computePossibleRaces(duration):
    """
    int * int -> np.array[int]
    From a maximum duration and a record of length, 
    compute the number of race combination that are compatible with 
    the 
    """
    time_pressed = np.arange(duration+1)
    speed = time_pressed*1
    course_length = (duration - time_pressed) * speed

    return course_length

def computeNBestRaces(duration, bestlength):
    """
    int * int -> int
    """
    p_races = computePossibleRaces(duration)
    return np.sum(p_races > bestlength)

filename = "./input6_table.csv"

l_nbest = []

with open(filename, newline = '') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        ctime, cbestlength = [int(x) for x in row]
        nbest = computeNBestRaces(ctime, cbestlength)
        print(row, ":", nbest)
        l_nbest.append(nbest)

print (l_nbest)
print(np.prod(l_nbest))


realtime = 46689866
realdist = 358105418071080