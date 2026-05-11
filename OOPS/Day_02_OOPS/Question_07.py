class call:
    def __init__(self, entity):
        self.entity = entity

class Employee(call):
    def __init__(self, entity, name):
        super().__init__(entity)
        self.name = name

    def __str__(self):
        return f"Employee {self.name} working in {self.entity}"
            
class Manager(call):
    def __init__(self,entity,name):
        super().__init__(entity)
        self.name = name
    def __str__(self):
        return f"Employee {self.name} working in {self.entity}"

my_employee_1 = Employee("Senior_Dev","Harry")
my_manager = Manager("Developer","IC")
print(my_employee_1)
print(my_manager)