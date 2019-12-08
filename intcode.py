import os.path
import pathlib

BASE_DIR = pathlib.Path(os.path.dirname(__file__))

def read_program(name):
    with open(BASE_DIR / 'inputs' / name) as infile:
        input = next(infile)
        return parse_program(input)

def parse_program(input):
    return list(map(int, input.split(',')))

def parse_modes(modes, count):
    while count:
        mode = modes % 10
        yield mode
        modes //= 10
        count -= 1

OP_ADD = 1
OP_MULTIPLY = 2
OP_SAVE_INPUT = 3
OP_PRINT_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS_THAN = 7
OP_EQUALS = 8
OP_HALT = 99

MODE_POS = 0
MODE_IMM = 1

class Computer:
    def __init__(self, program):
        self.state = program

        self.input_queue = []
        self.output_queue = []

    def execute(self):
        address = 0

        while True:
            instruction = self.state[address]
            op = instruction % 100
            modes = instruction // 100

            if op == OP_HALT:
                break

            elif op == OP_ADD:
                arg1, arg2, arg3 = self.state[address + 1:address + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg3] = self.get_val(arg1, mode1) + self.get_val(arg2, mode2)
                address += 4

            elif op == OP_MULTIPLY:
                arg1, arg2, arg3 = self.state[address + 1:address + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg3] = self.get_val(arg1, mode1) * self.get_val(arg2, mode2)
                address += 4

            elif op == OP_SAVE_INPUT:
                arg1 = self.state[address + 1]
                mode1, = parse_modes(modes, 1)

                if mode1 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg1] = self.pop_input()
                address += 2

            elif op == OP_PRINT_OUTPUT:
                arg1 = self.state[address + 1]
                mode1, = parse_modes(modes, 1)
                self.push_output(self.get_val(arg1, mode1))
                address += 2

            elif op == OP_JUMP_IF_TRUE:
                arg1, arg2 = self.state[address + 1:address + 3]
                mode1, mode2 = parse_modes(modes, 2)
                if self.get_val(arg1, mode1) != 0:
                    address = self.get_val(arg2, mode2)
                else:
                    address += 3

            elif op == OP_JUMP_IF_FALSE:
                arg1, arg2 = self.state[address + 1:address + 3]
                mode1, mode2 = parse_modes(modes, 2)
                if self.get_val(arg1, mode1) == 0:
                    address = self.get_val(arg2, mode2)
                else:
                    address += 3

            elif op == OP_LESS_THAN:
                arg1, arg2, arg3 = self.state[address + 1:address + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                val1 = self.get_val(arg1, mode1)
                val2 = self.get_val(arg2, mode2)
                self.state[arg3] = 1 if val1 < val2 else 0
                address += 4

            elif op == OP_EQUALS:
                arg1, arg2, arg3 = self.state[address + 1:address + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                val1 = self.get_val(arg1, mode1)
                val2 = self.get_val(arg2, mode2)
                self.state[arg3] = 1 if val1 == val2 else 0
                address += 4

            else:
                raise ValueError(f'Invalid operation code: {op}; state: {self.state}')

        return self

    def get_val(self, arg, mode):
        if mode == MODE_POS:
            return self.state[arg]
        elif mode == MODE_IMM:
            return arg
        else:
            raise ValueError(f'Invalid mode: {mode}')

    def push_input(self, val):
        self.input_queue.append(val)

    def pop_input(self):
        if not self.input_queue:
            return int(input('Input queue is empty; please provide a value: '))
        return self.input_queue.pop(0)

    def push_output(self, val):
        self.output_queue.append(val)
        print(val)

    def pop_output(self):
        return self.output_queue.pop(0)
