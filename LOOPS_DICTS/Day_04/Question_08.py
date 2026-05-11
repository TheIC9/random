list1 = [{"id": 1, "name": "Alice"}]
list2 = [{"id": 1, "score": 90}]

def join(list1,list2):
    list1.update(list2)
    return list1 
print(join(list1,list2))  # Output: {'a': 1, 'b': 2