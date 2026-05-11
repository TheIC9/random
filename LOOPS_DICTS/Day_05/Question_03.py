from counter import count_chars

text1 = "aabbcc"

b = count_chars(text1)
# print(b) 
text2 = "baccab"
d = count_chars(text2)
# print(d) 
if b == d:
    print(True)
else:
    print(False) 