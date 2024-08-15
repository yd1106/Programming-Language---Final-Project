from interpreter import Interpreter

def run_test(test_name, code):
    print(f"Running test: {test_name}")
    print(f"Code: {code}")
    try:
        interpreter = Interpreter()
        lines = code.split('\n')  # Split the code into lines
        for line in lines:
            result = interpreter.execute_line(line)  # Execute each line separately
        print(f"Output: {result}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def run_lambda_file(file_path):
    print(f"Running test: {file_path}")
    try:
        interpreter = Interpreter()
        interpreter.execute_file(file_path)
    except Exception as e:
        print(f"Error: {e}")
    print()

def main():
    tests = [
        # Simple Tests
        ("Addition", "2 + 3"),  # Should print 5
        ("Subtraction", "5 - 2"),  # Should print 3
        ("Multiplication", "3 * 4"),  # Should print 12
        ("Division", "10 / 2"),  # Should print 5
        ("Modulo", "10 % 3"),  # Should print 1

        # Boolean and Comparison Tests
        ("Boolean AND", "True && False"),  # Should print False
        ("Boolean OR", "True || False"),  # Should print True
        ("Boolean NOT", "!False"),  # Should print True
        ("Comparison Equal", "3 == 3"),  # Should print True
        ("Comparison Not Equal", "3 != 4"),  # Should print True
        ("Comparison Less Than", "3 < 4"),  # Should print True
        ("Comparison Greater Than", "4 > 3"),  # Should print True
        ("Comparison Less Than or Equal", "3 <= 3"),  # Should print True
        ("Comparison Greater Than or Equal", "4 >= 3"),  # Should print True

        # Lambda and Function Tests
        ("Lambda Function", "(lambda x: x + 1)(2)"),  # Should print 3
        ("Function Definition", "def add(x, y): x + y\nadd(2, 3)"),  # Should print 5
        ("If-Else True", "if True: 1 else: 0"),  # Should print 1
        ("If-Else False", "if False: 1 else: 0"),  # Should print 0
        ("Recursion", "def fact(n): if n <= 1: 1 else: n * fact(n - 1)\nfact(5)"),  # Should print 120

        # Nested Functions and Lambdas
        ("Function Within Function", "def add(x): x + x\ndef mul(x): x * x\nmul(add(2))"),  # Should print 16
        ("Lambda Within Lambda", "(lambda x: (lambda y: x + y)(2))(3)"),  # Should print 5
        ("Function Within Lambda", "def inner(x, y): x + y\n(lambda x, y: inner(x, y) + x + y)(3, 2)"),  # Should print 10

        # Recursion to Simulate While Loop
        ("Simulate While Loop", "def increment(x): if x < 10: increment(x * x) else: x\nincrement(3)"),  # Should print 10

        # Error Tests
        ("Division by Zero", "10 / 0"),  # Should raise ZeroDivisionError
        ("Lambda Argument Error", "(lambda x, y: x + y)(2)"),  # Should raise Exception
        ("Undefined Function", "unknown_function()"),  # Should raise Exception
        ("Syntax Error", "if True 1 else 0"),  # Should raise SyntaxError
    ]

    for test_name, code in tests:
        run_test(test_name, code)

    # Run test.lambda file
    run_lambda_file("test.lambda")

if __name__ == "__main__":
    main()
