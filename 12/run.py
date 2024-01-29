from itertools import repeat

def count_arrangements(conditions, rules):

    cache = [None for _ in range(len(rules) * len(conditions))]

    def count_from(cond_index, rule_index):
        nonlocal cache

        if rule_index == len(rules):
            if cond_index < len(conditions) and "#" in conditions[cond_index:]:
                return 0
            return 1
        if cond_index >= len(conditions):
            if rule_index == len(rules):
                return 1
            return 0

        result = cache[cond_index * len(rules) + rule_index]
        if result is not None:
            return result

        result = 0
        condition = conditions[cond_index]
        rule = rules[rule_index]

        if condition != "#":
            result += count_from(cond_index +1 , rule_index)
        if condition != ".":
            if (
                cond_index + rule <= len(conditions)
                and "." not in conditions[cond_index : cond_index + rule]
                and (cond_index + rule == len(conditions) or conditions[cond_index + rule] != "#")
            ):
                result += count_from(cond_index + rule + 1, rule_index + 1)

        cache[cond_index * len(rules) + rule_index] = result
        return result

    return count_from(0, 0)

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