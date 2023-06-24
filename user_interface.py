from oop import Bank, Account, AccountHolder
from bookkeeping import BookingSystem
from datetime import date, datetime, timedelta

bank = Bank()
booking_system = BookingSystem(bank)

bank.open_account("Emma", "Davis", datetime(1991, 3, 5), "13579", "City", "Lane", "private", "Emma's Personal Account")
bank.open_account("Michael", "Wilson", datetime(2000, 9, 15), "24680", "Town", "Street", "youth", "Michael's Youth Account")
bank.open_account("Sophia", "Lee", datetime(1994, 7, 20), "98765", "City", "Avenue", "private", "Sophia's Personal Account")
bank.open_account("Daniel", "Thomas", datetime(1999, 11, 18), "56789", "Town", "Road", "youth", "Daniel's Youth Account")
bank.open_account("Olivia", "Brown", datetime(1993, 2, 25), "34567", "City", "Lane", "private", "Olivia's Personal Account")
bank.open_account("William", "Taylor", datetime(2010, 6, 10), "87654", "Town", "Street", "youth", "William's Youth Account")
bank.open_account("Ava", "Martinez", datetime(1997, 9, 3), "98765", "City", "Avenue", "private", "Ava's Personal Account")
bank.open_account("James", "Garcia", datetime(2002, 8, 12), "43210", "Town", "Road", "youth", "James's Youth Account")
bank.open_account("Isabella", "Clark", datetime(2016, 5, 21), "56789", "City", "Lane", "private", "Isabella's Personal Account")
bank.open_account("Ethan", "Anderson", datetime(2003, 12, 8), "12345", "Town", "Street", "youth", "Ethan's Youth Account")

bank.print_account_holders()
bank.get_account(123)

def run_interface():
    while True:
        print("OOBank's Booking System:")
        print("1. Print all Account")
        print("2. Open a new Account")
        print("3. Create an additional Account")
        print("4. Close an Account")
        print("5: Make a Deposit (Cash or Virtually)")
        print("6: Enter a Payment to another Account")
        print("7. Retrieve account balance")
        print("8. Retrieve last payments")
        print("9. ADMIN ACCESS: Retrieve all payments")
        print("10. Quit")

        choice = input("Enter your choice (1-10): ")

        if choice == "1":
            print("All Accounts:")
            bank.print_account_holders()
        if choice == "2":
            print("Open a New Account")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            date_of_birth_str = input("Date of Birth (YYYY-MM-DD): ")
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
            plz = input("PLZ: ")
            city = input("City: ")
            address = input("Address: ")
            account_type = input("Account Type (private/youth/savings): ")
            account_name = input("Account Name: ")

            bank.open_account(first_name, last_name, date_of_birth, plz, city, address, account_type, account_name)

        elif choice == "3":
            print("Open an additional account")
            account_holder_id = int(input("Account Holder ID: "))
            account_type = input("Account Type (private/youth/savings): ")
            account_name = input("Account Name: ")
            
            try:
                bank.create_additional_account(account_holder_id, account_type, account_name)
            except Exception:
                pass

            print("\nAdditional account opened successfully!")
            
        elif choice == "4":
            print("Close an Account")
            account_number = int(input("Account Number: "))
            print(bank.close_account(account_number))

        elif choice == "5":
            print("Make a deposit (Cash or Virtually).")

            cash_virtual = input("Choose 'Cash' for Cash and 'Virtual' for a Bank Payment: ")

            if cash_virtual == "Cash":
                account_number = int(input("Enter the Beneficiary Account Number: "))
                amount = float(input("Enter the Amount to deposit: "))
                message = input("Enter a message (Optional): ")
                print(booking_system.cash_deposit(account_number, amount, message))
            
            elif cash_virtual == "Virtual":
                account_number = int(input("Enter the Beneficiary Account Number: "))
                amount = float(input("Enter the Amount to deposit: "))
                message = input("Enter a message (Optional): ")
                debitor_account = int(input("Enter the Sender's Account Number (int): "))
                debitor_name = input("Enter the Sender's Name: ")
                print(booking_system.virtual_deposit(account_number, amount, message, debitor_account, debitor_name))
            else:
                print("\nWrong format!")       

        elif choice == "6":
            print("Enter a payment to another account.")
            creditor = int(input("Enter the Beneficiary Account Number: "))
            debitor = int(input("Enter the Sender's Account Number: "))
            amount = float(input("Enter the Amount to send: "))
            message = input("Enter a message (Optional): ")
            print(booking_system.internal_payment(debitor, creditor, message, amount))

        elif choice == "7":
            print("Retrieve account balance.")
            num = int(input("Enter the desired Account Number: "))
            print(f'\nThe current balance on your account is {bank.get_account(num).balance} CHF')
        
        elif choice == "8":
            print("Retrieve last payments.")
            account_number = int(input("Enter the desired Account Number: "))
            num = int(input("Enter the desired # of Entries: "))
            print(booking_system.list_transactions(account_number, num))

        elif choice == "9":
            print("Retrieve last payments.")
            num = int(input("Enter the desired # of Entries: "))
            print(booking_system.list_transactions(None, num))        

        elif choice == "10":
            print("\nThank you for using OOBank's booking system.")
            break
        else:
            print("\nInvalid choice. Please try again.")
        print()

run_interface()