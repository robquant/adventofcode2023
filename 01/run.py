import sys
import pathlib

def first_last_digit(line: str) -> (int, int):
    first, last = None, None
    for c in line:
        if c.isdigit():
            if first is None:
                first = int(c)
            last = int(c)
    return first, last

def part1(lines: list[str]) -> int:
    s = 0
    for line in lines:
        first, last = first_last_digit(line)
        s += first * 10 + last
    return s

def part2(lines: list[str]) -> int:
    digit_word_to_digit = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }
    s = 0
    for line in lines:
        digit_pos: list[tuple[int, int]] = []
        for pos, char in enumerate(line):
            if char.isdigit():
                digit_pos.append((pos, int(char)))
        for digit_word in digit_word_to_digit:
            if (word_pos := line.find(digit_word)) != -1:
                digit_pos.append((word_pos, digit_word_to_digit[digit_word]))
            if (word_pos := line.rfind(digit_word)) != -1:
                digit_pos.append((word_pos, digit_word_to_digit[digit_word]))
        digit_pos.sort(key = lambda p: p[0])
        first, last = digit_pos[0][1], digit_pos[-1][1]
        s += first * 10 + last
        # print(line, digit_pos, '->', first * 10 + last)

    return s



def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = "two1nine eightwothree abcone2threexyz xtwone3four 4nineeightseven2 zoneight234 7pqrstsixteen eighthree sevenine oneight xtwone3four three7one7 eightwothree oooneeone eight7eight".split()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()