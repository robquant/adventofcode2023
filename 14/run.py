from calendar import c
import sys
import pathlib

ROUND_ROCK = "O"
SQUARE_ROCK = "#"
EMPTY = "."


test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

def tilt_col(field:list[list[str]], col:int):
    last_free = None
    nrows = len(field)
    for row in range(nrows):
        rock_type = field[row][col]
        match rock_type:
            case "O":
                if last_free is not None:
                    # print(f"Moving {row} to {last_free}")
                    field[last_free][col] = "O"
                    field[row][col] = "."
                    last_free += 1
                    # print(f"Last free {last_free}, last blocked {last_blocked}")
            case ".":
                # print(f"Last free {row}")
                if last_free is None:
                    last_free = row
            case "#":
                last_free = None
    return

def rotate_right(field:list[list[str]]):
    nrows = len(field)
    ncols = len(field[0])
    new_field = [[None] * nrows for _ in range(ncols)]
    for row in range(nrows):
        for col in range(ncols):
            new_field[col][nrows - row - 1] = field[row][col]
    return new_field

def calculate_load(field:list[list[str]]):
    s = 0
    for i_row, row in enumerate(reversed(field)):
        s += (i_row + 1) * sum(rock == "O" for rock in row)
    return s

def tilt_north(field:list[list[str]]):
    ncols = len(field[0])
    for col in range(ncols):
        tilt_col(field, col)
    return

def hash_field(field:list[list[str]]):
    return hash(tuple(tuple(row) for row in field))

def part1(field:list[list[str]]):
    tilt_north(field)
    return calculate_load(field)

def part2(field:list[list[str]]):
    cycle_hashes = {}
    def cycle(field:list[list[str]]):
        for _ in range(4):
            tilt_north(field)
            field = rotate_right(field)
        return field
    cycle_counter = 0
    while True:
        field = cycle(field)
        cycle_counter += 1
        h = hash_field(field)
        if h in cycle_hashes:
            repeat = cycle_counter - cycle_hashes[h]
            left = (1000000000 - cycle_counter) % repeat
            break
        cycle_hashes[h] = cycle_counter
    for _ in range(left):
        field = cycle(field)
    return calculate_load(field), field

def print_field(field:list[list[str]]):
    for row in field:
        print("".join(row))
    return

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = [line.rstrip("\n") for line in open(pathlib.Path(__file__).parent / "input")]
    # lines = test.split("\n")

    field = [list(line) for line in lines]

    print(part1(field))
    score, field = part2(field)
    print(score)

if __name__ == "__main__":
    main()