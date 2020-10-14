from collections import OrderedDict

from MyString import MyString


class SymbolTable:
    def __init__(self):
        self.symbol_to_value = OrderedDict()
        self.value_reached = 1

    def search_symbol(self, symbol: str) -> int:
        """
        Searches the symbol in the symbol table and returns the numeric value
        Returns -1 if the value is not found
        Complexity: O(1)
        """
        symbol = MyString(symbol)
        # Searching for the symbol in a dictionary is an O(1) operation
        if symbol in self.symbol_to_value:
            # The symbol already exists in the symbol table, we return its previous value
            return self.symbol_to_value[symbol]
        return -1

    def add_symbol(self, symbol: str) -> int:
        """
        Adds the symbol in the symbol table and returns the numeric value
        Complexity: O(1)
        """
        symbol = MyString(symbol)
        if self.search_symbol(symbol.value) != -1:
            return self.search_symbol(symbol.value)

        # The symbol doesn't exist, so we add it to the dict
        # and increment the value_reached (for the next symbol to be added)
        self.symbol_to_value[symbol] = self.value_reached
        self.value_reached += 1

        # Return the value reached minus 1 because it was previously incremented
        return self.value_reached - 1