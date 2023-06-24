from oop import Bank, Account, AccountHolder
import numpy as np
from datetime import date, datetime, timedelta


class BookingSystem:
    def __init__(self, bank):
        self.bookinglist = []
        self.bank = bank


    def cash_deposit(self, account_number, amount, message):
        account = self.bank.get_account(account_number)

        if account != None:
            if amount > 0.05:
                self.__enter_payment("Cash Deposit", "Cash Deposit", self.bank.cash_account.account_number, 
                                self.bank.cash_account.account_holder.first_name + " " + self.bank.cash_account.account_holder.last_name, 
                                message, amount, "CHF", True, False, False)
                self.__enter_payment(self.bank.cash_account.account_number, self.bank.cash_account.account_holder.first_name + " " + self.bank.cash_account.account_holder.last_name, 
                                account.account_number, account.account_holder.first_name + " " + account.account_holder.last_name, 
                                message, amount, "CHF", False, False, False)
                return "Cash deposited!"
        else:
            return "Account not found."
    def virtual_deposit(self, account_number, amount, message, debitor_account, debitor_name):
        account = self.bank.get_account(account_number)
        if account != None:
            if amount > 0:
                self.__enter_payment(debitor_account, debitor_name, account.account_number,
                                    account.account_holder.first_name + " " + account.account_holder.last_name, message, 
                                    amount, "CHF", False, False, False)

                return "Payment received!"
        else:
            return "Account not found."

    def internal_payment(self, debitor_account, creditor_account, message, amount):
            debitor = self.bank.get_account(debitor_account)
            creditor = self.bank.get_account(creditor_account)

            print(debitor)
            print(creditor)

            if debitor and creditor != None: 
                if amount > 0:
                    print("here")
                    if debitor.balance + debitor.overdraft_limit - debitor.domestic_outgoing_fee >= amount and creditor.balance + creditor.overdraft_limit + amount >= creditor.domestic_incoming_fee:

                        #Enters the definite booking
                        self.__enter_payment(debitor.account_number, 
                        debitor.account_holder.first_name + " " + debitor.account_holder.last_name, 
                        creditor.account_number, creditor.account_holder.first_name + " " + creditor.account_holder.last_name, 
                        message, amount, "CHF", False, False, False)

                        #Subtracts the fees from both parties
                        self.__charge_fee(debitor.domestic_outgoing_fee, creditor.domestic_incoming_fee, debitor.account_number, 
                        debitor.account_holder.first_name + " " + debitor.account_holder.last_name, creditor.account_number, 
                        creditor.account_holder.first_name + " " + creditor.account_holder.last_name, message, amount, "CHF", False, False, False)
                        return f'Payment received!'

            return "Wrong format. Check your payment entry and try again."


    def __charge_fee(self, outgoing_fee, incoming_fee, debitor_account, debitor_name, creditor_account, creditor_name, message, amount, currency, 
                        is_internal, is_interest_rate_deduction, is_fee_charge):
        if outgoing_fee > 0:
            self.__enter_payment(debitor_account, 
                debitor_name, self.bank.bookkeeping_account.account_number, self.bank.bookkeeping_account.account_holder.first_name + " " +
                self.bank.bookkeeping_account.account_holder.last_name, "Payment fee", outgoing_fee, "CHF", True, False, False)
        
        if incoming_fee > 0:
            self.__enter_payment(creditor_account, 
                creditor_name, 
                self.bank.bookkeeping_account.account_number, self.bank.bookkeeping_account.account_holder.first_name + " " +
                self.bank.bookkeeping_account.account_holder.last_name, 
                "Payment fee", incoming_fee, "CHF", True, False, False)
            

    def __enter_payment(self, debitor_account, debitor_name, creditor_account, creditor_name, message, amount, currency, 
                                                                is_internal, is_interest_rate_deduction, is_fee_charge):
        payment = {
            "debitor_account": debitor_account,
            "debitor_name": debitor_name,
            "creditor_account": creditor_account,
            "creditor_name": creditor_name,
            "message": message,
            "amount": amount,
            "currency": currency,
            "is_internal": is_internal,
            "is_interest_rate_deduction": is_interest_rate_deduction,
            "is_fee_charge": is_fee_charge,
            "payment_ref": np.random.randint(1, 1000000),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        }

        self.bookinglist.append(payment)

        if self.bank.get_account(debitor_account) != None:
            self.bank.get_account(debitor_account).withdraw(amount)

        if self.bank.get_account(creditor_account) != None:
            self.bank.get_account(creditor_account).deposit(amount)


   
    def list_transactions(self, account_number=None, num_entries=None):
        filtered_bookings = self.bookinglist

        if account_number is not None:
            filtered_bookings = [payment for payment in filtered_bookings if
                                payment['debitor_account'] == account_number or
                                payment['creditor_account'] == account_number]
        
        filtered_bookings.sort(key=lambda payment: payment['timestamp'], reverse=True)

        # Limit number of entries to display if num_entries is provided
        if num_entries is not None:
            filtered_bookings = filtered_bookings[:num_entries]

        for i, payment in enumerate(filtered_bookings, 1):
            print(f"Payment #{i}:")
            print(f"\tDebitor Account: {payment['debitor_account']}")
            print(f"\tDebitor Name: {payment['debitor_name']}")
            print(f"\tCreditor Account: {payment['creditor_account']}")
            print(f"\tCreditor Name: {payment['creditor_name']}")
            print(f"\tMessage: {payment['message']}")
            print(f"\tAmount: {payment['amount']} {payment['currency']}")
            print(f"\tIs Internal: {payment['is_internal']}")
            print(f"\tIs Interest Rate Deduction: {payment['is_interest_rate_deduction']}")
            print(f"\tIs Fee Charge: {payment['is_fee_charge']}")
            print(f"\tPayment ref: {payment['payment_ref']}")
            print(f"\tTimestamp of payment: {payment['timestamp']}")
            print("\n")



