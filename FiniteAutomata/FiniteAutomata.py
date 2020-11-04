import re


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
            S = {(tr[0], tr[1]): tr[2] for tr in transitions}
            Q0 = lines[3]
            F = set(lines[4].split(','))
            return cls(Q, E, S, Q0, F)

    # </editor-fold>

    @staticmethod
    def _validate_params(Q: set, E: set, S: dict, Q0: str, F: set):
        # Q, E, F and the keys of S are already guaranteed
        #     to be unique by using sets and dictionaries
        pattern = re.compile('^[A-Za-z0-9]+$')

        for elem in Q:
            assert pattern.match(elem), f'An element in Q is invalid: {elem}!'

        for elem in E:
            assert pattern.match(elem), f'An element in E is invalid: {elem}!'

        for key, value in S.items():
            assert key[0] in Q, f'A transition in S uses an invalid state: {key[0]}!'
            assert key[1] in E, f'A transition in S uses an invalid alphabet value: {key[1]}!'
            assert value in Q, f'A transition in S uses an invalid state: {value}!'

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
            temporary_str_S.append(f'\t({key[0]}, {key[1]}) -> {value}')
        str_S = ',\n'.join(temporary_str_S)
        return f'S = {{\n' \
               f'{str_S}\n' \
               f'}}'

    def _pretty_print_Q0(self):
        return f'Q0 = {self.Q0}'

    def _pretty_print_F(self):
        str_F = ', '.join(self.F)
        return f'F = {{ {str_F} }}'

    def pretty_print(self, element: str):
        element_to_function = {
            'Q': self._pretty_print_Q,
            'E': self._pretty_print_E,
            'S': self._pretty_print_S,
            'Q0': self._pretty_print_Q0,
            'F': self._pretty_print_F
            }
        return element_to_function[element]()

    # </editor-fold>

    def run_menu_once(self):
        menu = 'Enter Q to see the set of states\n' \
               'Enter E to see the alphabet\n' \
               'Enter S to see the set of transitions\n' \
               'Enter Q0 to see the initial state\n' \
               'Enter F to see the set of final states\n' \
               'Enter X to exit\n' \
               '>'
        user_choice = input(menu).upper()
        if user_choice == 'X':
            return ''
        if user_choice not in ['Q', 'E', 'S', 'Q0', 'F']:
            return 'Invalid choice! Please choose one of the 4 given inputs!'
        else:
            return self.pretty_print(user_choice)

    # <editor-fold desc="To String">
    def __str__(self):

        return f'{self.pretty_print("Q")}\n' \
               f'{self.pretty_print("E")}\n' \
               f'{self.pretty_print("S")}\n' \
               f'{self.pretty_print("Q0")}\n' \
               f'{self.pretty_print("F")}'

    __repr__ = __str__
    # </editor-fold>
