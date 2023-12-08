from enum import IntEnum
from collections import Counter
import sys
import pathlib

test = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

CARD_VALUES = {"A":12, "K":11, "Q":10, "J":9, "T":8, "9":7, "8":6, "7":5, "6":4, "5":3, "4":2, "3":1, "2":0}
CARD_VALUES_JOKER_RULE = {"A":12, "K":11, "Q":10, "T":8, "9":7, "8":6, "7":5, "6":4, "5":3, "4":2, "3":1, "2":0, "J":-1}

class HandType(IntEnum):
    FIVE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 8
    THREE_OF_A_KIND = 7
    TWO_PAIRS = 6
    ONE_PAIR = 5
    HIGH_CARD = 4

    def __str__(self):
        return self.name

def card_counts_to_hand_type(values: list[int]) -> HandType:
    if values == [5]:
        return HandType.FIVE_OF_A_KIND
    elif values[0] == 4:
        return HandType.FOUR_OF_A_KIND
    elif values == [3,2]:
        return HandType.FULL_HOUSE
    elif values[0] == 3:
        return HandType.THREE_OF_A_KIND
    elif values[0] == 2 and values[1] == 2:
        return HandType.TWO_PAIRS
    elif values[0] == 2:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD

def calc_hand_type(cards: str) -> HandType:
    c = Counter(cards)
    values = list(sorted(c.values(), reverse=True)) # Highest count first
    return card_counts_to_hand_type(values)

def calc_hand_type_with_joker_rule(cards: str) -> HandType:
    jokers = cards.count("J")
    c = Counter(cards.replace("J",""))
    values = list(sorted(c.values(), reverse=True)) # Highest count first
    if jokers == 5:
        values = [5]
    else:
        values[0] += jokers
    return card_counts_to_hand_type(values)

    # if values == [5]:
    #     return HandType.FIVE_OF_A_KIND
    # elif values[0] == 4:
    #     if jokers == 1:
    #         return HandType.FIVE_OF_A_KIND
    #     return HandType.FOUR_OF_A_KIND
    # elif values == [3,2]:
    #     return HandType.FULL_HOUSE
    # elif values[:2] == [3,1] and jokers == 1:
    #     return HandType.FULL_HOUSE
    # elif values[0] == 3:
    #     if jokers == 2:
    #         return HandType.FIVE_OF_A_KIND
    #     elif jokers == 1:
    #         return HandType.FOUR_OF_A_KIND
    #     return HandType.THREE_OF_A_KIND
    # elif values[0] == 2 and values[1] == 2:
    #     if jokers == 1:
    #         return HandType.FULL_HOUSE
    #     return HandType.TWO_PAIRS
    # elif values[0] == 2:
    #     if jokers == 3:
    #         return HandType.FIVE_OF_A_KIND
    #     return HandType.ONE_PAIR
    # if jokers == 5:
    #     return
    # return HandType.HIGH_CARD

class Hand:
    def __init__(self, cards: str, bid: int, joker_rule: bool = False):
        self.cards = cards
        if joker_rule:
            self.card_values:list[int] = [CARD_VALUES_JOKER_RULE[c] for c in cards]
            self.hand_type = calc_hand_type_with_joker_rule(cards)
        else:
            self.card_values:list[int] = [CARD_VALUES[c] for c in cards]
            self.hand_type = calc_hand_type(cards)
        self.bid = bid

    def __eq__(self, other):
        return (self.hand_type, self.card_values) == (other.hand_type, other.card_values)

    def __lt__(self, other):
        return (self.hand_type, self.card_values) < (other.hand_type, other.card_values)

    def __str__(self):
        return f"({self.cards}, {self.bid}, {self.hand_type})"

    def __repr__(self):
        return str(self)

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = test.split("\n")

    hands = []
    for line in lines:
        cards, bid = line.split(" ")
        bid = int(bid)
        hand = Hand(cards, bid)
        hands.append(hand)

    s = 0
    for rank, hand in enumerate(sorted(hands)):
        # print(hand)
        s += (rank + 1) * hand.bid
    print(s)


    hands = []
    for line in lines:
        cards, bid = line.split(" ")
        bid = int(bid)
        hand = Hand(cards, bid, joker_rule=True)
        hands.append(hand)

    s = 0
    for rank, hand in enumerate(sorted(hands)):
        # print(hand)
        s += (rank + 1) * hand.bid
    print(s)

if __name__ == "__main__":
    main()