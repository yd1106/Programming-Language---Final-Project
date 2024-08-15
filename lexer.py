import re


class Lexer:
    def __init__(self, source_code):
        """
        Initialize the Lexer with the source code.

        :param source_code: The input string that contains the code to be tokenized.
        """
        self.source_code = source_code  # Store the source code
        self.tokens = []  # List to store the generated tokens
        self.current_position = 0  # Position in the source code

    def tokenize(self):
        """
        Tokenize the source code into a list of tokens.

        :return: A list of tokens where each token is represented as a tuple (token_type, token_value).
        """
        # Define the specifications for each token type using regular expressions
        token_specification = [
            ('NUMBER', r'\d+'),  # Integer numbers
            ('BOOLEAN', r'\b(True|False)\b'),  # Boolean values
            ('KEYWORD', r'\b(lambda|if|else|return|def)\b'),  # Keywords
            ('ID', r'[A-Za-z_]\w*'),  # Identifiers (names of variables or functions)
            ('OP', r'[+\-*/%]'),  # Arithmetic operators
            ('LPAREN', r'\('),  # Left parenthesis
            ('RPAREN', r'\)'),  # Right parenthesis
            ('COMPARE', r'==|!=|<=|>=|<|>'),  # Comparison operators
            ('LOGICAL', r'&&|\|\|'),  # Logical operators
            ('NOT', r'!'),  # Logical NOT operator
            ('NEWLINE', r'\n'),  # Newline characters
            ('SKIP', r'[ \t]+'),  # Spaces and tabs
            ('COMMENT', r'#.*'),  # Comments
            ('DELIM', r','),  # Comma delimiter
            ('COLON', r':'),  # Colon delimiter
            ('MISMATCH', r'.'),  # Any other character (for error handling)
        ]

        # Create a single regular expression that combines all token specifications
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        get_token = re.compile(tok_regex).match  # Compile the combined regex for matching tokens
        line = self.source_code  # The source code to be tokenized
        pos = 0  # Current position in the source code
        mo = get_token(line)  # Match the first token

        # Loop to find all tokens in the source code
        while mo is not None:
            typ = mo.lastgroup  # Get the type of the matched token
            if typ == 'NUMBER':
                value = int(mo.group(typ))  # Convert number token to an integer
            elif typ == 'BOOLEAN':
                value = mo.group(typ) == 'True'  # Convert boolean token to a boolean value
            elif typ == 'SKIP' or typ == 'COMMENT':
                # Skip spaces, tabs, and comments
                pos = mo.end()  # Move the position to the end of the matched token
                mo = get_token(line, pos)  # Match the next token
                continue
            elif typ == 'MISMATCH':
                # Raise an error for any unmatched characters
                raise RuntimeError(f'Unexpected character {mo.group(typ)} at position {pos} in line: {line.strip()}')
            else:
                value = mo.group(typ)  # Get the value of the matched token
            self.tokens.append((typ, value))  # Append the token to the tokens list
            pos = mo.end()  # Move the position to the end of the matched token
            mo = get_token(line, pos)  # Match the next token

        # If there are any remaining characters that couldn't be matched, raise an error
        if pos != len(line):
            raise RuntimeError(f'Unexpected character {line[pos]} at position {pos}')
        return self.tokens  # Return the list of tokens


if __name__ == '__main__':
    lexer = Lexer("lambda x, y: (x + y) * 2 > 10 && x < y")  # Create a Lexer instance with some example code
    print(lexer.tokenize())  # Tokenize the code and print the tokens
