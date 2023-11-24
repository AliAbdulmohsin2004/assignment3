class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")
        if amount <= self.balance:
            self.balance -= amount
            return self.balance
        else:
            raise ValueError("Insufficient funds.")


class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, min_balance=2000):
        super().__init__(account_number, balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")

        available_balance = self.balance - self.min_balance

        if amount <= available_balance:
            self.balance -= amount
            return self.balance
        else:
            raise ValueError(f"Withdrawal rejected. Insufficient funds. Maximum allowed withdrawal: {available_balance}")


class ChequingAccount(Account):
    def __init__(self, account_number, balance=0, overdraft_limit=5000):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")

        available_funds = self.balance + self.overdraft_limit

        if amount <= available_funds:
            self.balance -= amount
            return self.balance
        else:
            raise ValueError(f"Withdrawal rejected. Insufficient funds including overdraft limit. Available funds: {available_funds}")


class Bank:
    def __init__(self):
        self.accounts = []  
        
        self.accounts.append(ChequingAccount(111, 1000, 5000))
        self.accounts.append(ChequingAccount(222, 2000, 3000))
        self.accounts.append(ChequingAccount(333, 3000, 4000))
        self.accounts.append(SavingsAccount(444, 4000, 1000))
        self.accounts.append(SavingsAccount(555, 5000, 2000))
        self.accounts.append(SavingsAccount(666, 6000, 3000))

    def search_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None  

    def open_account(self, account_number, initial_balance, account_type):
        if self.search_account(account_number) is not None:
            print("Account already exists with the same account number.")
        else:
            if account_type == "Savings":
                new_account = SavingsAccount(account_number, initial_balance)
            elif account_type == "Chequing":
                new_account = ChequingAccount(account_number, initial_balance)
            else:
                print("Invalid account type.")
                return

            self.accounts.append(new_account)
            print(f"Account {account_number} opened successfully.")


class Application:
    def __init__(self):
        self.current_account = None
        self.bank = Bank()

    def show_main_menu(self):
        while True:
            print("\nBanking Main Menu:")
            print("1. Select Account")
            print("2. Open Account")
            print("3. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    self.select_account()
                elif choice == '2':
                    self.open_account()
                elif choice == '3':
                    break
                else:
                    raise ValueError("Invalid choice. Please enter a valid option.")
            except ValueError as ve:
                print(f"Error: {ve}")

    def select_account(self):
        account_number = int(input("Enter account number: "))

        try:
            self.current_account = self.bank.search_account(account_number)
            if self.current_account is None:
                raise ValueError("Account not found.")
            else:
                self.show_account_menu()
        except ValueError as ve:
            print(f"Error: {ve}")

    def open_account(self):
        account_number = int(input("Enter account number for the new account: "))

        try:
            if self.bank.search_account(account_number) is not None:
                raise ValueError("Account already exists with the same account number.")
            else:
                initial_balance = self.get_valid_amount("Enter initial balance for the new account: ")
                account_type = input("Enter account type (Savings or Chequing): ")

                if account_type.lower() == "savings":
                    self.bank.open_account(account_number, initial_balance, "Savings")
                elif account_type.lower() == "chequing":
                    self.bank.open_account(account_number, initial_balance, "Chequing")
                else:
                    raise ValueError("Invalid account type. Please enter either Savings or Chequing.")

        except ValueError as ve:
            print(f"Error: {ve}")

    def show_account_menu(self):
        while True:
            print("\nAccount Menu:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit Account")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    balance = self.current_account.check_balance()
                    print(f"Current Balance: {balance}")
                elif choice == '2':
                    amount = self.get_valid_amount("Enter amount to deposit: ")
                    new_balance = self.current_account.deposit(amount)
                    print(f"Deposited. New Balance: {new_balance}")
                elif choice == '3':
                    amount = self.get_valid_amount("Enter amount to withdraw: ")
                    result = self.current_account.withdraw(amount)
                    print(f"Withdrawn. New Balance: {result}")
                elif choice == '4':
                    break
                else:
                    raise ValueError("Invalid choice. Please enter a valid option.")
            except ValueError as ve:
                print(f"Error: {ve}")

    def get_valid_amount(self, prompt):
        while True:
            try:
                amount = float(input(prompt))
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
                return amount
            except ValueError:
                print("Invalid input. Please enter a valid positive number.")

    def run(self):
        self.show_main_menu()



if __name__ == "__main__":
    bank_app = Application()
    bank_app.run()

