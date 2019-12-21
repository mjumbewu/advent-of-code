#!/usr/bin/env python3

from intcode import read_program
from amplifier import AmpSequence

if __name__ == '__main__':
    program = read_program('day07.txt')
    settings, signal = AmpSequence.find_max_feedback_loop_settings(program)
    print(signal)