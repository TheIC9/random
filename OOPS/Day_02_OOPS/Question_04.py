class Animal:
    def sound(self):
        print("Animal makes a generic sound")

class Cat(Animal):
    def sound(self):
        super().sound()
        print("Meow!")

class Cow(Animal):
    def sound(self):
        print("Moo!")

class Dog(Animal):
    def sound(self):
        print("Woof!")

class Zoo:
    def _init_(self):
        self.animals = []  # list to hold Animal objects

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal._class.name_} added to the zoo.")

    def make_all_sounds(self):
        print("\nAll animals in the zoo make sounds:")
        for animal in self.animals:
            animal.sound()

# Create a zoo
my_zoo = Zoo()

# Add animals to the zoo
my_zoo.add_animal(Cat())
my_zoo.add_animal(Cow())
my_zoo.add_animal(Dog())

# Make all animals sound
my_zoo.make_all_sounds()