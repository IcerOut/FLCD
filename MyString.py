class MyString:
    HASH_NUMBER = 65536

    def __init__(self, value: str):
        self.value = value

    def __hash__(self):
        """
        We take the sum of the ascii_values of all characters in the string
        Then we return its value modulo 65536 (2^16) to cap its value
        """
        ascii_values = [ord(char) for char in self.value]
        return sum(ascii_values) % MyString.HASH_NUMBER

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    __repr__ = __str__