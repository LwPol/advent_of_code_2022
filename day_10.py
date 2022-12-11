def execute(input):
    register = 1
    yield register
    for instruction in input:
        if instruction == 'noop':
            yield register
        else:
            arg = int(instruction.split(' ')[-1])
            yield register
            register += arg
            yield register


def register_signal_strength(program, cycles_for_collection):
    signal_strength_combined = 0
    next_cycle = cycles_for_collection.pop()
    for cycle, value in enumerate(execute(program), start=1):
        if cycle == next_cycle:
            signal_strength_combined += cycle * value
            if not cycles_for_collection:
                break
            next_cycle = cycles_for_collection.pop()
    return signal_strength_combined


def does_sprite_overlap_with_pixel(pixel_idx, sprite_pos):
    return abs(sprite_pos - pixel_idx % 40) <= 1


def draw_pixels(program):
    pixels = []
    for idx, sprite_position in zip(range(240), execute(program)):
        pixels.append('#' if does_sprite_overlap_with_pixel(idx, sprite_position) else ' ')
    return pixels


class PixelDisplay:
    def __init__(self, pixels):
        self.__pixels = pixels
    
    def __str__(self):
        return '\n' + '\n'.join(self.__group_rows())

    def __group_rows(self):
        current_beg = 0
        while current_beg < 240:
            yield ''.join(self.__pixels[current_beg:current_beg + 40])
            current_beg += 40


def resolve_part1(input):
    return register_signal_strength(input, [220, 180, 140, 100, 60, 20])


def resolve_part2(input):
    return PixelDisplay(draw_pixels(input))
