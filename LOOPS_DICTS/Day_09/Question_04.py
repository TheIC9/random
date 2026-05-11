from dict_counter import word_splitter
a = [1,2,2,3]
s = (word_splitter(a))
final = (s.keys())
b = [2,1,3,2]
d = (word_splitter(b))
also = (d.keys())
if final == also:
    print(True)
else:
    print(False)