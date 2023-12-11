import sys
import pathlib
from itertools import combinations

test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def distance(g1, g2, cumulative_rows, cumulative_cols):
    r1, c1 = g1
    r2, c2 = g2
    r1, r2 = min(r1, r2), max(r1, r2)
    c1, c2 = min(c1, c2), max(c1, c2)
    return cumulative_rows[r2] - cumulative_rows[r1] + cumulative_cols[c2] - cumulative_cols[c1]

def is_empty_row(field, row):
    return all(c == '.' for c in field[row])

def is_empty_col(field, col):
    return all(line[col] == '.' for line in field)

def cumulative_rows_and_cols(lines, expansion_factor):
    n_rows = len(lines)
    n_cols = len(lines[0])
    cumulative_rows = {}
    total_offset = 0
    for i_row in range(n_rows):
        if is_empty_row(lines, i_row):
            total_offset += expansion_factor - 1
        else:
            cumulative_rows[i_row] = i_row + total_offset
    cumulative_cols = {}
    total_offset = 0
    for i_col in range(n_cols):
        if is_empty_col(lines, i_col):
            total_offset += expansion_factor - 1
        else:
            cumulative_cols[i_col] = i_col + total_offset
    return cumulative_rows, cumulative_cols

def distance_sum(galaxies, cumulative_rows, cumulative_cols):
    s = 0
    for g1, g2 in combinations(galaxies, 2):
        s += distance(g1, g2, cumulative_rows, cumulative_cols)
    return s

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = [line.rstrip("\n") for line in open(pathlib.Path(__file__).parent / "input")]
    # lines = test.split("\n")


    galaxies = []
    for i_row, row in enumerate(lines):
        for i_col, chr in enumerate(row):
            if chr == "#":
                galaxies.append((i_row, i_col))


    cumulative_rows, cumulative_cols = cumulative_rows_and_cols(lines, expansion_factor=2)
    print(distance_sum(galaxies, cumulative_rows, cumulative_cols))
    cumulative_rows, cumulative_cols = cumulative_rows_and_cols(lines, expansion_factor=int(1e6))
    print(distance_sum(galaxies, cumulative_rows, cumulative_cols))

if __name__ == "__main__":
    main()