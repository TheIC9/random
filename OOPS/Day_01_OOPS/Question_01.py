class car:
    def __init__(self,brand,year):
        self.year = year 
        self.brand = brand
my_car = car("Porsche",2022)
print(my_car.brand)
print(my_car.year)