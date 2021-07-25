import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class TuringMachine:
    states: set[str]
    symbols: set[str]
    blank_symbol: str
    input_symbols: set[str]
    initial_state: str
    accepting_states: set[str]
    transitions: dict[tuple[str, str], tuple[str, str, int]]
    # state, symbol -> new state, new symbol, direction

    head: int = field(init=False)
    tape: defaultdict[int, str] = field(init=False)
    current_state: str = field(init=False)
    halted: bool = field(init=False, default=True)

    def initialize(self, input_symbols: dict[int, str]):
        self.head = 0
        self.halted = False
        self.current_state = self.initial_state
        self.tape = defaultdict(lambda: self.blank_symbol, input_symbols)

    def step(self):
        if self.halted:
            raise RuntimeError('Cannot step halted machine')

        try:
            state, symbol, direction = self.transitions[(self.current_state, self.tape[self.head])]
        except KeyError:
            self.halted = True
            return
        self.tape[self.head] = symbol
        self.current_state = state
        self.head += direction


    def accepted_input(self):
        if not self.halted:
            raise RuntimeError('Machine still running')
        return self.current_state in self.accepting_states

    def print(self, window=10):
        print('... ', end='')
        print(' '.join(self.tape[i] for i in range(self.head - window, self.head + window + 1)), end='')
        print(f' ... state={self.current_state}')
        print(f'{" " * (2 * window + 4)}^')


if __name__ == '__main__':
    tm = TuringMachine(states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q15', 'qf'},
                       symbols={'0', '1', 'T', 'F', '+', '#'},
                       blank_symbol='#',
                       input_symbols={'101+111'},
                       initial_state='q0',
                       accepting_states={'qf'},
                       transitions={
                           ('q0', '+'): ('q1', '+', 1),
                           ('q0', 'F'): ('q0', 'F', 1),
                           ('q0', 'T'): ('q0', 'T', 1),
                           ('q0', '0'): ('q0', '0', 1),
                           ('q0', '1'): ('q0', '1', 1),
                           ('q1', '#'): ('q2', '#', -1),
                           ('q1', '0'): ('q1', '0', 1),
                           ('q1', '1'): ('q1', '1', 1),
                           ('q2', '1'): ('q3', '#', 1),
                           ('q2', '0'): ('q15', '#', 1),
                           ('q2', '+'): ('q9', '#', 1),
                           ('q3', '+'): ('q4', '+', -1),
                           ('q3', '0'): ('q3', '0', -1),
                           ('q3', '1'): ('q3','1',-1),
                           ('q4', '#'): ('q0', '#', 1),
                           ('q4', '1'): ('q5', 'F', -1),
                           ('q4', '0'): ('q7', 'T', -1),
                           ('q4', 'T'): ('q4', 'T', -1),
                           ('q4', 'F'): ('q4', 'F', -1),
                           ('q5', '#'): ('q6', '1', -1),
                           ('q5', '1'): ('q5', '0', -1),
                           ('q5', '0'): ('q7', '1', -1),
                           ('q6', '#'): ('q0', '#', 1),
                           ('q7', '#'): ('q0', '#', 1),
                           ('q7', '0'): ('q7', '0', -1),
                           ('q7', '1'): ('q7', '1', -1),
                           ('q15', '+'): ('q8', '+', -1),
                           ('q15', '1'): ('q15', '1', -1),
                           ('q15', '0'): ('q15', '0', -1),
                           ('q8', '0'): ('q7', 'F', -1),
                           ('q8', '1'): ('q7', 'T', -1),
                           ('q8', '#'): ('q0', '#', 1),
                           ('q8', 'T'): ('q8', 'T', -1),
                           ('q8', 'F'): ('q8', 'F', -1),
                           ('q9', 'T'): ('q9', '1', -1),
                           ('q9', 'F'): ('q9', '0', -1),
                           ('q9', '#'): ('qf', '#', 1),
                       })
    tm.initialize(dict(enumerate("100 1110")))

    while not tm.halted:
        tm.print()
        tm.step()
        time.sleep(1)

    print(tm.accepted_input())