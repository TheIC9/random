class Bank:
    def __init__(self,name,account_number,balance = 0):
        self.name = name
        self.account_number = account_number
        self.__balance = balance
    @staticmethod
    def greet():
        return " Welcome to the WTF bank"

    def deposit(self,amount):
        amount = int(input("Enter the value : "))
        if amount > 0 :
            self.__balance += amount
        else:
            return "Invalid amount"
    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_balance):
        if new_balance >= 0:
            self.__balance = new_balance
            print(f"Balance updated to {self.__balance}")
        else:
            print("Invalid balance amount.")
    def __str__(self):
        return f"Bank holder: {self.name}, Number: {self.account_number}, Balance: {self.__balance}"

    def __len__(self):
        return len(str(self.__balance))

    def __repr__(self):
        return f"Bank('{self.name}', '{self.account_number}', {self.__balance})"

    def __lt__(self, other):
        return self.__balance < other.__balance

    def created(self):
        return f"Bank created for {self.name} with account number {self.account_number}."
class BankManager:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
        print(f"Added account for {account.name}")

    def total_balance(self):
        return sum(acc.balance for acc in self.accounts)
    
Bank.greet()
acc1 = Bank("Alice", "1234", 5000)
acc2 = Bank("Bob", "5678", 3000)

acc1.deposit(2000)
acc2.deposit(1500)

print(acc1)
print(acc2)

print(f"Is acc1 < acc2? {acc1 < acc2}")

manager = BankManager()
manager.add_account(acc1)
manager.add_account(acc2)
print(f"Total balance in bank: {manager.total_balance()}")

print(f"Number of digits in acc1's balance: {len(acc1)}")

print(f"Developer view: {repr(acc1)}")
        