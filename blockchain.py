genesis_block = {
        'previous_hash': "",
        "index": 0,
        "transaction": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Swill"


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """Append a new value as wekk as the last blockchain
    value to the blockchain

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :last_transaction: The amount of coins sent with the transaction (defaults [1])"""

    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount":amount
        }
    
    open_transactions.append(transaction)


def get_user_choice():
    user_input = input('Enter your choice: ')
    return user_input

def mine_block():
    last_block = blockchain[-1]
    block = {
        'previous_hash': "zyx",
        "index": len(blockchain),
        "transaction": open_transactions
    }


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


def edit_first_transaction(value):
    if len(blockchain) >= 1:
        blockchain[0] = [value]


def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print("Please Choose")
    print("1: Add a new trasaction value")
    print("2: Output the blockchain blocks")
    print("h: alter blockchain transaction")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        print_blockchain_element()
    elif user_choice == "q":
        waiting_for_input = False
    elif user_choice == "h":
        edit_first_transaction([123])
    else:
        print("Invalid input. Please select a value fro the list")
    if not verify_chain():
        print("Invalid blockchain")
        break
else:
    print("User left")