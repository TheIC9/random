a = [1, -2, 3, -4, 5]
def my_set(a):
    b = set()
    for items in a:
        if items >0 :
            b.add(items)
        else:
            continue
    return list(b)
print(my_set(a))