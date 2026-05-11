sentence ="I am coding in Python"
letter = "n"
def count_ending_with(sentence, letter):
    return sum(1 for word in sentence.split() if word.endswith(letter))
print(count_ending_with(sentence,letter))