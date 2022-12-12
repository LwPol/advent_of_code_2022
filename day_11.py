import re
from collections import defaultdict, deque, Counter
from typing import Dict, List, NamedTuple
import math
from functools import partial


MONKEY_ID = re.compile(r'Monkey (\d)+:')
STARTING_ITEMS = re.compile(r'\s*Starting items: (.+)')
OPERATION = re.compile(r'\s*Operation: new = (.+)')
TEST = re.compile(r'\s*Test: divisible by (\d+)')
IF_TRUE = re.compile(r'\s*If true: throw to monkey (\d+)')
IF_FALSE = re.compile(r'\s*If false: throw to monkey (\d+)')


class MonkeyParams(NamedTuple):
    monkey_id: int
    starting_items: List[int]
    operation: str
    modulo_test_value: int
    destination_for_true: int
    destination_for_false: int


def parse_monkey(lines):
    it = iter(lines)
    monkey_id = int(MONKEY_ID.match(next(it)).group(1))
    starting_items = map(int, STARTING_ITEMS.match(next(it)).group(1).split(', '))
    operation = OPERATION.match(next(it)).group(1)
    modulo = int(TEST.match(next(it)).group(1))
    destination_for_true = int(IF_TRUE.match(next(it)).group(1))
    destination_for_false = int(IF_FALSE.match(next(it)).group(1))
    return MonkeyParams(monkey_id, list(starting_items), operation, modulo,
                                   destination_for_true, destination_for_false)


def parse_monkeys(input):
    def group_monkey_repr():
        idx = 0
        while idx < len(input):
            yield input[idx:idx + 6]
            idx += 7
    return list(map(parse_monkey, group_monkey_repr()))


class Monkey:
    def __init__(self, items, operation, modulo, destinations, reductor):
        self.__items = deque(items)
        self.__operation = operation
        self.__modulo = modulo
        self.__destinations = destinations
        self.__worry_level_reductor = reductor
    
    def perform_turn(self):
        thrown_items = defaultdict(list)
        while self.__items:
            item = self.__items.popleft()
            worry_level = self.__worry_level_reductor(self.__operation(item))
            destination = self.__destinations[0] if worry_level % self.__modulo == 0\
                                                 else self.__destinations[1]
            thrown_items[destination].append(worry_level)
        return thrown_items
    
    def receive_items(self, items):
        self.__items.extend(items)


def parse_operation(operation_str):
    operator, arg2 = re.split(r' (\+|\*) ', operation_str)[1:]
    if arg2 == 'old':
        return (lambda old: 2 * old) if operator == '+' else lambda old: old ** 2
    arg2 = int(arg2)
    return (lambda old: old + arg2) if operator == '+' else lambda old: old * arg2


def monkey_generator(monkey_params: MonkeyParams):
    return partial(Monkey,
                   monkey_params.starting_items,
                   parse_operation(monkey_params.operation),
                   monkey_params.modulo_test_value,
                   (monkey_params.destination_for_true, monkey_params.destination_for_false))


def create_monkeys_for_part1(monkeys_params):
    def divide_by_3(value):
        return value // 3
    return {param.monkey_id: monkey_generator(param)(divide_by_3) for param in monkeys_params}


def create_monkeys_for_part2(monkeys_params):
    lcm = math.lcm(*(params.modulo_test_value for params in monkeys_params))
    def reduce_with_lcm(value):
        return value % lcm
    return {param.monkey_id: monkey_generator(param)(reduce_with_lcm) for param in monkeys_params}


def perform_round(monkeys: Dict[int, Monkey]):
    inspections = Counter()
    for idx, monkey in monkeys.items():
        thrown_items = monkey.perform_turn()
        for throw_to, items in thrown_items.items():
            inspections[idx] += len(items)
            monkeys[throw_to].receive_items(items)
    return inspections


def perform_rounds(monkeys, rounds):
    inspections = Counter()
    for _ in range(rounds):
        inspections.update(perform_round(monkeys))
    return inspections


def calculate_monkey_business(monkeys: List[Monkey], rounds):
    inspections = perform_rounds(monkeys, rounds)
    first, second = sorted(inspections.values())[-2:]
    return first * second


def resolve_part1(input):
    monkeys = create_monkeys_for_part1(parse_monkeys(input))
    return calculate_monkey_business(monkeys, rounds=20)


def resolve_part2(input):
    monkeys = create_monkeys_for_part2(parse_monkeys(input))
    return calculate_monkey_business(monkeys, rounds=10000)
