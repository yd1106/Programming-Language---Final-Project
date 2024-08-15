# Custom Language Interpreter Project Report

## Introduction

This report provides an overview of the design decisions, challenges faced, and solutions implemented during the development of a custom language interpreter. The interpreter supports basic arithmetic, boolean logic, conditional expressions, function definitions and calls, lambda expressions, and recursion. The goal was to create an interpreter that could execute commands both interactively and from a program file, handling various language features effectively.

## Design Decisions

### Language Features

1. **Basic Arithmetic and Boolean Operations**:
   - The language includes support for basic arithmetic operations (`+`, `-`, `*`, `/`, `%`) and boolean operations (`&&`, `||`, `!`).

2. **Comparison Operations**:
   - Support for comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) was included to enable conditional logic.

3. **Conditional Expressions**:
   - `if-else` expressions were implemented to allow for conditional execution of code.

4. **Function Definitions and Calls**:
   - The language supports defining functions using the `def` keyword and calling them with arguments.

5. **Lambda Expressions**:
   - Lambda expressions were added to allow for anonymous functions and higher-order functions.

6. **Recursion**:
   - Recursion was supported to simulate iterative processes and to enable complex function definitions.

7. **Interactive Mode and Program Execution**:
   - The interpreter can run in interactive mode, allowing users to enter commands line by line, and in program execution mode, running a full program from a file.

### Abstract Syntax Tree (AST)

The interpreter uses an Abstract Syntax Tree (AST) to represent the parsed structure of the code. Different types of nodes represent numbers, booleans, identifiers, binary operations, unary operations, function definitions, function calls, lambda expressions, and if-else expressions.

### Environment and Call Stack

An environment was designed to manage variable scopes and function environments. A call stack was implemented to manage function calls and recursion, ensuring proper handling of nested function calls and scope resolution.

## Challenges Faced

### 1. Getting Error Messages Right

**Challenge**:
- Providing meaningful and accurate error messages was crucial for debugging and user experience. Ensuring that the interpreter could identify and report errors accurately, such as type mismatches, undefined variables, and syntax errors, was challenging.

**Example**:
- When a variable is used before it is defined, the interpreter should report an `Undefined Variable` error instead of failing silently or crashing.

```plaintext
x + 5  # Error: Variable 'x' is not defined
```
#### Solution:

- Implemented comprehensive error handling throughout the interpreter. Custom exceptions were used to capture specific error conditions, and detailed error messages were provided to indicate the nature and location of errors.
####Implementation:
```python
class Environment:
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Error: Variable '{name}' not found")

# Example usage in the interpreter
try:
    env.get("x")
except Exception as e:
    print(e)  # Outputs: Error: Variable 'x' not found
```

### 2. Understanding Functions within Functions and Lambdas

**Challenge**:
- Understanding how to implement and correctly use functions within functions and lambdas was complex. Handling scopes, closures, and higher-order functions required careful design.

**Example**:
- Defining a function within another function and using a lambda that captures the outer function’s scope.
plaintext
```plaintext
def outer(x):
    def inner(y):
        return x + y
    return inner

(lambda f: f(2))(outer(3))  # Expected output: 5
```
#### Solution:

- A clear structure was established for the environment and function call handling. Nested environments were created for functions to capture the scope in which they were defined. This allowed functions to access variables from their defining scope even when called in a different context. Lambda expressions were treated similarly, ensuring they could capture and use their defining environment correctly.####Implementation:
```python
def eval_LambdaNode(self, node, env):
    def lambda_func(*args):
        if len(args) != len(node.params):
            raise Exception(f"Error: Lambda expected {len(node.params)} arguments but got {len(args)}.")
        new_env = Environment(parent=env)
        for param, arg in zip(node.params, args):
            new_env.set(param, arg)
        return self.evaluate(node.body, new_env)
    return lambda_func

def eval_FunctionDefNode(self, node, env):
    def function(*args):
        if len(args) != len(node.params):
            raise Exception(f"Error: Function '{node.name}' expected {len[node.params]} arguments but got {len(args)}.")
        new_env = Environment(parent=env)
        for param, arg in zip(node.params, args):
            new_env.set(param, arg)
        return self.evaluate(node.body, new_env)
    env.set(node.name, function)
    return "Function created!"
```

## Solutions Implemented

### Lexer and Parser
- A lexer was implemented to tokenize the input code, breaking it down into meaningful symbols. The parser then built the AST from these tokens, representing the structure of the code in a hierarchical manner.
### Interpreter
- The interpreter was designed to traverse the AST and evaluate the nodes. Different evaluation methods were defined for each node type, ensuring that the interpreter could handle 
- various expressions and statements correctly.
### Testing and Validation
- A comprehensive test suite was developed to validate the interpreter’s functionality. Test cases covered arithmetic operations, boolean logic, comparisons, conditionals, function definitions and calls, lambda expressions, recursion, and nested functions.
- A 30-line program was written to demonstrate the capabilities of the language, ensuring that all features were tested in a cohesive manner.
```plaintext
# Define functions
def add(a, b): a + b
def multiply(a, b): a * b
def factorial(n): if n == 0: 1 else: n * factorial(n - 1)

# Function calls
add(2, 3)      # Expected output: 5
multiply(3, 4) # Expected output: 12
factorial(5)   # Expected output: 120

# Lambda function calls
(lambda x: x + 1)(10)   # Expected output: 11
(lambda f: f(2))(lambda x: x + 3) # Expected output: 5

# Nested function call
def make_adder(x): lambda y: x + y
(make_adder(10))(5) # Expected output: 15

# Recursion to simulate a while loop
def increment(x): if x < 10: increment(x + 1) else: x
increment(0) # Expected output: 10

# Boolean and comparison operations
True && False  # Expected output: False
True || False  # Expected output: True
!False         # Expected output: True

3 == 3  # Expected output: True
3 != 4  # Expected output: True
3 < 4   # Expected output: True
4 > 3   # Expected output: True
3 <= 3  # Expected output: True
4 >= 3  # Expected output: True

# If-Else expressions
if True: 1 else: 0  # Expected output: 1
if False: 1 else: 0 # Expected output: 0

# More complex recursion example
def decrement(x): if x > 0: decrement(x - 1) else: x
decrement(10) # Expected output: 0
```

## Conclusion
The custom language interpreter project successfully implemented a functional programming language with a range of features. Despite challenges in error handling and understanding functions within functions and lambdas, robust solutions were developed. The interpreter can execute commands interactively and from a program file, providing meaningful error messages and supporting complex language constructs. The comprehensive test suite and example programs ensure the interpreter’s reliability and effectiveness.