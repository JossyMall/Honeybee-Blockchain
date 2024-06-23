# transaction.py

from blockchain import Blockchain

class TransactionVerifier:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def verify_transaction(self, farmer_id: str, amount: int) -> Optional[int]:
        """
        Verify a new transaction before adding it to the blockchain
        :param farmer_id: <str> ID of the farmer
        :param amount: <int> Amount of honey produced (in liters)
        :return: <int> Index of the block that will hold this transaction, None if verification fails
        """
        if not self.blockchain.is_registered_farmer(farmer_id):
            return None  # Farmer not registered

        # Other verification logic can be added here

        return self.blockchain.new_transaction(farmer_id, amount)
