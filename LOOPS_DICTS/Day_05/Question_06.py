from counter import count_chars

text = "abracadabra"
char_freq = count_chars(text)
max_freq = max(char_freq,key = char_freq.get)
print(max_freq)
# print(max(count_chars(text)))