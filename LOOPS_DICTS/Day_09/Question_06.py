def count_vowels_in_words(s):
    vowels = "aeiou"
    words = s.split()
    vowel_counts = {}
    for word in words:
        count = 0
        for letter in word.lower():
            if letter in vowels:
                count += 1
        vowel_counts[word] = count
    return vowel_counts

s = "Hello world"
result = count_vowels_in_words(s)
print(result)
