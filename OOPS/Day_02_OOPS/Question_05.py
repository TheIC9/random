class employee:
    def __init__(self,name):
        self.name = name
class role(employee):
    def __init__(self,name,duty):
        super().__init__(name)
        self.duty = duty
    
    def task(self):
        return f"The task of the employee {self.name} is {self.duty}"

my_employee = role("Harry","developer")
print(my_employee.task())