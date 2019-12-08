import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from intcode import (
    parse_program,
    read_program,
    Computer
)

def test_equal_to_8_pos_mode():
    program = parse_program('3,9,8,9,10,9,4,9,99,-1,8')
    c = Computer(program)
    c.push_input(8)
    c.execute()
    assert c.pop_output() == 1

def test_not_equal_to_8_pos_mode():
    program = parse_program('3,9,8,9,10,9,4,9,99,-1,8')
    c = Computer(program)
    c.push_input(7)
    c.execute()
    assert c.pop_output() == 0

def test_less_than_8_pos_mode():
    program = parse_program('3,9,7,9,10,9,4,9,99,-1,8')
    c = Computer(program)
    c.push_input(7)
    c.execute()
    assert c.pop_output() == 1

def test_not_less_than_8_pos_mode():
    program = parse_program('3,9,7,9,10,9,4,9,99,-1,8')
    c = Computer(program)
    c.push_input(8)
    c.execute()
    assert c.pop_output() == 0

def test_equal_to_8_immediate_mode():
    program = parse_program('3,3,1108,-1,8,3,4,3,99')
    c = Computer(program)
    c.push_input(8)
    c.execute()
    assert c.pop_output() == 1

def test_not_equal_to_8_immediate_mode():
    program = parse_program('3,3,1108,-1,8,3,4,3,99')
    c = Computer(program)
    c.push_input(7)
    c.execute()
    assert c.pop_output() == 0

def test_less_than_8_immediate_mode():
    program = parse_program('3,3,1107,-1,8,3,4,3,99')
    c = Computer(program)
    c.push_input(7)
    c.execute()
    assert c.pop_output() == 1

def test_not_less_than_8_immediate_mode():
    program = parse_program('3,3,1107,-1,8,3,4,3,99')
    c = Computer(program)
    c.push_input(8)
    c.execute()
    assert c.pop_output() == 0

def test_jump_in_pos_mode():
    program = parse_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9')
    c = Computer(program)
    c.push_input(0)
    c.execute()
    assert c.pop_output() == 0

    program = parse_program('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9')
    c = Computer(program)
    c.push_input(80)
    c.execute()
    assert c.pop_output() == 1

def test_jump_in_immediate_mode():
    program = parse_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')
    c = Computer(program)
    c.push_input(0)
    c.execute()
    assert c.pop_output() == 0

    program = parse_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')
    c = Computer(program)
    c.push_input(80)
    c.execute()
    assert c.pop_output() == 1

def test_large_input():
    program = parse_program('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')
    c = Computer(program)
    c.push_input(6)
    c.execute()
    assert c.pop_output() == 999

    program = parse_program('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')
    c = Computer(program)
    c.push_input(8)
    c.execute()
    assert c.pop_output() == 1000

    program = parse_program('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')
    c = Computer(program)
    c.push_input(10)
    c.execute()
    assert c.pop_output() == 1001