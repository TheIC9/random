class Dogs:
    def __init__(self,name,age):
        self.name = name
        self.age = age

my_dog = Dogs("Shitzu",5)
his_dog = Dogs("Golden",6)
print(my_dog.name,my_dog.age)
print(his_dog.name,his_dog.age)