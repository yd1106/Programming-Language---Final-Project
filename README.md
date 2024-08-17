# Custom Language Interpreter User Guide

## Introduction

This guide explains how to run the custom language interpreter in both interactive mode (line-by-line execution) and full program execution mode. The interpreter can handle files with the `.lambda` suffix and print the result of each command after its execution.

## Prerequisites

- Ensure you have Python installed on your system.
- Save your interpreter code in a file named `interpreter.py`.
- Save your language programs with the `.lambda` suffix.

## Running the Interpreter

### Interactive Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing `interpreter.py`.
3. Run the following command:

    ```sh
    python interpreter.py
    ```

4. You will see the prompt `YGH>`. You can now enter commands line by line. After typing each command, press Enter to execute it and see the result.

    Example:

    ```plaintext
    YGH> 2 + 3
    5
    YGH> def add(x, y): x + y
    Function created!
    YGH> add(2, 3)
    5
    YGH> (lambda x: x + 1)(4)
    5
    YGH> if True: 1 else: 0
    1
    ```

    To exit the interactive mode, press `Ctrl+C` and press Enter.

### Full Program Execution Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing `interpreter.py` and your `.lambda` program file.
3. Run the following command:

    ```sh
    python interpreter.py your_program.lambda
    ```

    Replace `your_program.lambda` with the name of your `.lambda` file.

    Example:

    Assuming you have a file named `test.lambda` with the following content:

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
    ```

    Run the following command:

    ```sh
    python interpreter.py test.lambda
    ```

    You will see the interpreter execute each line and print the results:

    ```plaintext
    Executing: def add(a, b): a + b
    Function created!
    Executing: def multiply(a, b): a * b
    Function created!
    Executing: def factorial(n): if n == 0: 1 else: n * factorial(n - 1)
    Function created!
    Executing: add(2, 3)
    5
    Executing: multiply(3, 4)
    12
    Executing: factorial(5)
    120
    Executing: (lambda x: x + 1)(10)
    11
    Executing: (lambda f: f(2))(lambda x: x + 3)
    5
    Executing: def make_adder(x): lambda y: x + y
    Function created!
    Executing: (make_adder(10))(5)
    15
    ```

## Conclusion

This guide covers how to run the custom language interpreter in both interactive mode and full program execution mode. By following these steps, you can execute and test your `.lambda` programs easily. If you encounter any issues, ensure that your Python installation is correctly set up and that your program files are properly formatted.
