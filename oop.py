from datetime import date, datetime, timedelta
import numpy as np

class Bank:
    accounts = []
    account_holders = []
    def __init__(self):

        self.bookkeeping_account = internal_account(AccountHolder("OOBank", "AG", datetime(1997, 9, 3), 9000, "Zürich", "Paradeplatz 8"), "internal_account", "Bookkeeping")
        #Am Paradeplatz wird anscheinend ein Plätzchen frei, perfekt für unsere OOBank :D            
        self.accounts.append(self.bookkeeping_account)

        self.cash_account = internal_account(AccountHolder("OOBank", "AG", datetime(1997, 9, 3), 9000, "Zürich", "Paradeplatz 8"), "internal_account", "Cash Account")
        self.accounts.append(self.cash_account)

        #Bookkeeping = internes Konto zur Gebührenverrechnung
        #Cash Account = internes Konto zur Verrechnung von Bargeldeinzahlungen, z.B. am Schalter


    def open_account(self, first_name, last_name, date_of_birth, plz, city, address, account_type, account_name):
        account_holder = AccountHolder(first_name, last_name, date_of_birth, plz, city, address)
        self.account_holders.append(account_holder)

        if account_type == "private" and not account_holder.young_person:
            account = private_account(account_holder, account_type, account_name)
        elif account_type == "youth" and account_holder.young_person:
            account = youth_account(account_holder, account_type, account_name)
        elif account_type == "savings" and not account_holder.young_person:
            account = savings_account(account_holder, account_type, account_name)
        else:
            print("This person cannot open the desired accout. Check if they're old enough/too young.")
            self.account_holders.remove(account_holder)
            del account_holder
            return

        self.accounts.append(account)
        account_holder.count_of_accounts += 1
        print("\nAccount opened up successfully!")

    def create_additional_account(self, account_holder_id, account_type, account_name):
        for account_holder in self.account_holders:
            if account_holder.account_holder_id == account_holder_id:
                if account_type == "private":
                    account = private_account(account_holder, account_type, account_name)
                elif account_type == "youth":
                    account = youth_account(account_holder, account_type, account_name)
                elif account_type == "savings":
                    account = savings_account(account_holder, account_type, account_name)

                self.accounts.append(account)
                account_holder.count_of_accounts += 1
                break
        else:
            print("Account holder not found. Try with new account holder id.")

    def close_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                account_holder = account.account_holder  # Retrieve the account holder from the account
                self.accounts.remove(account)
                del account
                account_holder.count_of_accounts -= 1
                if account_holder.count_of_accounts == 0:
                    self.account_holders.remove(account_holder)
                    del account_holder
                break

    def close_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                account_holder = account.account_holder
                if account.balance == 0:
                    self.accounts.remove(account)
                    del account
                    print("Account has been deleted.")

                    account_holder_accounts = [acc for acc in self.accounts if acc.account_holder == account_holder]
                    if len(account_holder_accounts) == 0:
                        self.account_holders.remove(account_holder)
                        del account_holder    
                        print("As this was the last account of the account holder, the account holder was deleted too.")
                        return
                    
                else:
                    print("Account balance is not 0.00.")      
                    return     
        print("Account not found.")

    @classmethod
    def get_account(cls, num):
        for account in cls.accounts:
            if account.account_number == num:
                return account
        else: 
            return None
            
    @classmethod
    def get_account_holder(cls, num):
        for account_holder in cls.account_holders:
            if account_holder.account_holder_id == num:
                return account_holder
        return None

    def print_account_holders(self):
        for account_holder in self.account_holders:
            print("Account Holder: {} {} Account Holder ID: {}".format(account_holder.first_name, account_holder.last_name, account_holder.account_holder_id))
            print("Accounts:")
            for account in self.accounts:
                if account.account_holder == account_holder:
                    account_type = type(account).__name__
                    print("- Account Type: {}, Account Name: {}, Account Number {}, Balance: {}".format(
                        account_type, account.account_name, account.account_number, account.balance))
            print()

class AccountHolder:
    def __init__(self, first_name, last_name, date_of_birth, plz, city, address):


        birthday = date(date_of_birth.year, date_of_birth.month, date_of_birth.day)
        self.young_person = birthday >= date.today() - timedelta(days=365 * 18)

        while True:
            rand_int = np.random.randint(1, 100000)
            if Bank.get_account_holder(rand_int) is None: # Now you can call it like this
                self.account_holder_id = rand_int
                break
                    

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.plz = plz
        self.city = city
        self.address = address
        self.count_of_accounts = 0

class Account:
    def __init__(self, account_holder, account_type, account_name):

        rand_int = np.random.randint(1, 100000)
        while rand_int > 0:
            rand_int = np.random.randint(1, 100000)
            if Bank.get_account(rand_int) == None:
                break

        self.account_number = rand_int
        self.account_holder = account_holder
        self.account_type = account_type 
        self.account_name = account_name

        self.balance = 0
        self.overdraft_limit = 0
        self.interest_rate = 1.00
        self.domestic_incoming_fee = 1.0
        self.domestic_outgoing_fee = 1.25
        self.international_incoming_fee = 5.00
        self.international_outgoing_fee = 2.50

    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        self.balance -= amount

class private_account(Account):
    def __init__(self, account_holder, account_type, account_name):
        super().__init__(account_holder, account_type, account_name)
        self.overdraft_limit = 1000    

class youth_account(Account):
    def __init__(self, account_holder, account_type, account_name):
        super().__init__(account_holder, account_type, account_name)
        self.domestic_incoming_fee = 0.00
        self.domestic_outgoing_fee = 0.00
        self.international_incoming_fee = 0.00
        self.international_outgoing_fee = 0.00
        self.interest_rate = 1.25

class savings_account(Account):
    def __init__(self, account_holder, account_type, account_name):
        super().__init__(account_holder, account_type, account_name)
        self.domestic_incoming_fee = 0.00
        self.domestic_outgoing_fee = 0.00
        self.international_incoming_fee = 0.00
        self.international_outgoing_fee = 0.00
        self.interest_rate = 1.5

class internal_account(Account):
    def __init__(self, account_holder, account_type, account_name):
        super().__init__(account_holder, account_type, account_name)
        self.balance = 0
        self.overdraft_limit = -float("inf") 
        self.interest_rate = 0.00
        self.domestic_incoming_fee = 0.00
        self.domestic_outgoing_fee = 0.00
        self.international_incoming_fee = 0.00
        self.international_outgoing_fee = 0.00