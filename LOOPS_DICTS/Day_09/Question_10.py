s = "abcde"
def split_pairs(s):
    if len(s) % 2 != 0:
        s += '_'
    return [s[i:i+2] for i in range(0, len(s), 2)]
print(split_pairs(s))