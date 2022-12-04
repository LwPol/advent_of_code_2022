def parse_rucksacks(input):
    def parse_line(line):
        middle = len(line) // 2
        return line[:middle], line[middle:]
    return [parse_line(line) for line in input]


def parse_groups(input):
    def groups():
        it = iter(input)
        try:
            while True:
                yield [next(it), next(it), next(it)]
        except StopIteration:
            pass
    return list(groups())


def get_common_item(rucksack):
    return next(iter(set(rucksack[0]) & set(rucksack[1])))


def get_badge(rucksack_group):
    first, second, third = map(set, rucksack_group)
    return next(iter(first & second & third))


def score_item(item):
    return ord(item) - 96 if item.islower() else ord(item) - 38


def resolve_part1(input):
    return sum(score_item(get_common_item(rucksack)) for rucksack in parse_rucksacks(input))


def resolve_part2(input):
    return sum(score_item(get_badge(group)) for group in parse_groups(input))
