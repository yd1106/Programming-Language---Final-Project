from lexer import Lexer
from my_parser import *

# Environment class to handle variable scopes and function environments
class Environment:
    def __init__(self, parent=None):
        # Store variables in a dictionary
        self.variables = {}
        # Link to parent environment for nested scopes
        self.parent = parent

    def get(self, name):
        # Retrieve a variable's value from the current or parent environment
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f'Variable {name} not found')

    def set(self, name, value):
        # Set a variable's value in the current environment
        self.variables[name] = value

# Interpreter class to evaluate AST nodes
class Interpreter:
    def __init__(self):
        # Global environment for storing variables and functions
        self.global_env = Environment()
        # Call stack for managing function calls and recursion
        self.call_stack = []

    def evaluate(self, node, env=None):
        if env is None:
            env = self.global_env

        # Dynamically call the appropriate evaluation method based on node type
        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name)
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
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '&&':
            return left and right
        elif node.op == '||':
            return left or right
        elif node.op == '==':
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
            raise Exception(f'Unsupported binary operator: {node.op}')

    def eval_UnaryOpNode(self, node, env):
        operand = self.evaluate(node.operand, env)
        if node.op == '!':
            return not operand
        else:
            raise Exception(f'Unsupported unary operator: {node.op}')

    def eval_LambdaNode(self, node, env):
        # Return a lambda function that captures the current environment
        def lambda_func(*args):
            new_env = Environment(parent=env)
            for param, arg in zip(node.params, args):
                new_env.set(param, arg)
            return self.evaluate(node.body, new_env)
        return lambda_func

    def eval_FunctionCallNode(self, node, env):
        func = self.evaluate(node.func, env)
        args = [self.evaluate(arg, env) for arg in node.args]
        return func(*args)

    def eval_FunctionDefNode(self, node, env):
        # Define a function that captures the current environment
        def function(*args):
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
        lexer = Lexer(line)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluate(ast)
        print(result)
        return result

    def execute_file(self, filename):
        with open(filename, 'r') as file:
            source_code = file.readlines()
        for line in source_code:
            if line.strip() and not line.strip().startswith('#'):
                print(f"Executing: {line.strip()}")
                result = self.execute_line(line.strip())
                print(result)

    def repl(self):
        while True:
            try:
                line = input('lambda> ')
                result = self.execute_line(line)
                print(result)
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
#