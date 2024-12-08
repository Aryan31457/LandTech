import requests
import json
import time

# Data to be sent as JSON
data = {
    "rooms": '3',
    "bathroom": '2',
    "kitchen": '3'
} 

# Target server and port
url = 'http://10.22.2.189:5000'

# Sending the POST request with the JSON data
response = requests.post(url, json=data)

# Check the response from the server
if response.status_code == 200:
    print(f"Data successfully sent: {response.text}")
else:
    print(f"Failed to send data. Status code: {response.status_code}")

# Wait for 60 seconds before fetching the data
time.sleep(60)

# Send a GET request to the same URL to fetch the exported data
# Adjust this if the server provides a different URL for fetching the exported data
fetch_response = requests.get(url)

# Check if the fetch request is successful
if fetch_response.status_code == 200:
    # Assuming the response is a JSON list of URLs
    urls = fetch_response.json()
    print("Received URLs:", urls)
else:
    print(f"Failed to fetch data. Status code: {fetch_response.status_code}")
