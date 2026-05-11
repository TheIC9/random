class Owner:
    def __init__(self, owner_name, main_dog):
        self.owner_name = owner_name
        self.main_dog = main_dog
        self.other_dogs = []

    def more_dogs(self, names):
        self.other_dogs = names

# Create the owner with their main dog
dog = Owner("Meghna", "Aakankshith")

# Call the method on the instance (not the class!)
dog.more_dogs(["Vaishnavi", "Koushik", "Leo", "Rocky"])

# Print the main dog-owner relationship
print(f"Tommy is owned by {dog.owner_name} and is domesticated by {dog.main_dog}")
print(f"More dogs owned by {dog.owner_name} are: {', '.join(dog.other_dogs)}")