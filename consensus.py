# consensus.py

from blockchain import Blockchain

class ConsensusMechanism:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def mine_block(self, miner_id: str) -> Dict[str, any]:
        """
        Mine a new block on the blockchain
        :param miner_id: <str> ID of the miner (validator)
        :return: <dict> New block
        """
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)
        previous_hash = self.blockchain.hash(last_block)

        # Create new block
        block = self.blockchain.new_block(proof, previous_hash)

        return block
