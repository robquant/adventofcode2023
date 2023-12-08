import math
import re
import sys
import pathlib

test = """Time:      7  15   30
Distance:  9  40  200"""


def numbers(string):
    return [int(m.group()) for m in re.finditer("[0-9]+", string)]

def t_press(t_total, d):
    D = math.sqrt(t_total**2/4 - d)
    return t_total/2 - D, t_total/2 + D

def part1(times, distances):
    p = 1
    for t, dist in zip(times, distances):
        t_1, t_2 = t_press(t, dist)
        if t_1 == math.ceil(t_1):
            t_1 += 1
        t_1 = math.ceil(t_1)
        if t_2 == math.floor(t_2):
            t_2 -= 1
        t_2 = math.floor(t_2)
        n_beat = t_2 - t_1 + 1
        print(t_1, t_2, "->", n_beat)
        p *= n_beat
    return p


def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = test.split("\n")

    times = numbers(lines[0])
    distances = numbers(lines[1])
    print(part1(times, distances))

    times = numbers(lines[0].replace(" ", ""))
    distances = numbers(lines[1].replace(" ", ""))
    print(part1(times, distances))

if __name__ == "__main__":
    main()