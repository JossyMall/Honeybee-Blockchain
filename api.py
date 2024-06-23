# api.py

from flask import Flask, jsonify, request
from blockchain import Blockchain, TransactionVerifier, ConsensusMechanism
from farmer import FarmerRegistry
from token import TokenManager

app = Flask(__name__)
blockchain = Blockchain()
transaction_verifier = TransactionVerifier(blockchain)
consensus_mechanism = ConsensusMechanism(blockchain)
farmer_registry = FarmerRegistry(blockchain)
token_manager = TokenManager(blockchain)

@app.route('/mine', methods=['GET'])
def mine_block():
    miner_id = request.args.get('miner_id')
    if not miner_id:
        return jsonify({'message': 'Miner ID not provided'}), 400
    new_block = consensus_mechanism.mine_block(miner_id)
    response = {
        'message': 'New block mined',
        'block': new_block
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required_fields = ['farmer_id', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields in transaction data
}), 400

    farmer_id = data['farmer_id']
    amount = data['amount']

    result = transaction_verifier.verify_transaction(farmer_id, amount)
    if result is None:
        return jsonify({'message': 'Invalid transaction or farmer not registered'}), 400

    response = {
        'message': f'Transaction will be added to Block {result}',
        'farmer_id': farmer_id,
        'amount': amount,
    }
    return jsonify(response), 201

@app.route('/farmers/register', methods=['POST'])
def register_farmer():
    data = request.get_json()
    farmer_id = data.get('farmer_id')
    if not farmer_id:
        return jsonify({'message': 'Farmer ID not provided'}), 400

    success = farmer_registry.register_farmer(farmer_id)
    if not success:
        return jsonify({'message': 'Farmer already registered'}), 400

    return jsonify({'message': 'Farmer registered successfully'}), 201

@app.route('/farmers', methods=['GET'])
def get_farmers():
    farmers = list(farmer_registry.get_registered_farmers())
    return jsonify({'farmers': farmers}), 200

@app.route('/tokens/mint', methods=['GET'])
def mint_tokens():
    tokens_minted = token_manager.mint_tokens()
    return jsonify({'message': f'Tokens minted: {tokens_minted}'}), 200

@app.route('/tokens/balance/<farmer_id>', methods=['GET'])
def get_token_balance(farmer_id):
    token_balance = token_manager.get_token_balance(farmer_id)
    return jsonify({'farmer_id': farmer_id, 'token_balance': token_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
