from uuid import uuid4

from utility.verification import Verification
from blockchain import BlockChain
from wallet import Wallet


class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = BlockChain(self.wallet.public_key)

    def get_transaction_value(self):
        """ Returns the input of the user ( a new transaction amount) as float. """

        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount please: "))
        return tx_recipient, tx_amount

    def print_blockchain_element(self):
        """Out the blockchain list in the terminal"""
        for block in self.blockchain.get_chain():
            print("Displaying Block")
            print(block)

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
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: save wallet keys ")
            print("q: Quit")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print('Added Transaction')
                else:
                    print('Transaction Failed')
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet')

            elif user_choice == "3":
                self.print_blockchain_element()

            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = BlockChain(self.wallet.public_key)
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = BlockChain(self.wallet.public_key)

            elif user_choice == "7":
                if self.wallet.public_key != None and self.wallet.private_key != None:
                    self.wallet.save_keys()
            elif user_choice == "q":
                waiting_for_input = False

            else:
                print("Invalid input. Please select a value from the list")
            if not Verification.verify_chain(self.blockchain.get_chain()):
                print("Invalid blockchain")
                break
            print(
                f'Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}')
        else:
            print("User left")

        print('Done')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
