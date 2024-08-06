import requests
import json

url = "http://52.66.239.27:8504/get_keys"
headers = {"Content-Type": "application/json"}
data = {"email": "surenichith1234567@gmail.com.com"}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("API Key:", response.json())
else:
    print("Failed to retrieve API key. Status code:", response.status_code)