class car:
    def __init__(self,brand = None,year = None,display_info = None):
        self.year = year 
        self.brand = brand
        self.display_info = display_info
    # def __init__(self,display_info):
my_car = car(brand = "Porsche",year = 2022)
details = car(display_info = "This has a v8 engine")
print(my_car.brand)
print(my_car.year)
print(details.display_info)