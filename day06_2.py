#!/usr/bin/env python3

from orbits import parse_orbital_map

if __name__ == '__main__':
    import os.path
    import pathlib
    BASE_DIR = pathlib.Path(os.path.dirname(__file__))

    with open(BASE_DIR / 'inputs' / 'day06.txt') as infile:
        m = parse_orbital_map(infile.read())
        print(m.count_orbital_transfers('YOU', 'SAN'))