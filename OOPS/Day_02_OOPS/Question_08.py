class vehicle:
    def __init__(self,speed,gears):
        self.speed = speed
        self.gears = gears
class cycle(vehicle):
    def __init__(self,bicycle,speed,gears):
        super().__init__(gears,speed)
        self.bicycle = bicycle
    def gear_count(self):
        return f"The gear count of {self.bicycle} is  3 x 7 while the speed is {self.gears} ."

my_vehicle = cycle("Your vehicle has ","21","3 X 7")

print(my_vehicle.gear_count())