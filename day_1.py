import itertools


def convert_calories(input):
    def elve_calories():
        iterator = iter(input)
        while True:
            elve = [int(line) for line in itertools.takewhile(bool, iterator)]
            if elve:
                yield elve
            else:
                break
    return list(map(sum, elve_calories()))


def resolve_part1(input):
    return max(convert_calories(input))


def resolve_part2(input):
    return sum(sorted(convert_calories(input))[-3:])
