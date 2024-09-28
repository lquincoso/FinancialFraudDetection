from flask import Flask, jsonify, request
from db import get_transaction_by_nameOrig
app = Flask(__name__)

# Sample route to check if the API is working
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

# Example GET route
@app.route('/api/data', methods=['GET'])
def get_data():

    data = {
        "id": 1,
        "name": "Sample Data",
        "description": "This is a sample API response"
    }
    return jsonify(data)

@app.route('/api/transaction', methods=['GET'])
def allTransactions():
    nameOrig = request.args.get('nameOrig')
    transaction = get_transaction_by_nameOrig(nameOrig)
    if transaction:
        return jsonify(transaction), 200
    else:
        return jsonify({"error": "nameOrig is not valid"}), 400
if __name__ == "__main__":
    # change host to own IP address
    app.run(host='10.108.94.53', port=5000, debug=True, threaded=False)