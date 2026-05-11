import random

class Account:
    def __init__(self,name):
        self.name = name
        print(f"The name of the Holder is {self.name}")
        self.balance = random.randint(100000,120000)
        print(f"The balance of the account is {self.balance}")
class Deposit(Account):
    def __init__(self, name):
        super().__init__(name)
        self.deposit = int(input("Enter a value: "))
    def call(self):
        return f"The amount is {self.deposit + self.balance}"
    
my_account = Deposit("IC")
print(my_account.call())