# Question 7

### Explain the term "lazy evaluation" in the context of the following program:

```python
def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x

print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)

```
###Answer:

In the eager evaluation section, 'generate_values()' is called and all values are generated at once.
This means that the program consumes memory to store all the values, even if not all of them are needed immediately.
The values are then squared, which also happens immediately, and the results are stored in 'squared_values'.
In the lazy evaluation section, 'generate_values()' is used directly in the list comprehension.
Here, values are generated one by one, and each value is squared immediately after it is generated.
This approach is more memory-efficient because values are not stored in memory unless necessary,
and computations are deferred until their results are actually needed.
This is especially useful when working with large datasets or when the entire sequence of values may not be required.
In summary, lazy evaluation allows the program to efficiently handle potentially large or infinite sequences of data
by delaying the generation and processing of values until the exact moment they are needed.
This can lead to significant performance improvements in scenarios where not all values are required at once.