import random

class Account:
    def __init__(self, name):
        self.name = name
        print(f"The name of the Holder is {self.name}")
        self.balance = random.randint(100000, 120000)
        print(f"The balance of the account is {self.balance}")

    @staticmethod
    def greet():
        print("Welcome to WTF Bank")

class Deposit(Account):
    def __init__(self, name):
        super().__init__(name)
        self.deposit = int(input("Enter deposit amount: "))

    def show_total_balance(self):
        return f"After deposit, total balance is {self.deposit + self.balance}"

class New(Deposit):
    def __init__(self, name):
        super().__init__(name)
        self.new_balance = int(input("Enter the new balance: "))

    def calling(self):
        if self.new_balance > 0:
            return f"The new balance is {self.new_balance}"
        else:
            return "Enter a valid balance"

class Create(New):
    def __init__(self, name, account_number):
        super().__init__(name)
        self.account_number = account_number
    def __str__(self):
        return f"Account holder: {self.name} , Number : {account_number}"

    def __len__(self):
        return len(self.account_number)
    def created(self):
        return f"Account created for {self.name} with account number {self.account_number}."

# Usage
Account.greet()
my_account = Create("IC", "5000")
print(my_account.calling())
print(my_account.show_total_balance())
print(my_account.created())
print(len(my_account))

