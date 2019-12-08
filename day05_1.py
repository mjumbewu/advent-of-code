#!/usr/bin/env python3

from intcode import read_program, Computer

if __name__ == '__main__':
    program = read_program('day05.txt')
    c = Computer(program)
    c.push_input(1)
    c.execute()
