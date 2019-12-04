#!/usr/bin/env python3

import os.path
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(__file__))

def fuel_req(mass):
    return mass // 3 - 2

def read_masses():
    with open(BASE_DIR / 'inputs' / 'day01.txt') as infile:
        return list(map(int, infile))

print(sum(fuel_req(mass) for mass in read_masses()))
