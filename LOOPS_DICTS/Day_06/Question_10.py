words = "I love Python"
word = words.split()
# print(word)
def counting(word):
    my_dict = {}
    for item in word:
            my_dict[item] = len(item)
    return my_dict
  
print(counting(word))