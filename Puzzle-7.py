from collections import OrderedDict
from collections import Counter
import operator 
import re


dict_cards = {"A": "a",
              "K": "b",
              "Q": "c",
              "J": "d",
              "T": "e",
              "9": "f",
              "8": "g",
              "7": "h",
              "6": "i",
              "5": "j",
              "4": "k",
              "3": "l",
              "2": "m"}

cards_letters =     "AKQJT98765432"
cards_ltranslate =  "abcdefghijklm"
cards_ltransjoker = "abcmdefghijkl"

test = ["32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
        ]


def handLabeller(cards):
    """
    str -> str
    A function that assigns an hand one of possible types:
    - Five of a kind: H1
    - Four of a kind: H2
    - Full house : H3
    - Three of a kind: H4
    - Two pair: H5
    - one pair : H6
    - High card: H7
    """
    cards_counted = Counter(list(cards))
    cardcounts = cards_counted.values()
    if 5 in cardcounts:
        return "H1"
    elif 4 in cardcounts:
        return "H2"
    elif 3 in cardcounts and 2 in cardcounts:
        return "H3"
    elif 3 in cardcounts:
        return "H4"
    elif 2 in cardcounts:
        if Counter(cardcounts)[2] == 2:
            return "H5"
        else:
            return "H6"
    else:
        return "H7"

def handLabellerJoker(cards):
    """
    str -> str
    labelling an hand with the rule that J can help any combination
    """
    cards_counted = Counter(list(cards))
    cardcounts = cards_counted.values()
    joker_counts = cards_counted.get("J", 0)
    cardcounts = sorted(list(cardcounts))
    maxcardcount = cardcounts[-1]
    second_best_card_count = cardcounts[-2] if len(cardcounts) > 1 else 0
    if joker_counts == maxcardcount:
        best_card_count = joker_counts + second_best_card_count
    else:
        best_card_count = cardcounts[-1] + joker_counts
    if best_card_count == 5:
        return "H1"
    elif best_card_count == 4:
        return "H2"
    elif best_card_count == 3 and second_best_card_count == 2 :
        return "H3"
    elif best_card_count == 3:
        return "H4"
    elif best_card_count == 2:
        if second_best_card_count == 2:
            return "H5"
        else:
            return "H6"
    else:
        return "H7"



def cardTranslate(chand, translator = cards_ltranslate ):
    """
    str -> str
    Translate the cards hand chand into a list of letters for lexicographical comparison
    """
    return chand.translate(str.maketrans(cards_letters, translator))

def sortHands(l_hands):
    """
    list[str] -> list[int]
    """
    l_hands_translated = [(i, hand, handLabeller(hand), cardTranslate(hand, cards_ltranslate)) 
                          for i,hand in enumerate(l_hands)]
    l_hands_sorted = sorted(l_hands_translated, key = operator.itemgetter(2,3), 
                            reverse = True)
    
    return l_hands_sorted

def sortHandsJoker(l_hands):
    """
    """ 
    l_hands_translated = [(i, hand, handLabellerJoker(hand), 
                                    cardTranslate(hand, translator = cards_ltransjoker)) 
                          for i,hand in enumerate(l_hands)]
    l_hands_sorted = sorted(l_hands_translated, key = operator.itemgetter(2,3), 
                            reverse = True)
    return l_hands_sorted


def scoreHands(l_hands_with_bets, scoring = "N"):
    """
    list[(str,str)] * str-> int
    scoring parameter can be:
    - "N" for Normal
    - "J" for Joker
    """
    l_hands = [x[0] for x in l_hands_with_bets]
    l_bets = [int(x[1]) for x in l_hands_with_bets]
    if scoring == "N":
        l_hands_sorted = sortHands(l_hands)
    elif scoring == "J":
        l_hands_sorted = sortHandsJoker(l_hands)
    else:
        print ("Scoring type not known:", scoring)
        raise

    l_bets_scored = [l_bets[l_hands_sorted[i][0]] * (i+1) for i in range(len(l_hands_sorted))]
    return l_bets_scored

test_with_bets = [x.split(" ") for x in test]
test_cards = [x[0] for x in test_with_bets]

sh = sortHands(test_cards)
testbets = scoreHands(test_with_bets)

fin = open("./input_day7.txt", "r")
all_hands_with_bets = [l.rstrip().split(" ") for l in fin]
fin.close() 

all_cards = [x[0] for x in all_hands_with_bets]

all_cards_sorted_Joker = sortHandsJoker(all_cards)

allhands_bets = scoreHands(all_hands_with_bets)

allhands_sorted = sortHands([x[0] for x in all_hands_with_bets])

print(sum(allhands_bets))
### Let's try with jokers:

