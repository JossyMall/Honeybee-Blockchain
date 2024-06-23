# blockchain.py

import hashlib
import json
from time import time
from typing import List, Dict, Optional

from utils import generate_uuid

# Define Transaction type
Transaction = Dict[str, any]

class Blockchain:
    def __init__(self):
        self.chain: List[Dict[str, any]] = []
        self.current_transactions: List[Transaction] = []
        self.farmers: set[str] = set()  # Set to store registered farmer IDs

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Dict[str, any]:
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, farmer_id: str, amount: int) -> Optional[int]:
        """
        Creates a new transaction to go into the next mined Block
        :param farmer_id: <str> ID of the farmer
        :param amount: <int> Amount of honey produced (in liters)
        :return: <int> The index of the Block that will hold this transaction, None if verification fails
        """
        if not self.is_registered_farmer(farmer_id):
            return None  # Farmer not registered

        # Other verification logic can be added here

        self.current_transactions.append({
            'farmer_id': farmer_id,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: Dict[str, any]) -> str:
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Dict[str, any]:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains 4 leading zeroes, where p is the previous proof
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_farmer(self, farmer_id: str) -> bool:
        """
        Register a new farmer on the blockchain network
        :param farmer_id: <str> Unique ID of the farmer
        :return: <bool> True if registration successful, False if farmer already registered
        """
        if farmer_id in self.farmers:
            return False
        self.farmers.add(farmer_id)
        return True

    def is_registered_farmer(self, farmer_id: str) -> bool:
        """
        Check if a farmer is registered on the blockchain network
        :param farmer_id: <str> ID of the farmer
        :return: <bool> True if registered, False otherwise
        """
        return farmer_id in self.farmers

    def get_farmers(self) -> set[str]:
        """
        Get the set of registered farmers
        :return: <set[str]> Set of farmer IDs
        """
        return self.farmers

    def get_balance(self, farmer_id: str) -> int:
        """
        Calculate the balance (total honey produced) for a farmer
        :param farmer_id: <str> ID of the farmer
        :return: <int> Total honey produced by the farmer
        """
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['farmer_id'] == farmer_id:
                    balance += tx['amount']
        return balance

    def get_chain(self) -> List[Dict[str, any]]:
        return self.chain
