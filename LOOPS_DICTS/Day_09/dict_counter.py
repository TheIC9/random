def word_splitter(a):
    my_dict = {}
    for word in a:
        if word in my_dict:
            my_dict[word]+= 1
        else:
            my_dict[word] = 1
    return my_dict
