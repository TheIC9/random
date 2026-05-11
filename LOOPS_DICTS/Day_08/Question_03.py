import string

def is_pangram(sentence):
    alphabet = set(string.ascii_lowercase)
    return alphabet <= set(sentence.lower())

# Test it
print(is_pangram("The quick brown fox jumps over the lazy dog."))