import sys
import pathlib
import re

test="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

def extract_numbers(string):
    return [int(m.group()) for m in re.finditer("[-]?[0-9]+", string)]

def diff(numbers: list[int]) -> list[int]:
    result = [0] * (len(numbers) - 1)
    for i in range(1, len(numbers)):
        result[i-1] = numbers[i] - numbers[i-1]
    return result

def predict_next(numbers: list[int]) -> int:
    d = diff(numbers)
    if all(n==0 for n in d):
        return numbers[0]
    return numbers[-1] + predict_next(d)

def predict_previous(numbers: list[int]) -> int:
    d = diff(numbers)
    if all(n==0 for n in d):
        return numbers[0]
    return numbers[0] - predict_previous(d)

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    # lines = test.split("\n")

    s_next = s_previous = 0
    for line in lines:
        numbers = extract_numbers(line)
        s_next += predict_next(numbers)
        s_previous += predict_previous(numbers)
    print(s_next)
    print(s_previous)


if __name__ == "__main__":
    main()