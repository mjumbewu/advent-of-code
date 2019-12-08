#!/usr/bin/env python3

from intcode import read_program, Computer

program = read_program('day02.txt')
program1202 = [program[0],51,21] + program[3:]
c = Computer(program1202).execute()
print(c.state[0])
