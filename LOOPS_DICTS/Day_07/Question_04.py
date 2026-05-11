a = "Hello, World!"
a = a.replace(',','')
split = a.split()
def joining(split):
    for words in split:
        words = " ".join(split)
    return words
# joining(split)
print(joining(split))