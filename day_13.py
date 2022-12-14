import itertools


def parse_packet_pairs(input):
    def packet_lines():
        idx = 0
        while idx < len(input):
            yield input[idx], input[idx + 1]
            idx += 3
    return (tuple(eval(line) for line in pair) for pair in packet_lines())


def compare_integers(lhs, rhs):
    if lhs < rhs:
        return -1
    if lhs == rhs:
        return 0
    return 1


def compare_lists(lhs, rhs):
    for l, r in zip(lhs, rhs):
        comparison = compare(l, r)
        if comparison < 0:
            return -1
        if comparison > 0:
            return 1
    return compare_integers(len(lhs), len(rhs))


def compare(lhs, rhs):
    if isinstance(lhs, int) and isinstance(rhs, int):
        return compare_integers(lhs, rhs)
    elif isinstance(lhs, list) and isinstance(rhs, list):
        return compare_lists(lhs, rhs)
    if isinstance(lhs, int):
        return compare_lists([lhs], rhs)
    return compare_lists(lhs, [rhs])


def is_in_right_order(lhs, rhs):
    return compare(lhs, rhs) < 0


DIVIDER_PACKETS = ([[2]], [[6]])


class PacketWrapper:
    def __init__(self, packet):
        self.packet = packet
    
    def __lt__(self, other: "PacketWrapper"):
        return compare(self.packet, other.packet) < 0


def find_divider_packets_positions(packets):
    return [idx for idx, packet in enumerate(packets, start=1) if packet in DIVIDER_PACKETS]


def resolve_part1(input):
    indexed_pairs = enumerate(parse_packet_pairs(input), start=1)
    return sum(idx for idx, pair in indexed_pairs if is_in_right_order(*pair))


def resolve_part2(input):
    flat_packets = itertools.chain.from_iterable(parse_packet_pairs(input))
    ordered = sorted(itertools.chain(flat_packets, DIVIDER_PACKETS), key=PacketWrapper)
    first, second = find_divider_packets_positions(ordered)
    return first * second
