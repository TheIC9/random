
number = [1, 2, 2, 3, 1, 1]
def frequency_dict(number):
    freq = {}
    for num in number:
        freq[num] = freq.get(num, 0) + 1
    return freq


print(frequency_dict(number))
