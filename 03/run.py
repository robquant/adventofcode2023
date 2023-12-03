import sys
import pathlib
from dataclasses import dataclass
import re
from collections import defaultdict

test="""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

@dataclass(frozen=True)
class Number:
    value: int
    row: int
    start_col: int
    end_col: int # Column index of last digit

def find_numbers(field: list[str]):
    numbers = []
    for i_row, row in enumerate(field):
        number_matches = re.finditer(r"[0-9]+", row)
        if number_matches:
            for number in number_matches:
                numbers.append(Number(int(number[0]), i_row, number.start(), number.end() - 1))
    return numbers

def neighbours(n_row, n_col, pos):
    row, col = pos
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dx == 0 and dy == 0: continue
            if 0 <= row + dy < n_row and 0 <= col + dx < n_col:
                yield (row + dy, col + dx)

def part1(field, numbers):
    s = 0
    n_rows = len(field)
    n_cols = len(field[0])
    for number in numbers:
        found_symbol = False
        for col in range(number.start_col, number.end_col + 1):
            for n in neighbours(n_rows, n_cols, (number.row, col)):
                val = field[n[0]][n[1]]
                if not val.isdigit() and val != '.':
                    # print(number, "for", n, "value", val)
                    s += number.value
                    found_symbol = True
                    break
            if found_symbol:
                break
    return s

def part2(field, numbers):
    gears = defaultdict(set)
    n_rows = len(field)
    n_cols = len(field[0])
    for number in numbers:
        for col in range(number.start_col, number.end_col + 1):
            for n in neighbours(n_rows, n_cols, (number.row, col)):
                val = field[n[0]][n[1]]
                if val == "*":
                    gears[n].add(number)
    s = 0
    for gear in gears:
        ratio = 1
        if len(gears[gear]) == 2:
            for number in gears[gear]:
                ratio *= number.value
            s += ratio
    return s

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines=test.split("\n")
    field = [line.rstrip("\n") for line in lines]
    numbers = find_numbers(field)
    print(part1(field, numbers))
    print(part2(field, numbers))

if __name__ == "__main__":
    main()