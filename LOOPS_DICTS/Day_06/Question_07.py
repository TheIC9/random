my_set=[1, 2, 3, 2, 4, 1, 1]
def my_func(my_set):
    my_dict ={}
    for item in my_set:
        if item in my_dict:
            my_dict[item]+= 1
        else:
            my_dict[item] = 1
    return my_dict

high_feq = (my_func(my_set))
final_ans = max(high_feq, key = high_feq.get)
print(final_ans)
# print(my_dict)
