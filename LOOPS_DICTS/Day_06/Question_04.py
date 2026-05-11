a = "hello"
def replacer(a):
    chars =("a","e",'i',"o","u")
    for word in chars:
        a = a.replace(word,'*')
    return a
print(replacer(a))
