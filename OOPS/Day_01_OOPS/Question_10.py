class Calculator:
    def __init__(self,a,b):
        self.a = a
        self.b = b 
    def sum(self):
        return self.a+self.b
    def sub(self):
        return self.a - self.b
    def mul(self):
        return self.a*self.b
    def div(self):
        if self.b ==0:
            return "error division invalid."
        else:
            return self.a %self.b
a = int(input("Enter a value: "))
b = int(input("Enter a value: "))
calc = Calculator(a,b)
print(f"The sum of the numbers is {calc.sum()}")
print(f"The sub of the numbers is {calc.sub()}")
print(f"The mul of the numbers is {calc.mul()}")
print(f"The div of the numbers is {calc.div()}")