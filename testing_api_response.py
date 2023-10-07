import requests

# Define the API endpoint and request data (body)
url = 'http://127.0.0.1:5000/'
data = {
    "fixed_acidity": 5, 
    "volatile_acidity": 1, 
    "citric_acid": 0.5, 
    "residual_sugar": 10, 
    "chlorides": 0.5, 
    "free_sulfur_dioxide": 3, 
    "total_sulfur_dioxide": 75, 
    "density": 1, 
    "pH": 3, 
    "sulphates": 1, 
    "alcohol": 9
}

# Make the POST request
response = requests.post(url, json=data)  # You can also use data=data if sending form data

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse and print the response content (assuming it's JSON)
    response_data = response.json()
    print(response_data)
else:
    # Handle errors
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
