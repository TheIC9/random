s = "House number 42 and zip 12345" 

def extract_digits(s):
    return [c for c in s if c.isdigit()]
print(extract_digits(s))