import datetime
from flask import Flask, jsonify, request
from db import get_transaction_by_nameOrig, get_transactions_in_blocks,create_transaction
from predictions import predict_fraud
app = Flask(__name__)

# Sample route to check if the API is working
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

# GET route to get a transaction by nameOrig
@app.route('/api/transaction', methods=['GET'])
def getByNameOrig():
    nameOrig = request.args.get('nameOrig')
    # get the transaction by nameOrig from the database
    transaction = get_transaction_by_nameOrig(nameOrig)
    if transaction:
        return jsonify(transaction), 200
    else:
        return jsonify({"error": "nameOrig is not valid"}), 400
    

# GET route to get all transactions in blocks of 10
@app.route('/api/transactions', methods=['GET'])
def getTransactionsByPage():
    pageNum = request.args.get('pageNum')
    if not pageNum:
        return jsonify({"error": "pageNum is required"}), 400
    # get all the transaction in a page from the database
    transactions = get_transactions_in_blocks(pageNum)
    if transactions:
        return jsonify(transactions), 200
    else:
        return jsonify({"error": "no transactions found"}), 400


# create new transaction
@app.route('/api/transaction', methods=['POST'])
def createTransaction():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    
    nameOrig = data.get('nameOrig')
    steps = data.get('steps')
    type = data.get('type')
    amount = data.get('amount')
    oldbalanceOrg = data.get('oldbalanceOrg')
    newbalanceOrig = data.get('newbalanceOrig')
    nameDest = data.get('nameDest')
    oldbalanceDest = data.get('oldbalanceDest')
    newbalanceDest = data.get('newbalanceDest')
    isflaggedFraud = data.get('isflaggedFraud')
    # create a new transaction object
    new_transaction = {
        "nameOrig": nameOrig,
        "steps": steps,
        "type": type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "nameDest": nameDest,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "isflaggedFraud": isflaggedFraud
    }
    

    # send transaction to model
    prediction = predict_fraud(new_transaction)
    new_transaction['isfraud'] = bool(prediction[0])
    create_transaction(new_transaction)
    return jsonify(new_transaction), 201


if __name__ == "__main__":
    # change host to own IP address or remove for localhost
    app.run(port=5000, debug=True, threaded=False)