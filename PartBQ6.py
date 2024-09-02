# One-liner function to count palindromes in each sublist
palindromeCount = lambda lists: list(map(lambda sublist: len(list(filter(lambda s: s == s[::-1], sublist))), lists))

if __name__ == "__main__":
    strings = [["radar", "apple", "level", "banana"], ["racecar", "hello", "world"],
                        ["madam", "test", "civic"]]

    result = palindromeCount(strings)

    print(result)