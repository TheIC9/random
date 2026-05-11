a = [1,2,3]
b = set()
for values in a:
    # print(values**2)
    b.add(values**2)
print(sum(b))