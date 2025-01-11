import requests

url = "http://127.0.0.1:8000/predict_home_price"
data = {
    'total_sqft': 1000,
    'location': '1st Phase JP Nagar',
    'bhk': 2,
    'bath': 2
}

# Send the data as JSON in the POST request
response = requests.post(url, json=data)

# Print the JSON response from the server
print(response.json())

