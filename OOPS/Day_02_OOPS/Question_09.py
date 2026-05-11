class vehicle:
    def __init__(self,speed,gears,name):
        self.name = name
        self.gears = gears
        self.speed = speed
class cycle(vehicle):
    def __init__(self,bicycle,speed,gears,name):
        super().__init__(speed,gears,name)
        self.bicycle = bicycle
    # def gear_count(self):
    #     return f"The gear count of {self.bicycle} is  3 x 7 while the speed is {self.gears} ."
    def vehicle_info(self):
         return f"The gear count of {self.bicycle} 3 x 7 while the speed is {self.gears} ."
    @staticmethod
    def vehicle_name():
        return "Your vehicle is great"
my_vehicle = cycle("BMX has ","3 X 7","21","")

print(my_vehicle.vehicle_name())
print(my_vehicle.vehicle_info())