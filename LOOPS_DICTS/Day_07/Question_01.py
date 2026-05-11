my_set= [1, 2, 2, 3, 4, 4, 4]
def my_func(my_set):
    my_dict ={}
    for item in my_set:
        if item in my_dict:
            my_dict[item]+= 1
        else:
            my_dict[item] = 1
    return my_dict

high_feq = (my_func(my_set))
final_ans = len(high_feq)
print(final_ans)