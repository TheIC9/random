from dict_counter import word_splitter

s = "The dog and the Dog"
s = s.lower()
a = s.split()
articles = {"a", "an", "the"}
b = (word_splitter(a))
filtered = {k: v for k, v in b.items() if k not in articles}
if filtered:
    final = max(filtered, key=filtered.get)
    print(final)
else:
    print("No valid words to count.")
