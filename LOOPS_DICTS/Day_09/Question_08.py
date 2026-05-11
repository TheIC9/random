a = [1,5,3,7]
def threshold_func(a):
    s = set()
    a.sort()
    threshold=4
    for values in a:
        if values > threshold:
            s.add(values)
    return s
print(list(threshold_func(a)))