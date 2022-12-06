import itertools
from collections import defaultdict
import re


PROCEDURE_REGEX = re.compile(r'move (\d+) from (\d+) to (\d+)')


def yield_crates(line):
    def crate_or_none(char):
        return char if char.isalpha() else None
    return map(crate_or_none, itertools.compress(line, itertools.cycle([0, 1, 0, 0])))


def parse_stacks(iterator):
    stacks = defaultdict(list)
    def process_line(line):
        for idx, crate in enumerate(yield_crates(line), start=1):
            if crate is not None:
                stacks[idx].append(crate)
    for line in itertools.takewhile(bool, iterator):
        process_line(line)
    for stack in stacks.values():
        stack.reverse()
    return stacks


def parse_procedure(iterator):
    def parse_line(line):
        return tuple(map(int, PROCEDURE_REGEX.match(line).groups()))
    return [parse_line(line) for line in iterator]


def parse_input(input):
    it = iter(input)
    stacks = parse_stacks(it)
    procedure = parse_procedure(it)
    return stacks, procedure


def execute_procedure_step(stacks, step, is_9001_model):
    amount = step[0]
    from_stack, to_stack = (stacks[idx] for idx in (step[1], step[2]))
    crates_to_move = from_stack[-amount:]
    del from_stack[-amount:]
    if not is_9001_model:
        crates_to_move.reverse()
    to_stack.extend(crates_to_move)


def execute_procedure(stacks, procedure, model_no):
    for step in procedure:
        execute_procedure_step(stacks, step, model_no == 9001)


def collect_top_crates(stacks):
    return ''.join(stack[-1] for _, stack in sorted(stacks.items(), key=lambda x: x[0]))


def resolve_part1(input):
    stacks, procedure = parse_input(input)
    execute_procedure(stacks, procedure, model_no=9000)
    return collect_top_crates(stacks)


def resolve_part2(input):
    stacks, procedure = parse_input(input)
    execute_procedure(stacks, procedure, model_no=9001)
    return collect_top_crates(stacks)

