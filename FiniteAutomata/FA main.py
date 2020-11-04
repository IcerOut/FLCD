from FiniteAutomata import FiniteAutomata

if __name__ == '__main__':
    FA = FiniteAutomata.read_from_file('FA.in')
    while (res := FA.run_menu_once()) != '':
        print(res, '\n')
