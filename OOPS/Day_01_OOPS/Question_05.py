class Dog:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def age_inc(self):
        self.age +=1 


my_dog = Dog("Shitzu",5)
print(my_dog.name,my_dog.age)
# print(my_dog.age)
my_dog.age_inc()

print(my_dog.age)