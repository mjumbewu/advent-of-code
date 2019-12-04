#!/usr/bin/env python3

import os.path
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(__file__))

def fuel_req(mass):
    fuel_mass = max(mass // 3 - 2, 0)
    return fuel_mass + (fuel_req(fuel_mass) if fuel_mass > 0 else 0)

def read_masses():
    with open(BASE_DIR / 'inputs' / 'day01.txt') as infile:
        return list(map(int, infile))

print(sum(fuel_req(mass) for mass in read_masses()))
