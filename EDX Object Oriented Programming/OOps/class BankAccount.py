class BankAccount:
    """
    Create  a class with 4 methods
    this is called as block code.
    """
    def __init__(self, name, balance = 0):
        self.log("Account Created")
        self.name = name
        self.balance = balance

    def get_balance(self):
        """
        Getter for balance
        :return: balance amount
        """
        self.log("Balance checked at " + str(self.balance))
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        self.log("+ " + str(amount) + "credited. New Balance is:"+str(self.balance))

    def withdraw(self, amount):
        self.balance -= amount
        self.log("+ " + str(amount) + "Withdrawn. New Balance is:"+str(self.balance))

    def log(self, message): #  Logging a message
        my_log = open("Log.txt", "a")
        print(message, file=my_log)
        my_log.close()

my_bank_account = BankAccount("Sanket Wagh", balance=0)
my_bank_account.deposit(100)
my_bank_account.withdraw(50)
my_bank_account.deposit(1000)
my_bank_account.withdraw(1050)
my_bank_account.deposit(1)
my_bank_account.withdraw(-146)
print(my_bank_account.get_balance())

