import random

class Bank:
    def __init__(self, name):
        self.name = name
        self.balance = random.randint(56435, 75543)

    def deposit(self):
        s = 12000  # fixed deposit amount
        self.balance += s  # update balance in place
        print(f"Deposited {s}. New balance is {self.balance}")
    def withdrawl(self):
        b = 13000
        if self.balance < b:
            print("Insufficient funds")
        else:
            self.balance = self.balance - b 
        print(f"The amount you withdrew is {b} and the balance is {self.balance}")

my_balance = Bank("Pratik")
print(f"Hello {my_balance.name}, your starting balance is {my_balance.balance}")

# Perform the deposit
my_balance.deposit()
my_balance.withdrawl()
# Print updated balance
print(f"After deposit, your balance is {my_balance.balance}")
