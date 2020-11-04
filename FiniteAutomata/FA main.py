from FiniteAutomata import FiniteAutomata

if __name__ == '__main__':
    FA = FiniteAutomata.read_from_file('FA.in')
    print(FA.sequence_accepted('0'))
    print(FA.sequence_accepted('01'))
    print(FA.sequence_accepted('01110'))
    print(FA.sequence_accepted('111100'))
    print(FA.sequence_accepted('011000101110'))
    while (res := FA.run_menu_once()) != '':
        print(res, '\n')
