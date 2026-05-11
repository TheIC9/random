a = [1, 2, 3, 4] 
b = [3, 4, 5, 6]
def common_elements(a,b):
    c = set()
    for element in a:
        if element in b:
            c.add(element)
    return c 
common_elements(a,b)
print(list(common_elements(a,b)))