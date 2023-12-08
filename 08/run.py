import sys
import pathlib
import re
import itertools
import math

test="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

def nsteps_to_target(network, path, start_pos, is_target_func):
    steps = 0
    pos = start_pos
    for direction in itertools.cycle(path):
        match direction:
            case "L":
                pos = network[pos][0]
            case "R":
                pos = network[pos][1]
            case _:
                print("Unknown direction")
        steps += 1
        if is_target_func(pos):
            break
    return steps

def part1(network, path):
    start_pos = "AAA"
    nsteps = nsteps_to_target(network, path, start_pos, lambda pos: pos == "ZZZ")
    return nsteps

def part2(network, path):
    all_pos = [p for p in network.keys() if p.endswith("A")]
    nsteps_per_pos = [nsteps_to_target(network, path, p, lambda pos: pos.endswith("Z")) for p in all_pos]
    total = math.lcm(*nsteps_per_pos)
    return total

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = test.split("\n")

    directions = lines[0].rstrip("\n")
    network = {}
    for line in lines[2:]:
        nodes = [m.group(0) for m in re.finditer("[A-Z]{3}", line)]
        network[nodes[0]] = tuple(nodes[1:])

    print(part1(network, directions))
    print(part2(network, directions))

if __name__ == "__main__":
    main()