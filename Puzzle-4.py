

test = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]

def nwinCard(text):
    """
    str -> int
    reads a scratch card info and return the number of winning
    numbers
    """
    Cardnum, numbers = text.split(":")
    winning, mine = numbers.split("|")
    l_win = [int(x.strip()) for x in winning.split()]
    l_mine = [int(x.strip()) for x in mine.split()]
    nwin = len(set(l_win) & set(l_mine))
    #print(Cardnum, nwin, l_win, l_mine)
    return nwin

def winScratchCard(text):
    """
    str -> int
    Read a scractch card info and return the number of points
    """
    nwin = nwinCard(text)
    return int(2**(nwin-1))


def cumulCards(l_text):
    """
    list[str] -> list[int]
    compute the cumulated sum of all card copies over the whole text
    """
    ncards = len(l_text)
    ncopy = [1] * ncards
    for i,scard in enumerate(l_text):
        nwin = nwinCard(scard)
        for j in range(nwin):
            if i+j+1 < ncards:
                ncopy[i+j+1] += ncopy[i]
    return ncopy

test_wins = [winScratchCard(s) for s in test]

filename = "./input_day4.txt"
with open(filename, "r") as file:
    l_text= [l.rstrip() for l in file.readlines()]

input_wins = [winScratchCard(l) for l in l_text]

test_copies = cumulCards(test)

win_copies = cumulCards(l_text)