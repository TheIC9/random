a = "The fox jumped over the lazy dog"
a = a.lower()
split = a.split()

long_words = [word for word in split if len(word) > 3]
print(long_words)
