class employee:
    def __init__(self,name):
        self.name = name
class role(employee):
    def __init__(self,name,duty,department):
        super().__init__(name)
        self.duty = duty
        super().__init__(name)
        self.department = department
    
    def task(self):
        return f"The task of the employee {self.name} is {self.duty} in the feild {self.department}"

my_employee = role("Harry","developer","Design Analysis")
print(my_employee.task())