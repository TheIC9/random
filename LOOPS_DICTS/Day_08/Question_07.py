import re
a = "Hello    world   this is   Python"
a = re.sub(r"\s+", " ", a)
print(a)
