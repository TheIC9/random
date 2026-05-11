def group_by_last_letter(words):
    d = {}
    for word in words:
        last = word[-1]
        d.setdefault(last, []).append(word)
    return d
words = ["apple", "banana", "cable", "dog"]
group_by_last_letter(words)
print(group_by_last_letter(words))