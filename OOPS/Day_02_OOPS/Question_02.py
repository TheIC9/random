class Animal:
    def __init__(self):
        print("Animal sound")
    
class Cat(Animal):
    def sound(self):
        print("Meow!")
class Cow(Cat):
    def sound(self):
        print("Moo!")
class Dog(Cat):
    def sound(self):
        print("Woof!")
    
my_cat = Cat()
my_cat.sound()
my_cow = Cow()
my_cow.sound()
my_dog = Dog()
my_dog.sound()
