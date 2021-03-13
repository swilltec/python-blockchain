blockchain = [[1]]


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    """Append a new value as wekk as the last blockchain
    value to the blockchain

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (defaults [1])"""
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_user_choice():
    user_input = input('Enter your choice: ')
    return user_input


def get_transaction_value():
    """ Returns the input of the user ( a new transaction amount) as float. """

    user_input = float(input('Enter your transactio amount please: '))
    return user_input


def print_blockchain_element():
    """Out the blockchain list in the terminal"""
    for block in blockchain:
        print("Displaying Block")
        print(blockchain)


def edit_first_transaction(value):
    if len(blockchain) >= 1:
        blockchain[0] = [value]


def verify_chain():
    block_index = 0

    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid


while True:
    print("Please Choose")
    print("1: Add a new trasaction value")
    print("2: Output the blockchain blocks")
    print("h: alter blockchain transaction")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        print_blockchain_element()
    elif user_choice == "q":
        break
    elif user_choice == "h":
        edit_first_transaction([123])
    else:
        print("Invalid input. Please select a value fro the list")
    if not verify_chain():
        print("Invalid blockchain")
        break
