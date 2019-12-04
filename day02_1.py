#!/usr/bin/env python3

import os.path
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(__file__))

def read_program():
    with open(BASE_DIR / 'inputs' / 'day02.txt') as infile:
        input = next(infile)
        return list(map(int, input.split(',')))

ADD = 1
MUL = 2
HALT = 99

class Computer:
    def __init__(self, program):
        self.program = program

    def execute(self):
        program = self.program[:]
        address = 0

        while program[address] != HALT:
            address1, address2, address3 = program[address + 1:address + 4]

            if program[address] == ADD:
                program[address3] = program[address1] + program[address2]

            elif program[address] == MUL:
                program[address3] = program[address1] * program[address2]

            address += 4
        return program

program = read_program()
program1202 = [program[0],12,2] + program[3:]
output = Computer(program1202).execute()
print(output[0])
