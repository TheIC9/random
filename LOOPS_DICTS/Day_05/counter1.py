def count_chars(split):
    char_dict = {}
    for char in split:
        if char == " ":
            continue
        if char in char_dict:
            char_dict[char] += 1
        else:
            char_dict[char] = 1
    return (char_dict)