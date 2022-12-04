from enum import IntEnum


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def get_winning_shape(self):
        if self == Shape.ROCK:
            return Shape.PAPER
        if self == Shape.PAPER:
            return Shape.SCISSORS
        return Shape.ROCK
    
    def get_losing_shape(self):
        left = {Shape.ROCK, Shape.PAPER, Shape.SCISSORS} - {self, self.get_winning_shape()}
        return next(iter(left))


def parse_rounds(input):
    figure_mapping = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
    def parse_line(line):
        opponent, _, second = line
        return figure_mapping[opponent], second
    return map(parse_line, input)


def score(round):
    opponent, me = round
    def score_result():
        if opponent.get_winning_shape() == me:
            return 6
        if opponent == me:
            return 3
        return 0
    return me + score_result()


def resolve_part1(input):
    xyz_mapping = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}
    rounds = ((opponent, xyz_mapping[second]) for opponent, second in parse_rounds(input))
    return sum(map(score, rounds))


def resolve_part2(input):
    def resolve_xyz(opponent, xyz):
        if xyz == 'X':
            return opponent.get_losing_shape()
        if xyz == 'Y':
            return opponent
        return opponent.get_winning_shape()
    rounds = ((opponent, resolve_xyz(opponent, second)) for opponent, second in parse_rounds(input))
    return sum(map(score, rounds))
