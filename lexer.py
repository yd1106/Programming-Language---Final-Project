import re


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        token_specification = [
            ('NUMBER', r'\d+'),  # Integer
            ('KEYWORD', r'\b(lambda|if|else|return)\b'),  # Keywords
            ('ID', r'[A-Za-z_]\w*'),  # Identifiers
            ('OP', r'[+\-*/%]'),  # Arithmetic operators
            ('LPAREN', r'\('),  # Left parenthesis
            ('RPAREN', r'\)'),  # Right parenthesis
            ('BOOLEAN', r'(True|False)'),  # Boolean values
            ('COMPARE', r'==|!=|<=|>=|<|>'),  # Comparison operators
            ('NEWLINE', r'\n'),  # Line endings
            ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
            ('DELIM', r'[,]'),  # Comma delimiter
            ('COLON', r':'),  # Colon delimiter
            ('LOGICAL', r'(&&|\|\|)'),  # Logical operators
            ('MISMATCH', r'.'),  # Any other character
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
            elif typ == 'ID' and mo.group(typ) in ('True', 'False'):
                typ = 'BOOLEAN'
                value = mo.group(typ) == 'True'
            elif typ == 'SKIP':
                pos = mo.end()
                mo = get_token(line, pos)
                continue
            elif typ == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {mo.group(typ)} at position {pos}')
            else:
                value = mo.group(typ)
            self.tokens.append((typ, value))
            pos = mo.end()
            mo = get_token(line, pos)

        if pos != len(line):
            raise RuntimeError(f'Unexpected character {line[pos]} at position {pos}')
        return self.tokens


if __name__ == '__main__':
    lexer = Lexer("lambda x, y: x + y == 8")
    print(lexer.tokenize())
