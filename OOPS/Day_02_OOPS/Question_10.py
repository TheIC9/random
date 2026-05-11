class Animal:
    def __init__(self,name,info):
        print("I am a living creature")
        self.name = name
        self.info = info 
class dog(Animal):
    def information(self):
        print(f"{self.name} is the name of the Dog.While the info of the dog is ' {self.info} ' .")
    @staticmethod
    def greet():
        return "Your dog looks good."


my_animal = dog("Breeze","Breed: Shitzu , Height: 40 cms")
my_animal.information()