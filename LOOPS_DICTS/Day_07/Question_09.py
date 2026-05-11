a = "Python is fun" 
split = a.split()
# print(split)
def join_words(split):
    word = set()
    for word in split:
        word = "-".join(split)
    return word
join_words(split)
print(join_words(split))