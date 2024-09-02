from functools import reduce

def ex_4(op):
    return lambda seq: reduce(op, seq)

factorial = lambda n: ex_4(lambda x, y: x * y)(range(1, n + 1))
exponentiation = lambda base, exp: ex_4(lambda x, y: x * y)([base] * exp)

print(factorial(5))  # Output: 120 (5!)
print(exponentiation(2, 3))  # Output: 8 (2^3)