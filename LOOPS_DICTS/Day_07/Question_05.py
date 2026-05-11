a = "The cat and the dog and the mouse"
def my_func(a):
    my_dict ={}
    words = a.split()
    for item in words:
        if item in my_dict:
            my_dict[item]+= 1
        else:
            my_dict[item] = 1
    return my_dict
my_freqs = my_func(a)
s = set()
for word,count in my_freqs.items():
    if count > 1:
        s.add(word)
print(list(s))
