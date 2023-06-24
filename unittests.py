import unittest
import datetime
from unittest.mock import patch
from io import StringIO
import user_interface  # assuming user_interface.py contains the classes and the function to be tested

class TestUserInterface(unittest.TestCase):

    # Setup
    def setUp(self):
        self.bank = user_interface.Bank()
        self.booking_system = user_interface.BookingSystem(self.bank)

    # Test for printing account holders
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_account_holders(self, mock_stdout):
        self.bank.print_account_holders()
        self.assertEqual(mock_stdout.getvalue(), 'Expected output')

    # Test for opening a new account
    @patch('builtins.input', side_effect=['Emma', 'Davis', '1991-03-05', '13579', 'City', 'Lane', 'private', "Emma's Personal Account"])
    def test_open_account(self, mock_input):
        self.bank.open_account('Emma', 'Davis', datetime(1991, 3, 5), '13579', 'City', 'Lane', 'private', "Emma's Personal Account")
        self.assertEqual(self.bank.get_account(1).first_name, 'Emma')

    # Similarly, you can add other tests...

if __name__ == '__main__':
    unittest.main()
