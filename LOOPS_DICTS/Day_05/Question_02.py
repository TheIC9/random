a = "hello"
def check_str(a):
    my_dict= {}
    for char in a:
        if char in my_dict:
            return False
        my_dict[char]= +1
    return True
        
print(check_str(a))