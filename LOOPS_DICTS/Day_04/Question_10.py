d1 = {"a": 1, "b": 2}
d2 = {"a": 1}
def check_dict(d1,d2):
    return all(item in d1.items() for item in d2.items())
print(check_dict(d1,d2))