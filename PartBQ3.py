from functools import reduce
def ex_3_lambda(lists):
    return list(map(  #1
        lambda sublist: reduce(  #2
            lambda acc, x: acc + x**2,  #3
            filter(  #4
                lambda num: num % 2 == 0,  #5
                sublist
            ),
            0
        ),
        lists
    ))

input_lists = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
result = ex_3_lambda(input_lists)
print(result)  # Output: [20, 100, 244]