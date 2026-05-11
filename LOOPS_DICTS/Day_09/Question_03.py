s = "Hello world" 
def reversing(s):
    words = s.split()
    reversed_order = words[::-1]
    reversed_words = [word[::-1] for word in reversed_order]
    return " ".join(reversed_words)
print(reversing(s))