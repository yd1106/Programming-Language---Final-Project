from lexer import Lexer
from my_parser import *

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Error: Variable '{name}' not found")

    def set(self, name, value):
        self.variables[name] = value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.call_stack = []

    def evaluate(self, node, env=None):
        if env is None:
            env = self.global_env

        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            raise Exception(f"No method to evaluate node type {type(node).__name__}")
        return method(node, env)

    def eval_NumberNode(self, node, env):
        return node.value

    def eval_BooleanNode(self, node, env):
        return node.value

    def eval_IdentifierNode(self, node, env):
        return env.get(node.name)

    def eval_BinaryOpNode(self, node, env):
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)

        if node.op in ('+', '-', '*', '/', '%'):
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError(f"Unsupported operand type(s) for {node.op}: '{type(left).__name__}' and '{type(right).__name__}'")
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                return left // right
            elif node.op == '%':
                return left % right

        elif node.op in ('&&', '||'):
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise TypeError(f"Unsupported operand type(s) for {node.op}: '{type(left).__name__}' and '{type(right).__name__}'")
            if node.op == '&&':
                return left and right
            elif node.op == '||':
                return left or right

        elif node.op in ('==', '!=', '<', '>', '<=', '>='):
            if type(left) != type(right):
                raise TypeError(f"Cannot compare different types: '{type(left).__name__}' and '{type(right).__name__}'")
            if node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '>':
                return left > right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>=':
                return left >= right

        else:
            raise Exception(f"Error: Unsupported binary operator: '{node.op}'")

    def eval_UnaryOpNode(self, node, env):
        operand = self.evaluate(node.operand, env)
        if node.op == '!':
            if not isinstance(operand, bool):
                raise TypeError(f"Unsupported operand type for {node.op}: '{type(operand).__name__}'")
            return not operand
        else:
            raise Exception(f"Error: Unsupported unary operator: '{node.op}'")

    def eval_LambdaNode(self, node, env):
        def lambda_func(*args):
            if len(args) != len(node.params):
                raise Exception(f"Error: Lambda expected {len(node.params)} arguments but got {len(args)}.")
            new_env = Environment(parent=env)
            for param, arg in zip(node.params, args):
                new_env.set(param, arg)
            return self.evaluate(node.body, new_env)
        return lambda_func

    def eval_FunctionCallNode(self, node, env):
        func = self.evaluate(node.func, env)
        if not callable(func):
            raise Exception(f"Error: Attempt to call a non-function value '{func}'.")
        args = [self.evaluate(arg, env) for arg in node.args]
        return func(*args)

    def eval_FunctionDefNode(self, node, env):
        def function(*args):
            if len(args) != len(node.params):
                raise Exception(f"Error: Function '{node.name}' expected {len(node.params)} arguments but got {len(args)}.")
            new_env = Environment(parent=env)
            for param, arg in zip(node.params, args):
                new_env.set(param, arg)
            return self.evaluate(node.body, new_env)
        env.set(node.name, function)
        return function

    def eval_IfElseNode(self, node, env):
        condition = self.evaluate(node.condition, env)
        if condition:
            return self.evaluate(node.if_body, env)
        else:
            return self.evaluate(node.else_body, env)

    def execute_line(self, line):
        try:
            if line.strip().startswith("#") or not line.strip():
                return  # Ignore comment and empty lines
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            result = self.evaluate(ast)
            print(result)
            return result
        except Exception as e:
            print(e)

    def execute_file(self, filename):
        with open(filename, 'r') as file:
            source_code = file.read()
        for line in source_code.splitlines():
            if line.strip() and not line.strip().startswith("#"):
                print(f"Executing: {line}")
            self.execute_line(line.strip())

    def repl(self):
        while True:
            try:
                line = input('lambda> ')
                self.execute_line(line)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    import sys
    interpreter = Interpreter()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpreter.execute_file(filename)
    else:
        interpreter.repl()
