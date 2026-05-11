a = "Python is awesome"
split= a.split()
def rev_set(split):
    return (split)[::-1]

word_rev = rev_set(split)
final_set = " ".join(word_rev)
print(final_set)