# from dict_counter import word_splitter

a = [1,2,3,4] 
b = [1,2,2,3]
def all_unique(a):
    return len(a) == len(set(a))

print(all_unique(a))