from counter1 import count_chars

text = "swiss"
char_freq = count_chars(text)
max_freq = min(char_freq,key = char_freq.get)
# print(max_freq)
print(max(count_chars(text)))