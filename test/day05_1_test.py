import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from intcode import (
    parse_program,
    read_program,
    Computer
)

def test_original_day02_program():
    program = read_program('day02.txt')
    program1202 = [program[0],12,2] + program[3:]
    c = Computer(program1202)
    c.execute()
    assert c.state[0] == 4714701

def test_inout_opcodes():
    program = parse_program('3,0,4,0,99')
    c = Computer(program)
    c.push_input(27)
    c.execute()
    output = c.pop_output()
    assert output == 27

def test_modes():
    program = parse_program('1002,4,3,4,33')
    c = Computer(program)
    c.execute()
    assert c.state == [1002, 4, 3, 4, 99]

def test_negatives():
    program = parse_program('1101,100,-1,4,0')
    c = Computer(program)
    c.execute()
    assert c.state == [1101, 100, -1, 4, 99]
