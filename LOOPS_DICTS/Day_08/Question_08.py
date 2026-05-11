import re
s = "My emails are test@example.com and info@domain.org"
def extract_emails(text):
    return re.findall(r'\S+@\S+', text)
extract_emails(s)