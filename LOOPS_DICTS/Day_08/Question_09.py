s1 = "hello"
s2 = "world"
def common_chars(s1, s2):
    return set(s1) & set(s2)
common_chars(s1,s2)