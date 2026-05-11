class Animal:
    def sound(self):
        print("Animal makes a generic sound")

class cat(Animal):
    def sound(self):
        super().sound()
        print("Meow")
class dog(cat):
    def sound(self):
        print("woof!")
class cow(cat):
    def sound(self):
        print("Moo!")

my_cat = cat()
my_cat.sound()

my_dog = dog()
my_dog.sound()

my_cow = cow()
my_cow.sound()