import functools
import json
import pickle

from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction

owner = "Swill"
MINING_REWARD = 10
blockchain = []

def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]

    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    tx_sender_amount = [amount[0] for amount in tx_sender if len(amount) > 0]
    amount_sent = functools.reduce(lambda a, b: a + b, tx_sender_amount, 0)

    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant] for block in blockchain]
    tx_recipient_amount = [amount[0]
                           for amount in tx_recipient if len(amount) > 0]
    amount_recieved = functools.reduce(
        lambda a, b: a + b, tx_recipient_amount, 0)

    return amount_recieved - amount_sent


def load_data():
    try:
        with open("blockchain.p", mode="rb") as f:
            file_content = pickle.loads(f.read())
            global blockchain
            global open_transactions
            blockchain = file_content['chain']
            open_transactions = file_content['ot']

    except IOError:
        genesis_block = Block(0, "", [], 1000, 0)
        blockchain = [genesis_block]
        open_transactions = []
        print("file not found")


def save_data():
    try:
        with open("blockchain.p", mode="wb") as f:
            save_data = {
                'chain': blockchain,
                'ot': open_transactions,
            }
            f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed')

load_data()


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == '11'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def add_transaction(recipient, sender=owner, amount=1.0):
    """Append a new value as wekk as the last blockchain
    value to the blockchain

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :last_transaction: The amount of coins sent with the transaction (defaults [1])"""
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def get_user_choice():
    user_input = input('Enter your choice: ')
    return user_input


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('Mining', owner, MINING_REWARD)
    copied_transaction = open_transactions[:]
    open_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, open_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user ( a new transaction amount) as float. """

    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount please: "))
    return tx_recipient, tx_amount


def print_blockchain_element():
    """Out the blockchain list in the terminal"""
    for block in blockchain:
        print("Displaying Block")
        print(blockchain)

def verify_chain():
    """Verify the current blockchain and return True
     if it's valid. False is returned if the value is invalid"""

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print("Please Choose")
    print("1: Add a new trasaction value")
    print("2: Mine a new block ")
    print("3: Output the blockchain blocks")
    print("4: Check transaction validity")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
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
        print_blockchain_element()
   
    elif user_choice == "4":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "q":
        waiting_for_input = False
    
    else:
        print("Invalid input. Please select a value from the list")
    if not verify_chain():
        print("Invalid blockchain")
        break
else:
    print("User left")
