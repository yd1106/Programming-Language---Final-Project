from lexer import Lexer
from my_parser import *


# Class representing an environment (variable/function scope)
class Environment:
    def __init__(self, parent=None):
        self.variables = {}  # Dictionary to store variable/function names and their values
        self.parent = parent  # Parent environment for nested scopes

    def get(self, name):
        """
        Retrieve a variable's value from the current or parent environment.

        :param name: The name of the variable to retrieve.
        :return: The value of the variable.
        :raises Exception: If the variable is not found.
        """
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Error: Variable '{name}' not found")

    def set(self, name, value):
        """
        Set a variable's value in the current environment.

        :param name: The name of the variable.
        :param value: The value to assign to the variable.
        """
        self.variables[name] = value


# Interpreter class to evaluate the AST nodes
class Interpreter:
    def __init__(self):
        self.global_env = Environment()  # Global environment for storing variables and functions
        self.call_stack = []  # Call stack for managing function calls and recursion

    def evaluate(self, node, env=None):
        """
        Evaluate a given AST node.

        :param node: The AST node to evaluate.
        :param env: The environment to use for variable/function lookups.
        :return: The result of the evaluation.
        :raises Exception: If the node type is not supported.
        """
        if env is None:
            env = self.global_env

        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            raise Exception(f"No method to evaluate node type {type(node).__name__}")
        return method(node, env)

    def eval_NumberNode(self, node, env):
        """
        Evaluate a NumberNode and return its value.

        :param node: The NumberNode to evaluate.
        :param env: The environment (unused).
        :return: The integer value of the node.
        """
        return node.value

    def eval_BooleanNode(self, node, env):
        """
        Evaluate a BooleanNode and return its value.

        :param node: The BooleanNode to evaluate.
        :param env: The environment (unused).
        :return: The boolean value of the node.
        """
        return node.value

    def eval_IdentifierNode(self, node, env):
        """
        Evaluate an IdentifierNode and return its value from the environment.

        :param node: The IdentifierNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The value of the identifier.
        """
        return env.get(node.name)

    def eval_BinaryOpNode(self, node, env):
        """
        Evaluate a BinaryOpNode and return the result of the binary operation.

        :param node: The BinaryOpNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The result of the binary operation.
        """
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)

        if node.op in ('+', '-', '*', '/', '%'):
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError(
                    f"Unsupported operand type(s) for {node.op}: '{type(left).__name__}' and '{type(right).__name__}'")
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
                raise TypeError(
                    f"Unsupported operand type(s) for {node.op}: '{type(left).__name__}' and '{type(right).__name__}'")
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
        """
        Evaluate a UnaryOpNode and return the result of the unary operation.

        :param node: The UnaryOpNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The result of the unary operation.
        """
        operand = self.evaluate(node.operand, env)
        if node.op == '!':
            if not isinstance(operand, bool):
                raise TypeError(f"Unsupported operand type for {node.op}: '{type(operand).__name__}'")
            return not operand
        else:
            raise Exception(f"Error: Unsupported unary operator: '{node.op}'")

    def eval_LambdaNode(self, node, env):
        """
        Evaluate a LambdaNode and return a lambda function.

        :param node: The LambdaNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The lambda function.
        """

        def lambda_func(*args):
            if len(args) != len(node.params):
                raise Exception(f"Error: Lambda expected {len(node.params)} arguments but got {len(args)}.")
            new_env = Environment(parent=env)
            for param, arg in zip(node.params, args):
                new_env.set(param, arg)
            return self.evaluate(node.body, new_env)

        return lambda_func

    def eval_FunctionCallNode(self, node, env):
        """
        Evaluate a FunctionCallNode and return the result of the function call.

        :param node: The FunctionCallNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The result of the function call.
        """
        func = self.evaluate(node.func, env)
        if not callable(func):
            raise Exception(f"Error: Attempt to call a non-function value '{func}'.")
        args = [self.evaluate(arg, env) for arg in node.args]
        return func(*args)

    def eval_FunctionDefNode(self, node, env):
        """
        Evaluate a FunctionDefNode and define the function in the environment.

        :param node: The FunctionDefNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: A message indicating the function was created.
        """

        def function(*args):
            if len(args) != len(node.params):
                raise Exception(
                    f"Error: Function '{node.name}' expected {len(node.params)} arguments but got {len(args)}.")
            new_env = Environment(parent=env)
            for param, arg in zip(node.params, args):
                new_env.set(param, arg)
            return self.evaluate(node.body, new_env)

        env.set(node.name, function)
        return "Function created!"

    def eval_IfElseNode(self, node, env):
        """
        Evaluate an IfElseNode and return the result of the if-else expression.

        :param node: The IfElseNode to evaluate.
        :param env: The environment to use for variable lookups.
        :return: The result of the if-else expression.
        """
        condition = self.evaluate(node.condition, env)
        if condition:
            return self.evaluate(node.if_body, env)
        else:
            return self.evaluate(node.else_body, env)

    def execute_line(self, line):
        """
        Execute a single line of code.

        :param line: The line of code to execute.
        :return: The result of the execution or None.
        """
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
        """
        Execute a file containing code.

        :param filename: The name of the file to execute.
        """
        with open(filename, 'r') as file:
            source_code = file.read()
        for line in source_code.splitlines():
            if line.strip() and not line.strip().startswith("#"):
                print(f"Executing: {line}")
            self.execute_line(line.strip())

    def repl(self):
        """
        Read-Eval-Print Loop (REPL) for interactive execution.
        """
        while True:
            try:
                line = input('YGH> ')
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
