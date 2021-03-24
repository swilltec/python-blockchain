import functools
import json
import pickle

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# The Reward given to miners ( for creatig a new blockchain )
MINING_REWARD = 10


class BlockChain:
    def __init__(self, hosting_node_id):
        # Initializing our (empty) blockchain list
        genesis_block = Block(0, "", [], 1000, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.load_data()

    def get_chain(self):
        return self.__chain[:]
    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open("blockchain.p", mode="rb") as f:
                file_content = pickle.loads(f.read())
                self.__chain = file_content['chain']
                self.__open_transactions = file_content['ot']

        except IOError:
            print("Handled exceptions")

    def save_data(self):
        try:
            with open("blockchain.p", mode="wb") as f:
                save_data = {
                    'chain': self.__chain,
                    'ot': self.__open_transactions,
                }
                f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed')

    def get_balance(self):
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]

        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        tx_sender_amount = [amount[0]
                            for amount in tx_sender if len(amount) > 0]
        amount_sent = functools.reduce(lambda a, b: a + b, tx_sender_amount, 0)

        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]
        tx_recipient_amount = [amount[0]
                               for amount in tx_recipient if len(amount) > 0]
        amount_recieved = functools.reduce(
            lambda a, b: a + b, tx_recipient_amount, 0)

        return amount_recieved - amount_sent

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount, signature):
        """Append a new value as wekk as the last blockchain
        value to the blockchain

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :last_transaction: The amount of coins sent with the transaction (defaults [1])"""

        if self.hosting_node == None:
            return None
        transaction = Transaction(sender, recipient, amount, signature)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('Mining', self.hosting_node, MINING_REWARD, '')
        copied_transaction = self.__open_transactions[:]
        for tx in copied_transaction:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transaction, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block
