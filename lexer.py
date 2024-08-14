import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
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
            ('DELIM', r','),
            ('COLON', r':'),
            ('MISMATCH', r'.'),  # Any other character (for error handling)
        ]

        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line = self.source_code
        pos = 0
        mo = get_token(line)

        while mo is not None:
            typ = mo.lastgroup
            if typ == 'NUMBER':
                value = int(mo.group(typ))
            elif typ == 'BOOLEAN':
                value = mo.group(typ) == 'True'
            elif typ == 'SKIP' or typ == 'COMMENT':
                pos = mo.end()
                mo = get_token(line, pos)
                continue
            elif typ == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {mo.group(typ)} at position {pos} in line: {line.strip()}')
            else:
                value = mo.group(typ)
            self.tokens.append((typ, value))
            pos = mo.end()
            mo = get_token(line, pos)

        if pos != len(line):
            raise RuntimeError(f'Unexpected character {line[pos]} at position {pos}')
        return self.tokens

if __name__ == '__main__':
    lexer = Lexer("lambda x, y: (x + y) * 2 > 10 && x < y")
    print(lexer.tokenize())
