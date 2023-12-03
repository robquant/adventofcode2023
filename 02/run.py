import sys
import pathlib
from dataclasses import dataclass

@dataclass
class CubeSet:
    red: int
    green: int
    blue: int

    def __le__(self, other):
        return self.red <= other.red \
            and self.green <= other.green \
            and self.blue <= other.blue

    def power(self) -> int:
        return self.red * self.green * self.blue

@dataclass
class Game:
    id_number: int
    draws: list[CubeSet]
    cubes: CubeSet | None = None

def parse(line) -> Game:
    colon_pos = line.find(":")
    id_number = int(line[line.find(" "):colon_pos])
    games_str = line[colon_pos+1:].split(";")
    game = Game(id_number, draws=[])
    for game_str in games_str:
        red = green = blue = 0
        cubes = game_str.split(",")
        for cube_color in cubes:
            n, color = cube_color.strip().split()
            n = int(n)
            if color == "red":
                red = n
            elif color == "green":
                green = n
            elif color == "blue":
                blue = n
        draw = CubeSet(red, green, blue)
        game.draws.append(draw)
    return game


def part1(games: list[Game], cubes: CubeSet):
    s = 0
    for game in games:
        if all(draw <= cubes for draw in game.draws):
            s += game.id_number
    return s

def part2(games: list[Game]):
    s = 0
    for game in games:
        min_red = max(s.red for s in game.draws)
        min_green = max(s.green for s in game.draws)
        min_blue = max(s.blue for s in game.draws)
        s += CubeSet(min_red, min_green, min_blue).power()
    return s

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    lines = open(pathlib.Path(__file__).parent / "input").readlines()
    games = [parse(line) for line in lines]

    cubes = CubeSet(red=12, green=13, blue=14)
    print(part1(games, cubes))
    print(part2(games))


if __name__ == "__main__":
    main()