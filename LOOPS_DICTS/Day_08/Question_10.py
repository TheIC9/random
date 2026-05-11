a = "The dog and the Dog"
a = a.lower()
split = a.split()
# print(split)
def word_splitter(split):
    my_dict = {}
    for word in split:
        if word in my_dict:
            my_dict[word]+= 1
        else:
            my_dict[word] = 1
    return my_dict

print(word_splitter(split))
