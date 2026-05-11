text = "Python is amazing"
words = text.split()

def max_len(word_list):
    word_lengths = {word: len(word) for word in word_list}
    return word_lengths

char_freq = max_len(words)
max_freq = max(char_freq, key=char_freq.get)
print(max_freq)
