a = [1,3,4,56]
for index,values in enumerate(a):
    print(values)
    if (values == max(a)):
        print(f"The highest value is {values}")
    else:
        continue