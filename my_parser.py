from lexer import Lexer

class ASTNode:
    def __str__(self):
        return self.__repr__()

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'NumberNode({self.value})'

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'BooleanNode({self.value})'

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'IdentifierNode({self.name})'

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinaryOpNode({self.left}, {self.op}, {self.right})'

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'UnaryOpNode({self.op}, {self.operand})'

class LambdaNode(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        return f'LambdaNode(params={self.params}, body={self.body})'

class FunctionCallNode(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return f'FunctionCallNode({self.func}, {self.args})'

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f'FunctionDefNode(name={self.name}, params={self.params}, body={self.body})'

class IfElseNode(ASTNode):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def __repr__(self):
        return f'IfElseNode(condition={self.condition}, if_body={self.if_body}, else_body={self.else_body})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        return self.statement()

    def statement(self):
        if self.current_token() and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'def':
            return self.function_definition()
        return self.expression()

    def function_definition(self):
        self.eat('def')
        name = self.current_token()[1]
        self.eat('ID')
        self.eat('LPAREN')
        params = []
        if self.current_token() and self.current_token()[0] == 'ID':
            params.append(self.current_token()[1])
            self.eat('ID')
            while self.current_token() and self.current_token()[0] == 'DELIM':
                self.eat('DELIM')
                if self.current_token() and self.current_token()[0] == 'ID':
                    params.append(self.current_token()[1])
                    self.eat('ID')
                else:
                    raise Exception(f'Unexpected token: {self.current_token()}')
        self.eat('RPAREN')
        self.eat('COLON')
        body = self.expression()
        return FunctionDefNode(name=name, params=params, body=body)

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token()[0] in ('OP', 'COMPARE', 'LOGICAL'):
            token = self.current_token()
            self.eat(token[0])
            node = BinaryOpNode(left=node, op=token[1], right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'OP' and self.current_token()[1] in ('*', '/', '%'):
            token = self.current_token()
            self.eat('OP')
            node = BinaryOpNode(left=node, op=token[1], right=self.factor())
        return node

    def factor(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(value=token[1])
        elif token[0] == 'BOOLEAN':
            self.eat('BOOLEAN')
            return BooleanNode(value=token[1])
        elif token[0] == 'ID':
            self.eat('ID')
            if self.current_token() and self.current_token()[0] == 'LPAREN':
                return self.function_call(IdentifierNode(name=token[1]))
            return IdentifierNode(name=token[1])
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            if self.current_token() and self.current_token()[0] == 'LPAREN':
                return self.function_call(node)
            return node
        elif token[0] == 'NOT':
            self.eat('NOT')
            return UnaryOpNode(op='!', operand=self.factor())
        elif token[0] == 'KEYWORD' and token[1] == 'lambda':
            return self.lambda_expression()
        elif token[0] == 'KEYWORD' and token[1] == 'if':
            return self.if_else_expression()
        raise Exception(f'Unexpected token: {token}')

    def lambda_expression(self):
        self.eat('lambda')
        params = []
        if self.current_token() and self.current_token()[0] == 'ID':
            params.append(self.current_token()[1])
            self.eat('ID')
            while self.current_token() and self.current_token()[0] == 'DELIM':
                self.eat('DELIM')
                if self.current_token() and self.current_token()[0] == 'ID':
                    params.append(self.current_token()[1])
                    self.eat('ID')
                else:
                    raise Exception(f'Unexpected token: {self.current_token()}')
        self.eat('COLON')
        body = self.expression()
        return LambdaNode(params=params, body=body)

    def if_else_expression(self):
        self.eat('if')
        condition = self.expression()
        self.eat('COLON')
        if_body = self.expression()
        if self.current_token() and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'else':
            self.eat('KEYWORD')
            self.eat('COLON')
            else_body = self.expression()
        else:
            raise Exception(f'Expected else but got {self.current_token()}')
        return IfElseNode(condition=condition, if_body=if_body, else_body=else_body)

    def function_call(self, func):
        self.eat('LPAREN')
        args = []
        if self.current_token() and self.current_token()[0] != 'RPAREN':
            args.append(self.expression())
            while self.current_token() and self.current_token()[0] == 'DELIM':
                self.eat('DELIM')
                args.append(self.expression())
        self.eat('RPAREN')
        return FunctionCallNode(func=func, args=args)

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and (self.current_token()[0] == token_type or self.current_token()[1] == token_type):
            print(f"Eating token: {self.current_token()}")  # Debugging line
            self.current_token_index += 1
        else:
            raise Exception(f'Unexpected token: {self.current_token()}')
