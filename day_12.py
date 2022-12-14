from typing import NamedTuple, Tuple
from functools import partial
import heapq


class Square(NamedTuple):
    elevation: str
    coords: Tuple[int, int]
    cost: int

    def __lt__(self, other: "Square"):
        return self.cost < other.cost


def generate_heightmap_points(heightmap):
    for y, row in enumerate(heightmap):
        for x, value in enumerate(row):
            yield (x, y), value


def find_starting_pos_coords(heightmap):
    return next(coords for coords, value
                in generate_heightmap_points(heightmap)
                if value == 'S')


def get_at_coords(heightmap, coords):
    x, y = coords
    return heightmap[y][x]


def get_elevation(heightmap, coords):
    raw = get_at_coords(heightmap, coords)
    if raw == 'S':
        return 'a'
    if raw == 'E':
        return 'z'
    return raw


def generate_path_continuations(heightmap, current_coords):
    current_elevation = get_elevation(heightmap, current_coords)
    def neighbours():
        x, y = current_coords
        row = heightmap[y]
        if x > 0:
            yield x - 1, y
        if x < len(row) - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < len(heightmap) - 1:
            yield x, y + 1
    def is_viable_continuation(neighbour):
        elevation = get_elevation(heightmap, neighbour)
        return ord(elevation) - ord(current_elevation) <= 1
    return filter(is_viable_continuation, neighbours())


def find_fewest_steps_count(heightmap, starting_point):
    visited_coords = set()
    nodes = [Square(get_at_coords(heightmap, starting_point), starting_point, 0)]
    while nodes and (current := heapq.heappop(nodes)).elevation != 'E':
        if current.coords in visited_coords:
            continue
        for next_square in generate_path_continuations(heightmap, current.coords):
            value = get_at_coords(heightmap, next_square)
            heapq.heappush(nodes, Square(value, next_square, current.cost + 1))
        visited_coords.add(current.coords)
    return current.cost if current.elevation == 'E' else None


def generate_lowest_positions(heightmap):
    return (coords for coords, elevation
            in generate_heightmap_points(heightmap)
            if elevation == 'S' or elevation == 'a')


def resolve_part1(input):
    starting_point = find_starting_pos_coords(input)
    return find_fewest_steps_count(input, starting_point)


def resolve_part2(input):
    shortest_paths = map(partial(find_fewest_steps_count, input),
                         generate_lowest_positions(input))
    return min(filter(lambda x: x is not None, shortest_paths))
