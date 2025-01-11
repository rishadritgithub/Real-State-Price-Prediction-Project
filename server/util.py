import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def normalize_location(location):
    return location.strip().lower()

def get_estimated_price(location, sqft, bhk, bath):
    if location is None or sqft is None or bhk is None or bath is None:
        print("Invalid input values received.")
        return None  # Handle invalid input gracefully

    location = normalize_location(location)
    print(f"Predicting for location: {location}, sqft: {sqft}, bhk: {bhk}, bath: {bath}")
    
    try:
        # Ensure __data_columns is properly loaded
        if __data_columns is None:
            print("Error: __data_columns is not loaded correctly.")
            return None
        
        # Ensure location index is found before using it
        loc_index = -1  # Default to -1 if not found
        try:
            loc_index = __data_columns.index(location.lower())
        except ValueError:
            print(f"Location {location} not found in columns.")

        # Create the feature vector
        x = np.zeros(len(__data_columns))
        x[0], x[1], x[2] = sqft, bath, bhk
        
        if loc_index >= 0:
            x[loc_index] = 1  # Only set the location index if it's found

        # Predict and return the estimated price
        return round(__model.predict([x])[0], 2)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts...starts")
    global __data_columns
    global __locations

    try:
        # Load data columns
        with open("./artifacts/columns.json", 'r') as f:
            data = json.load(f)
            __data_columns = data['data_columns']
            __locations = __data_columns[3:]  # Extract locations after the first 3 columns
            print(f"Loaded columns: {__data_columns}")
            print(f"Loaded locations: {__locations}")
    except Exception as e:
        print(f"Error loading columns.json: {e}")

    try:
        # Load the model
        with open("./artifacts/bengaluru_house_prices_model.pickle", 'rb') as f:
            global __model
            __model = pickle.load(f)
            print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

    print("Loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Unknown Location', 1000, 2, 2))
