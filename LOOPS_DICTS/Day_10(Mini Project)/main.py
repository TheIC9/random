#with open ("file.txt ") as f:
	#a = f.read()
a = "Python is amazing! Python can do many things. I love Python because it is easy, powerful, and fun. Programming in Python makes me feel productive and creative. The more I learn Python, the more I enjoy coding."
a= a.split()
def paragraph(a):
	my_dict={}
	for word in a:
		if word in my_dict:
			my_dict[word]+= 1
		else:
			my_dict[word]= 1
	return my_dict
#print(paragraph(a))
s = paragraph(a)
vowels = {}
final = max(s,key=s.get)
print(final)