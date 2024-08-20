q1 = lambda n: (lambda f: f(f, n, [0, 1]))(lambda f, n, acc: acc if n <= 2 else f(f, n-1, acc + [acc[-1] + acc[-2]]))

# Example usage
n = 10
print(q1(n))
