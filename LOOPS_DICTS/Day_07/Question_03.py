from collections import Counter
my_set= [1, 2, 2, 3, 4, 4, 4] 
count = Counter(my_set)
def most_common(count):
    b = set()
    for items in count:
        if count[items] > 1:
            b.add(items)
        else:
            continue
    return b 
print(list(most_common(count)))
