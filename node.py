from verification import Verification

class Node:

    def __init__(self):
        self.blockchain = []

    def get_transaction_value(self):
        """ Returns the input of the user ( a new transaction amount) as float. """

        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount please: "))
        return tx_recipient, tx_amount

    def print_blockchain_element(self):
        """Out the blockchain list in the terminal"""
        for block in self.blockchain:
            print("Displaying Block")
            print(self.blockchain)

    def get_user_choice(self):
        user_input = input('Enter your choice: ')
        return user_input

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
        print("Please Choose")
        print("1: Add a new trasaction value")
        print("2: Mine a new block ")
        print("3: Output the blockchain blocks")
        print("4: Check transaction validity")
        print("q: Quit")
        user_choice = self.get_user_choice()
        if user_choice == "1":
            tx_data = self.get_transaction_value()
            recipient, amount = tx_data
            if add_transaction(recipient, amount=amount):
                print('Added Transaction')
            else:
                print('Transaction Failed')
            print(open_transactions)
        elif user_choice == "2":
            if mine_block():
                open_transactions = []
                save_data()
                print(' Balance of {}: {:6.2f}'.format(
                    'Swill', get_balance('Swill')))
        elif user_choice == "3":
            self.print_blockchain_element()

        elif user_choice == "4":
            verifier = Verification()
            if verifier.verify_transactions(open_transactions, get_balance):
                print("All transactions are valid")
            else:
                print("There are invalid transactions")
        elif user_choice == "q":
            waiting_for_input = False

        else:
            print("Invalid input. Please select a value from the list")
        verifier = Verification()
        if not verifier.verify_chain(self.blockchain):
            print("Invalid blockchain")
            break
    else:
        print("User left")

    print('Done')
