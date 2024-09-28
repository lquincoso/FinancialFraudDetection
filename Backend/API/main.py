from flask import Flask, jsonify, request

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

# Example POST route
@app.route('/api/data', methods=['POST'])
def create_data():
    new_data = request.get_json()  # Get the data from the request body
    return jsonify(new_data), 201  # Return the new data with a 201 status code

if __name__ == "__main__":
    app.run(port=8080, debug=True)
