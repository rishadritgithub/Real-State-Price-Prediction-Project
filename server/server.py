from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the artifacts when the server starts
util.load_saved_artifacts()

@app.route('/')
def home():
    return "Welcome to the Home Price Prediction API!"

@app.route('/get_location_names')
def get_location_names():
    locations = util.get_location_names()
    response = jsonify({
        'locations': locations
    })
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()
        print(f"data: {data}")
        if not data or 'total_sqft' not in data or 'location' not in data or 'bhk' not in data or 'bath' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])
        # print(f"total_sqrt: {total_sqft}, location:{location}, bhk:{bhk}, bath:{bath}")

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        # print(f"estimated_price:{estimated_price}")
        
        if estimated_price is None:
            return jsonify({"error": "Unable to predict price. Please check if location exists and all inputs are valid"}), 400

        response = jsonify({'estimated_price': estimated_price})
        return response

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(debug=True, port=8000)