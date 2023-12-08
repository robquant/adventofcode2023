import sys
import pathlib
import re

test = """"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""



def numbers(string):
    return [int(m.group()) for m in re.finditer("[0-9]+", string)]

def part1(cards):
    s = 0
    for winning_numbers, my_numbers in cards:
        n_winning = len(set(winning_numbers) &  set(my_numbers))
        if n_winning > 0:
            s += 2 ** (n_winning - 1)
    return s

def part2(cards):
    card_counts = [1] * len(cards)
    for i, (winning_numbers, my_numbers)  in enumerate(cards):
        n_winning = len(set(winning_numbers) &  set(my_numbers))
        if n_winning > 0:
            for j in range(n_winning):
                card_counts[i + j + 1] += card_counts[i]
    return sum(card_counts)

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = test.split("\n")

    cards = []
    for line in lines:
        winning_numbers = numbers(line[line.find(":"):line.find("|")])
        my_numbers = numbers(line[line.find("|"):])
        cards.append((winning_numbers, my_numbers))

    print(part1(cards))
    print(part2(cards))

if __name__ == "__main__":
    main()