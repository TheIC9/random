class Animal:
    def __init__(self):
        print("Animal sound")
    
class Cat(Animal):
    def sound(self):
        print("Meow!")
    
my_dog = Cat()
my_dog.sound()