import sys
import pathlib
import re

def numbers(string):
    return [int(m.group()) for m in re.finditer("[0-9]+", string)]

def parse_seeds(lines, i):
    line = lines[i]
    seeds = numbers(line)
    return seeds, i + 1

def parse_map(lines, i):
    line = lines[i]
    items = line.split(" ")[0].split("-")
    src_name, dst_name = items[0], items[2]
    i += 1
    ranges = []
    while len(lines) > i and len(lines[i]) > 1:
        line = lines[i]
        dst, src, l = numbers(line)
        ranges.append(((src, src + l), (dst, dst + l)))
        i += 1
    return i, src_name, dst_name, ranges

def map_to_location(src, val, maps):
    if src == "location":
        return val
    dst, ranges = maps[src]
    for ((src_start, src_end), (dst_start, _)) in ranges:
        if src_start <= val <= src_end:
            dst_val = val - src_start + dst_start
            return map_to_location(dst, dst_val, maps)
    return map_to_location(dst, val, maps)



def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = open(pathlib.Path(__file__).parent / "testdata").readlines()

    maps = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("seeds"):
            seeds, i = parse_seeds(lines, i)
        elif " map" in line:
            i, src, dst, ranges = parse_map(lines, i)
            maps[src] = (dst, ranges)
        else:
            i += 1

    locations = []
    for seed in seeds:
        location = map_to_location("seed", seed, maps)
        locations.append(location)
    print(min(locations))

if __name__ == "__main__":
    main()