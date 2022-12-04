def parse_section_assignment(str_assignment):
    begin, end = str_assignment.split('-')
    return int(begin), int(end)


def parse_pairs(input):
    def parse_pair(line):
        return tuple(map(parse_section_assignment, line.split(',')))
    return [parse_pair(line) for line in input]


def is_assignment_contained_in_other(assignment, other):
    return assignment[0] >= other[0] and assignment[1] <= other[1]


def are_assignments_overlapping(lhs, rhs):
    x, y = sorted((lhs, rhs), key=lambda assignment: assignment[0])
    return y[0] <= x[1]


def resolve_part1(input):
    def is_one_contained_in_other(lhs, rhs):
        return is_assignment_contained_in_other(lhs, rhs) or \
               is_assignment_contained_in_other(rhs, lhs)
    return sum(1 for lhs, rhs in parse_pairs(input) if is_one_contained_in_other(lhs, rhs))


def resolve_part2(input):
    return sum(1 for lhs, rhs in parse_pairs(input) if are_assignments_overlapping(lhs, rhs))
