text = "I love python"
text = text.lower()
split = text.split()
def count_chars(split):
    char_dict = {"a":0,"e":0,"i":0,"o":0,"u":0}
    for char in split:
        if char in char_dict:
            char_dict[char] += 1
    print(char_dict)

count_chars(text)