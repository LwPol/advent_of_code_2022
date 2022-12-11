from dataclasses import dataclass


def parse_moves(input):
    def parse_line(line):
        move, amount = line.split(' ')
        return move, int(amount)
    return [parse_line(line) for line in input]


@dataclass
class Point:
    x: int
    y: int


class MoveSimulator:
    def __init__(self, fragments_no):
        self.__fragments = [Point(0, 0) for _ in range(fragments_no)]
        self.__visited = {(0, 0)}
    
    def simulate_move(self, move):
        direction, distance = move
        for _ in range(distance):
            self.__make_single_move(direction)
    
    def get_visited_spots_count(self):
        return len(self.__visited)
    
    def __make_single_move(self, direction):
        if direction == 'U':
            self.__make_vertical_move(1)
        elif direction == 'D':
            self.__make_vertical_move(-1)
        elif direction == 'R':
            self.__make_horizontal_move(1)
        else:
            self.__make_horizontal_move(-1)
        self.__align_all_other_fragments_with_head()
        self.__visited.add((self.__fragments[-1].x, self.__fragments[-1].y))
    
    def __make_vertical_move(self, amount):
        self.__fragments[0].y += amount
    
    def __make_horizontal_move(self, amount):
        self.__fragments[0].x += amount
    
    def __align_all_other_fragments_with_head(self):
        for head, tail in zip(self.__fragments, self.__fragments[1:]):
            if not self.__align_tail_with_head(head, tail):
                break
    
    @staticmethod
    def __align_tail_with_head(head: Point, tail: Point):
        if MoveSimulator.__is_tail_aligned_with_head(head, tail):
            return False
        if head.x == tail.x:
            dy = head.y - tail.y
            tail.y += dy // 2
        elif head.y == tail.y:
            dx = head.x - tail.x
            tail.x += dx // 2
        else:
            dx = head.x - tail.x
            dy = head.y - tail.y
            tail.x += dx // abs(dx)
            tail.y += dy // abs(dy)
        return True

    @staticmethod
    def __is_tail_aligned_with_head(head: Point, tail: Point):
        return max(abs(head.x - tail.x), abs(head.y - tail.y)) <= 1


def run_whole_simulation(simulator: MoveSimulator, input):
    for move in parse_moves(input):
        simulator.simulate_move(move)
    return simulator.get_visited_spots_count()


def resolve_part1(input):
    return run_whole_simulation(MoveSimulator(fragments_no=2), input)


def resolve_part2(input):
    return run_whole_simulation(MoveSimulator(fragments_no=10), input)
