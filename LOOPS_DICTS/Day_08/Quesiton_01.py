a = "The cat and the dog and the mouse"
a = a.lower()
split = a.split()
# print(a) # Output: the cat and the dog and the mous
def my_func(split):
    my_dict = {}
    for word in split:
        if word in my_dict:
            my_dict[word] += 1
        else:
            my_dict[word] = 1
    return my_dict

calling = my_func(split)
final_call = (calling.keys())
print(list(final_call)) # Output: ({'the': 3, 'cat': 1,
