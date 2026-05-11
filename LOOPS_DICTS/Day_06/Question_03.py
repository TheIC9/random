a = [1, 2, 3, 4, 5, 6]
# item = 0 
def my_func(a):
    my_set = set()
    for item in a:
        if item % 2 == 0:
            my_set.add(item)
    return (sum(my_set))
    # return ((my_set))

print(my_func(a))