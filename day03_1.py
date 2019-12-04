#!/usr/bin/env python3

import collections
import os.path
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(__file__))
PathComponent = collections.namedtuple('PathComponent', ['dir', 'dist'])
Coordinate = collections.namedtuple('Coordinate', ['x', 'y'])

def parse_component(component_str):
    return PathComponent(component_str[0], int(component_str[1:]))

def read_paths():
    with open(BASE_DIR / 'inputs' / 'day03.txt') as infile:
        line1 = next(infile)
        line2 = next(infile)
        return (
            list(map(parse_component, line1.split(','))),
            list(map(parse_component, line2.split(','))),
        )

def manhattan_dist(coord):
    return abs(coord.x) + abs(coord.y)

def trace_wire(path):
    start = Coordinate(0, 0)
    wire = [start]

    for comp in path:
        start = wire[-1]
        for d in range(comp.dist):
            if comp.dir == 'R':
                next_coord = Coordinate(start.x + d + 1, start.y)
            elif comp.dir == 'L':
                next_coord = Coordinate(start.x - d - 1, start.y)
            elif comp.dir == 'U':
                next_coord = Coordinate(start.x, start.y + d + 1)
            elif comp.dir == 'D':
                next_coord = Coordinate(start.x, start.y - d - 1)
            wire.append(next_coord)
    return wire

path1, path2 = read_paths()
wire1 = trace_wire(path1)
wire2 = trace_wire(path2)

intersections = set(wire1) & set(wire2)
closest = sorted(intersections, key=manhattan_dist)[1]
print(manhattan_dist(closest))
