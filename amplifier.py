from intcode import Computer
from itertools import cycle

class Amplifier (Computer):
    def __init__(self, program, phase_setting):
        super().__init__(program)
        self.push_input(phase_setting)

class AmpSequence:
    def __init__(self, program, phase_settings, feedback=False):
        self.amps = [Amplifier(program.copy(), s) for s in phase_settings]
        self.feedback = feedback

    def execute(self, yield_on_output=True, feedback=False, debug=False):
        amps = cycle(self.amps) if feedback else self.amps
        output = 0

        for idx, amp in enumerate(amps):
            if debug:
                print(f'\nExecuting amp {idx % 5}')
            amp.push_input(output)
            amp.execute(yield_on_output, debug=debug)

            if feedback and amp.is_halted:
                if debug:
                    print(f'\nHalted')
                break

            output = amp.pop_output()
        self.signal = output
        return self

    @classmethod
    def find_max_settings(cls, program, possible_phase_settings=None, feedback=False, debug=False):
        if possible_phase_settings is None:
            possible_phase_settings = range(5)

        maximal_settings = None
        max_signal = None

        for phase_settings in permutations(possible_phase_settings):
            amp_seq = cls(program, phase_settings).execute(feedback=feedback, debug=debug)
            if max_signal is None or max_signal < amp_seq.signal:
                maximal_settings = phase_settings
                max_signal = amp_seq.signal
        return maximal_settings, max_signal

    @classmethod
    def find_max_feedback_loop_settings(cls, program, debug=False):
        return cls.find_max_settings(program,
                                     possible_phase_settings=range(5, 10),
                                     feedback=True,
                                     debug=debug)

def permutations(values):
    values = list(values)
    if not values:
        yield []
    elif len(values) == 1:
        yield values
    else:
        for i in range(len(values)):
            first = values[i]
            for rest in permutations(values[:i] + values[i + 1:]):
                yield [first, *rest]
