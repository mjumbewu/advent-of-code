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

operator_labels = {
    OP_ADD: 'ADD',
    OP_MULTIPLY: 'MULTIPLY',
    OP_SAVE_INPUT: 'SAVE_INPUT',
    OP_PRINT_OUTPUT: 'PRINT_OUTPUT',
    OP_JUMP_IF_TRUE: 'JUMP_IF_TRUE',
    OP_JUMP_IF_FALSE: 'JUMP_IF_FALSE',
    OP_LESS_THAN: 'LESS_THAN',
    OP_EQUALS: 'EQUALS',
    OP_HALT: 'HALT',
}

class Computer:
    def __init__(self, program):
        self.state = program
        self.address = 0
        self.is_halted = False

        self.input_queue = []
        self.output_queue = []

    def __str__(self):
        strs = tuple(f'\033[1m{st}\033[0m' if idx == self.address else str(st)
                     for idx, st in enumerate(self.state))
        return '[' + ','.join(strs) + ']'


    def execute(self, yield_on_output=False, debug=False):
        if self.is_halted:
            raise Exception('Computer is already halted.')

        while not self.is_halted:
            addr = self.address
            instruction = self.state[addr]
            op = instruction % 100
            modes = instruction // 100

            if debug:
                print(f'\nAddr: {addr}\nOperator: {operator_labels[op]}\nModes: {modes}\nState: {self}')
                import pdb; pdb.set_trace()

            if op == OP_HALT:
                self.is_halted = True

            elif op == OP_ADD:
                arg1, arg2, arg3 = self.state[addr + 1:addr + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg3] = self.get_val(arg1, mode1) + self.get_val(arg2, mode2)
                self.address += 4

            elif op == OP_MULTIPLY:
                arg1, arg2, arg3 = self.state[addr + 1:addr + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg3] = self.get_val(arg1, mode1) * self.get_val(arg2, mode2)
                self.address += 4

            elif op == OP_SAVE_INPUT:
                arg1 = self.state[addr + 1]
                mode1, = parse_modes(modes, 1)

                if mode1 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                self.state[arg1] = self.pop_input(debug=debug)
                self.address += 2

            elif op == OP_PRINT_OUTPUT:
                arg1 = self.state[addr + 1]
                mode1, = parse_modes(modes, 1)
                self.push_output(self.get_val(arg1, mode1), debug=debug)
                self.address += 2

                if yield_on_output:
                    break

            elif op == OP_JUMP_IF_TRUE:
                arg1, arg2 = self.state[addr + 1:addr + 3]
                mode1, mode2 = parse_modes(modes, 2)
                if self.get_val(arg1, mode1) != 0:
                    self.address = self.get_val(arg2, mode2)
                else:
                    self.address += 3

            elif op == OP_JUMP_IF_FALSE:
                arg1, arg2 = self.state[addr + 1:addr + 3]
                mode1, mode2 = parse_modes(modes, 2)
                if self.get_val(arg1, mode1) == 0:
                    self.address = self.get_val(arg2, mode2)
                else:
                    self.address += 3

            elif op == OP_LESS_THAN:
                arg1, arg2, arg3 = self.state[addr + 1:addr + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                val1 = self.get_val(arg1, mode1)
                val2 = self.get_val(arg2, mode2)
                self.state[arg3] = 1 if val1 < val2 else 0
                self.address += 4

            elif op == OP_EQUALS:
                arg1, arg2, arg3 = self.state[addr + 1:addr + 4]
                mode1, mode2, mode3 = parse_modes(modes, 3)

                if mode3 == MODE_IMM:
                    raise ValueError('Cannot use immediate mode for outputs.')

                val1 = self.get_val(arg1, mode1)
                val2 = self.get_val(arg2, mode2)
                self.state[arg3] = 1 if val1 == val2 else 0
                self.address += 4

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

    def push_input(self, val, debug=False):
        self.input_queue.append(val)

    def pop_input(self, debug=False):
        if not self.input_queue:
            return int(input('Input queue is empty; please provide a value: '))
        val = self.input_queue.pop(0)
        if debug:
            print(f'\nInput value is {val!r}')
        return val

    def push_output(self, val, debug=False):
        if debug:
            print(f'\nOutput value is {val!r}')
        self.output_queue.append(val)

    def pop_output(self, debug=False):
        return self.output_queue.pop(0)
