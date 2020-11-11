import re
from collections import defaultdict


class FiniteAutomata:
    # <editor-fold desc="Constructors">
    def __init__(self, Q: set, E: set, S: dict, Q0: str, F: set):
        FiniteAutomata._validate_params(Q, E, S, Q0, F)
        self.Q = Q
        self.E = E
        self.S = S
        self.Q0 = Q0
        self.F = F

    @classmethod
    def read_from_file(cls, filename: str):
        with open(filename, 'r') as infile:
            lines = infile.readlines()
            lines = [line.strip('\n') for line in lines]
            Q = set(lines[0].split(','))
            E = set(lines[1].split(','))
            transitions = [tr.split(',') for tr in lines[2].split('; ')]
            S = defaultdict(set)
            for tr in transitions:
                S[(tr[0], tr[1])].add(tr[2])
            Q0 = lines[3]
            F = set(lines[4].split(','))
            return cls(Q, E, S, Q0, F)

    # </editor-fold>

    @staticmethod
    def _validate_params(Q: set, E: set, S: dict, Q0: str, F: set):
        # Q, E, F and the keys of S are already guaranteed
        #     to be unique by using sets and dictionaries
        pattern = re.compile('^[A-Za-z0-9_-]+$')

        for elem in Q:
            assert pattern.match(elem), f'An element in Q is invalid: {elem}!'

        for elem in E:
            assert pattern.match(elem), f'An element in E is invalid: {elem}!'

        for key, value in S.items():
            assert key[0] in Q, f'A transition in S uses an invalid state: {key[0]}!'
            assert key[1] in E, f'A transition in S uses an invalid alphabet value: {key[1]}!'
            for state in value:
                assert state in Q, f'A transition in S uses an invalid state: {state}!'

        assert pattern.match(Q0), f'Q0 is invalid: {Q0}!'

        for elem in F:
            assert pattern.match(elem) and elem in Q, f'An element in F is invalid: {elem}!'

    # <editor-fold desc="Pretty Print Helper Functions">
    def _pretty_print_Q(self):
        str_Q = ', '.join(self.Q)
        return f'Q = {{ {str_Q} }}'

    def _pretty_print_E(self):
        str_E = ', '.join(self.E)
        return f'E = {{ {str_E} }}'

    def _pretty_print_S(self):
        temporary_str_S = []
        for key, value in self.S.items():
            temporary_str_S.append(f'\t({key[0]}, {key[1]}) -> {{ {", ".join(value)} }}')
        str_S = ',\n'.join(temporary_str_S)
        return f'S = {{\n' \
               f'{str_S}\n' \
               f'}}'

    def _pretty_print_Q0(self):
        return f'Q0 = {self.Q0}'

    def _pretty_print_F(self):
        str_F = ', '.join(self.F)
        return f'F = {{ {str_F} }}'

    def _pretty_print_sequence_accepted(self):
        sequence = input('Sequence = ')
        return self.sequence_accepted(sequence)

    def pretty_print(self, element: str):
        element_to_function = {
            'Q': self._pretty_print_Q,
            'E': self._pretty_print_E,
            'S': self._pretty_print_S,
            'Q0': self._pretty_print_Q0,
            'F': self._pretty_print_F,
            'T': self._pretty_print_sequence_accepted
            }
        return element_to_function[element]()

    # </editor-fold>

    def run_menu_once(self):
        menu = 'Enter Q to see the set of states\n' \
               'Enter E to see the alphabet\n' \
               'Enter S to see the set of transitions\n' \
               'Enter Q0 to see the initial state\n' \
               'Enter F to see the set of final states\n' \
               'Enter T to test a sequence\n' \
               'Enter X to exit\n' \
               '>'
        user_choice = input(menu).upper()
        if user_choice == 'X':
            return ''
        if user_choice not in ['Q', 'E', 'S', 'Q0', 'F', 'T']:
            return 'Invalid choice! Please choose one of the 4 given inputs!'
        else:
            return self.pretty_print(user_choice)

    def sequence_accepted(self, sequence: str) -> bool or str:
        for transition in self.S.values():
            if len(transition) != 1:
                # The given Finite Automata is not deterministic
                return "The automata is not deterministic"

        sequence = list(sequence)

        # We start from the initial state
        current_state = self.Q0

        while sequence:
            # We put the symbol that transitions us to the next state in transition_symbol
            transition_symbol, *sequence = sequence

            if transition_symbol not in self.E:
                # The transition symbol is not part of the alphabet
                return False

            if (current_state, transition_symbol) not in self.S.keys():
                # There is no transition starting from the current state and using the transition symbol
                return False

            current_state = tuple(self.S[(current_state, transition_symbol)])[0]

        if current_state not in self.F:
            # The state the sequence ended on is not a final state
            return False

        # If none of the other return statements were hit, the sequence is accepted by our FA
        return True

    # <editor-fold desc="To String">
    def __str__(self):

        return f'{self.pretty_print("Q")}\n' \
               f'{self.pretty_print("E")}\n' \
               f'{self.pretty_print("S")}\n' \
               f'{self.pretty_print("Q0")}\n' \
               f'{self.pretty_print("F")}'

    __repr__ = __str__
    # </editor-fold>
