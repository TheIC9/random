a = "I love Python"
b = "Python is great"
s1 = a.split()
s2 = b.split()
def common(s1,s2):
    for word in s1:
        for word2 in s2:
            if word == word2:
                return word
            else:
                continue
print((common(s1,s2))) 