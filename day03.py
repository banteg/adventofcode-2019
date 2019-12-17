from dataclasses import dataclass

import aoc

@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scale):
        assert isinstance(scale, int)
        return Point(self.x * scale, self.y * scale)


@dataclass
class Wire:
    a: Point
    b: Point

    def intersect(self, other):
        assert isinstance(other, Wire)
        if self.a.x == self.b.x and other.a.x <= self.a.x <= other.b.x and self.a.y <= other.a.y <= other.b.y:
            return Point(self.a.x, other.a.y)
        if self.a.y == self.b.y and other.a.y <= self.a.y <= other.b.y and self.a.x <= other.a.x <= self.b.x:
            return Point(other.a.x, self.a.y)


def manhattan_distance(point):
    return abs(point.x) + abs(point.y)


move = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}


@aoc.test({
    'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83': 159,
    'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7': 135,
})
def part_1(data: aoc.Data):
    wires = []
    for wire in data.splitlines():
        wires.append([])
        pos = Point()
        for segment in wire.split(','):
            direction = segment[0]
            length = int(segment[1:])
            delta = move[direction] * length
            wires[-1].append(Wire(pos, pos + delta))
            pos += delta

    intersections = set()
    for a in wires[0]:
        for b in wires[1]:
            if intersect := a.intersect(b):
                intersections.add(intersect)

    intersections.discard(Point())  # central port doesn't count
    closest = min(intersections, key=manhattan_distance)
    return manhattan_distance(closest)


@aoc.test({})
def part_2(data: aoc.Data):
    return
