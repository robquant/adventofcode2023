from itertools import repeat
from functools import cache

@cache
def count_arrangements(conditions, rules):
    if not rules:
        return 0 if "#" in conditions else 1
    if not conditions:
        return 1 if not rules else 0

    result = 0
    condition = conditions[0]
    rule = rules[0]

    if condition in ".?":
        result += count_arrangements(conditions[1:], rules)
    if condition in "#?":
        if (
            rule <= len(conditions)
            and "." not in conditions[: rule]
            and (rule == len(conditions) or conditions[rule] != "#")
        ):
            result += count_arrangements(conditions[rule + 1 :], rules[1:])

    return result

if __name__ == "__main__":
    all_rules = []
    all_conditions = []
    for line in open("input"):
        conditions, rules = line.split()
        rules = tuple(int(rule) for rule in rules.split(","))
        all_rules.append(rules)
        all_conditions.append(conditions)

    sum_part1 = 0
    sum_part2 = 0
    for conditions, rules in zip(all_conditions, all_rules):
        sum_part1 += count_arrangements(conditions, rules)
        p2 = count_arrangements("?".join(repeat(conditions, 5)), rules * 5)
        sum_part2 += p2

    print("Part 1:", sum_part1)
    print("Part 2:", sum_part2)