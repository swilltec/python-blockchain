import functools

genesis_block = {
        'previous_hash': "",
        "index": 0,
        "transaction": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Swill"
participants = {'Max'}
MINING_REWARD = 10

def hash_block(block):
    return "-".join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transaction'] if tx['sender'] == participant ] for block in blockchain ]
    open_tx_sender = [tx["amount"] for tx in open_transactions if tx["sender"] == participant ]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) else tx_sum + 0 > 0, tx_sender, 0)
    
    tx_recipient = [[tx['amount'] for tx in block['transaction'] if tx['recipient'] == participant ] for block in blockchain ]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) else tx_sum + 0 > 0, tx_recipient, 0)
    return amount_recieved - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction["amount"]


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

    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount":amount
        }
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def get_user_choice():
    user_input = input('Enter your choice: ')
    return user_input

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        "sender": "Mining",
        "recipient": owner,
        "amount": MINING_REWARD
    }
    copied_transaction = open_transactions[:]
    open_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transaction": open_transactions
    }
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


def edit_first_transaction(value):
    if len(blockchain) >= 1:
        blockchain[0] = {
            'previous_hash': "",
            "index": 0,
            "transaction": [{"sender": "Swill", "recipient": "Joseph", "amount":100 }]
        }


def verify_chain():
    """Verify the current blockchain and return True
     if it's valid. False is returned if the value is invalid"""

    for (index, block) in enumerate(blockchain):
        if index == 0:
             continue 
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

        



waiting_for_input = True

while waiting_for_input:
    print("Please Choose")
    print("1: Add a new trasaction value")
    print("2: Mine a new block ")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: alter blockchain transaction")
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
            print(' Balance of {}: {:6.2f}'.format('Swill', get_balance('Swill')))
    elif user_choice == "3":
        print_blockchain_element()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
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