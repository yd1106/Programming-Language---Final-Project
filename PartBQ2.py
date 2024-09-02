from functools import reduce

q2 = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)
# Example usage
print(q2(["Yarin", "Yuval", "Yuval", "Project"]))
