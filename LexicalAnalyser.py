import re

from FiniteAutomata import FiniteAutomata
from SymbolTable import SymbolTable


class LexicalAnalyser:
    def __init__(self):
        self.__tokens = []
        with open('token.in', 'r') as token_file:
            for line in token_file:
                self.__tokens.append(line.rstrip('\r\n'))

        self.__ST = SymbolTable()
        self.__PIF = []
        self.__lexical_errors = []

    # <editor-fold desc="Getters and setters">
    @property
    def tokens(self) -> list:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: list):
        self.__tokens = value

    @property
    def ST(self) -> SymbolTable:
        return self.__ST

    @ST.setter
    def ST(self, value: SymbolTable):
        self.__ST = value

    @property
    def PIF(self) -> list:
        return self.__PIF

    @PIF.setter
    def PIF(self, value: list):
        self.__PIF = value

    @property
    def lexical_errors(self) -> list:
        return self.__lexical_errors

    @lexical_errors.setter
    def lexical_errors(self, value: list):
        self.__lexical_errors = value

    # </editor-fold>

    def gen_PIF(self, token: str, index: int = 0):
        token = token \
            .lstrip('"') \
            .lstrip("'") \
            .rstrip('"') \
            .lstrip('"')
        self.__PIF.append((token, index))

    def raise_lexical_error(self, error_text: str):
        self.__lexical_errors.append(error_text)

    def output_files(self, filename: str):
        with open(filename + ' PIF.out', 'w') as pif_file:
            pif_file.write('\n'.join([f'"{token}": {index}' for token, index in self.__PIF]))

        with open(filename + ' ST.out', 'w') as st_file:
            st_file.write('The SymbolTable is implemented on a hashtable.\n')
            st_file.write('\n'.join(
                    [f'"{key}": {value}' for key, value in self.__ST.symbol_to_value.items()]))

        if not self.__lexical_errors:
            print(f'{filename} is lexically correct!')
        else:
            print(f'{filename} has lexical errors:\n\t' +
                  '\n\t'.join(self.__lexical_errors))

    def parse(self, filename: str):
        in_string = False
        string_delimiter = ''
        string_literal = ''
        identifier_FA = FiniteAutomata.read_from_file('identifier_FA.in')
        numeric_constant_FA = FiniteAutomata.read_from_file('numeric_constant_FA.in')

        with open(filename, 'r') as program_file:
            for line_index, line in enumerate(program_file):
                # We strip CR (\r) characters, so newlines are only delimited by LN (\n)
                line.replace('\r', '')

                # Split the line by separators
                split_line = re.split('([ \t\n()\\[\\]{},;#\'\"])', line)

                # Remove the empty strings from the list
                split_line = list(filter(None, split_line))
                for token in split_line:
                    # If it's a newline, we check if we're not in a string and ignore it
                    if token == '\n':
                        if in_string:
                            self.raise_lexical_error(
                                    f'Lexical error on line {line_index + 1}: Unexpected line end while parsing string!')
                            in_string = False
                        else:
                            pass
                    # Else we are in a string and haven't just finished it
                    elif in_string and token != string_delimiter:
                        string_literal += token

                    # Else if it's a '#', the rest of the line is a comment and we don't parse it
                    elif token == '#':
                        break

                    # Else if it's a single or double quote, we entered or left a string
                    elif token in ['\'', '\"']:
                        # If we weren't in a string before, we just started one
                        if not in_string:
                            string_literal = token
                            string_delimiter = token
                            in_string = True

                        # Else if we were in a string before, we just finished it
                        elif token == string_delimiter:
                            string_literal += token
                            index = self.__ST.add_symbol(string_literal)
                            self.gen_PIF('const', index)
                            in_string = False

                        # Else it's the other delimiter (so we add it to the string normally)
                        else:
                            string_literal += token

                    # Else if it's whitespace, ignore it
                    elif token in [' ', '\t']:
                        pass

                    # Else if it's part of the tokens list, we add it to the PIF with index 0
                    #     (because it's a reserved word, operator or separator)
                    elif token in self.__tokens:
                        self.gen_PIF(token, 0)

                    # Else if it's a numerical constant
                    elif numeric_constant_FA.sequence_accepted(token) is True:
                        index = self.__ST.add_symbol(token)
                        self.gen_PIF('const', index)

                    # Else if it's an identifier
                    elif identifier_FA.sequence_accepted(token) is True:
                        index = self.__ST.add_symbol(token)
                        self.gen_PIF('identifier', index)

                    # Otherwise, it's a lexical error so we print it
                    else:
                        self.raise_lexical_error(
                                f'Lexical error on line {line_index + 1}: Unexpected token {repr(token)}')

    def __str__(self):
        tokens = ', '.join(self.__tokens)
        pif = '\n\t\t'.join([f'"{token}": {index}' for token, index in self.__PIF])
        if self.__lexical_errors:
            lexical_errors = f'\tLexicalErrors{{\n' \
                             f'\t\t' + \
                             '\n\t\t'.join(self.__lexical_errors) + \
                             f'\n' \
                             f'\t\t}}\n'
        else:
            lexical_errors = ''
        return f'LexicalAnalyser{{\n' \
               f'\tTokens{{\n' \
               f'\t\t{tokens}\n' \
               f'\t\t}}\n' \
               f'\t{self.__ST}\n' \
               f'\tPIF{{\n' \
               f'\t\t{pif}\n' \
               f'\t\t}}\n' \
               f'{lexical_errors}' \
               f'}}'
