from collections import deque
import itertools


def parse_signal(input):
    return input[0]


def yield_characters_windows(signal, size):
    it = iter(signal)
    window = deque(maxlen=size)
    while len(window) < size - 1:
        window.append(next(it))
    for letter in it:
        window.append(letter)
        yield window


def find_marker(signal, window_size):
    def has_repeating_chars(item):
        return len(set(item[1])) < window_size
    indexed_windows = enumerate(yield_characters_windows(signal, window_size), start=window_size)
    return next(itertools.dropwhile(has_repeating_chars, indexed_windows))[0]


def resolve_part1(input):
    return find_marker(parse_signal(input), window_size=4)


def resolve_part2(input):
    return find_marker(parse_signal(input), window_size=14)
