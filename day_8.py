from enum import Enum
import itertools
from functools import partial, reduce


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


ALL_DIRECTIONS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class TreeMap:
    def __init__(self, input):
        self.__map = [[int(value) for value in line] for line in input]
        self.size = len(self.__map[0]), len(self.__map)
    
    def get_at_coords(self, x, y):
        return self.__map[y][x]
    
    def go_from(self, x, y, direction):
        dx, dy = self.__get_dx_dy(direction)
        while (coords := self.__go_one_step(x, y, dx, dy)) is not None:
            x, y = coords
            yield self.get_at_coords(*coords)
    
    def is_visible(self, coords):
        x, y = coords
        def is_visible_in_direction(direction):
            return all(val < self.get_at_coords(x, y) for val in self.go_from(x, y, direction))
        return any(is_visible_in_direction(dir) for dir in ALL_DIRECTIONS)
    
    def get_scenic_score(self, coords):
        scores = map(partial(self.__count_visible_trees_in_direction, *coords), ALL_DIRECTIONS)
        return reduce(lambda x, y: x * y, scores)
    
    def __count_visible_trees_in_direction(self, x, y, direction):
        result = 0
        for tree in self.go_from(x, y, direction):
            result += 1
            if tree >= self.get_at_coords(x, y):
                break
        return result
    
    def __go_one_step(self, x, y, dx, dy):
        width, height = self.size
        x += dx
        y += dy
        return (x, y) if x >= 0 and x < width and y >= 0 and y < height else None

    @staticmethod
    def __get_dx_dy(direction):
        return {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST: (-1, 0),
            Direction.WEST: (1, 0),
        }[direction]


def resolve_part1(input):
    treemap = TreeMap(input)
    width, height = treemap.size
    visible = filter(treemap.is_visible, itertools.product(range(width), range(height)))
    return len(list(visible))


def resolve_part2(input):
    treemap = TreeMap(input)
    width, height = treemap.size
    inner_xs = range(1, width - 1)
    inner_ys = range(1, height - 1)
    return max(map(treemap.get_scenic_score, itertools.product(inner_xs, inner_ys)))
