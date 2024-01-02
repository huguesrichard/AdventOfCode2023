from collections import OrderedDict

all_test_text = \
"""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def prepareMappingInfos(map_string):
    """
    str -> list[(int, int, int)]
    From a mapping defined as multiple lines, 
    returns a list of Tuple of 3 int
    Example the strint: 
        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15
    will return the list [(0,15,37), (37,52,2), (39,0,15)]
    """
    l_strmaps = map_string.split("\n")
    name = l_strmaps[0]
    l_maps = [tuple(int(t) for t in x.split(" ")) for x in l_strmaps[1:] if len(x) > 0]
    return (name,l_maps)

def mapFromTo(source_val, mapping_infos):
    """
    int * list[(int, int, int)] -> int
    from a source value, and a list of mapping informations
    will return the corresponding destination value
    """
    destination_val = source_val
    l_dest_candidate = []
    for destination_start, source_start, srange in mapping_infos: 
        if source_start <= source_val < source_start + srange:
            destination_candidate = destination_start + source_val - source_start
            l_dest_candidate.append(destination_candidate)
    if len(l_dest_candidate) > 0:
       destination_val = min(l_dest_candidate)
    return destination_val

def seeds2ranges(l_seeds):
    """
    list[int] -> list[(int,int)]
    converts the list of seeds to a list of tuples (seeds_start, range)
    """
    return [(l_seeds[i], l_seeds[i+1]) for i in range(0, len(l_seeds), 2)]


def is_overlap(sA, eA, sB, eB):
    """
    int * int * int * int -> bool
    return True if [sA;eA[ and [sB; eB[ overlap
    """
    return not(eA <= sB or sA >= eB)

def is_ovrange(sA, rA, sB, rB):
    """
    Same as above taking range values
    """
    return is_overlap(sA, sA+rA, sB, sB+rB)

def compute_overlap(sA, rA, sB, rB):
    """
    int * int * int * int -> (list[(int,int)], list[(int, int)])
    Processes the overlap between two intervals [sA;sA+rA[ and [sB; sB+rB[
    (note the exclusive end)
    Returns two lists corresponding to:
    - the overlapping part 
    - the **not** overlapping part from A 
    """
    eA, eB = sA + rA, sB + rB
    ov = []
    nonov = []
    if not is_overlap(sA, eA, sB, eB):
        nonov.append((sA, rA))
    else:
        sOv = (max(sA, sB), min(eA, eB))
        sleft = (sA, max(sA, sB))
        sright = (min(eA,eB), eA )
        ov.append((sOv[0], sOv[1]- sOv[0]))
        if sleft[1] != sleft[0]:
            nonov.append((sleft[0], sleft[1]-sleft[0]))
        if sright[1] != sright[0]:
            nonov.append((sright[0], sright[1] - sright[0]))
    return [ov, nonov]

def mapFromListRangeTo(l_sources, mapping_infos):
    """
    list[(int,int)] * list[(int, int, int)] -> list[(int, int)]
    from a list of (source value, range), 
    and a list of mapping informations
    returns the corresponding list of mapped destination values and their ranges
    """
    ## We keep track of the ranges that are not mapped yet
    ## and we update the mapped ones to give the new values
    l_source_mapped = []
    for source_val, range in l_sources:
        ##We consider each source range separately
        l_source_notmapped = [(source_val, range)]
        for destination_start, source_start, srange in mapping_infos:
            ## We test it on all the possible overlap in sequence
            ## if it overlap partly we add that to the mapped and we keep what 
            ## was not mapped
            csource, crange = l_source_notmapped.pop(0)
            coverlap, cnooverlap = compute_overlap(csource, crange, source_start, srange)
            if len(coverlap) > 0:
                #print(coverlap)
                ovstart, ovrange = coverlap[0]
                destination_candidate = destination_start + ovstart - source_start
                cmap = (destination_candidate, ovrange)
                l_source_mapped.append(cmap)
            if len(cnooverlap) > 0:
                l_source_notmapped += cnooverlap 
            if len(l_source_notmapped) == 0:
                break

        ###after testing all overlaps we transfer the non mapped to the mapped directly
        if len(l_source_notmapped) > 0:
            l_source_mapped += l_source_notmapped
    return l_source_mapped

def parse_input(text):
    """
    str -> (list[int], dict(str:list[int])
    Parses the input as a large text files and returns:
    - the list of seeds
    - the list of mappings
    """
    l_infos = text.split("\n\n")
    seeds = [int(x) for x in l_infos[0].split(":")[1].strip().split(" ")]
    l_all_mappings = OrderedDict([prepareMappingInfos(x) for x in l_infos[1:]])
    return (seeds, l_all_mappings)

def moveOneSeed(seed, d_mapping):
    """
    int * OrderedDict -> list[int]
    moves one seed from the start of the mapping to the end and 
    return the list of all values obtained
    """
    chain = [seed]
    cseed = seed
    for cmapping in d_mapping.values():
        cseed = mapFromTo(cseed, cmapping)
        chain.append(cseed)
    return chain

def moveAllSeedRanges(l_seeds, d_mapping):
    """
    list[(int,int)] * OrderedDict -> list[(int,int)]
    moves all the seeds with their ranges through the mappings
    """
    clseed = l_seeds[:]
    print("Seeds orig:", clseed)
    for cname, cmapping in d_mapping.items():
        clseednew = mapFromListRangeTo(clseed, cmapping)
        clseed = clseednew[:]
        print("***",cname,":\n", clseed)
    return clseed

tseeds, tmappings = parse_input(all_test_text)
tseedsrange= seeds2ranges(tseeds)

tt = moveAllSeedRanges(tseedsrange, tmappings)
uu = set(sorted([x[0] for x in tt]))

for s in tseeds:
    l = moveOneSeed(s, tmappings)
    #print(l)



filename = "./input_day5.txt"
fin = open(filename, "r")
all_text = fin.read()
fin.close()

seeds, mappings = parse_input(all_text)
seeds_range = seeds2ranges(seeds)
all_last_vals = []
for s in seeds:
     ll = moveOneSeed(s, mappings)
     last_val = ll[-1]
     all_last_vals.append(last_val)

aa = moveAllSeedRanges(seeds_range, mappings)
bb = set(sorted([x[0] for x in aa]))

#print(all_last_vals)
#print(min(all_last_vals))

###Before doing q2, we verify that there are no overlaps between the mappings
###

toto = [ [is_ovrange(a[i][1], a[i][2], a[j][1], a[j][2]) 
          for i in range(len(a)) for j in range(i+1, len(a))] 
            for a in mappings.values()]

ov_inmaps = [any(x) for x in toto]