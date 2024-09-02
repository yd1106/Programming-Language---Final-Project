# One-liner function to filter prime numbers and sort them in descending order
prime_descending = lambda lst: sorted(
    [x for x in lst if all(x % i != 0 for i in range(2, int(x ** 0.5) + 1)) and x > 1], reverse=True)

if __name__ == "__main__":
    numbers = [10, 3, 5, 8, 13, 7, 22, 11, 1, 29]
    result = prime_descending(numbers)
    print(result)