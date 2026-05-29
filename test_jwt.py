import requests
import json

url = 'http://127.0.0.1:8000/api/token/'
data = {'username': 'admin', 'password': '0205038008Dott'}

response = requests.post(url, json=data)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    print('✅ JWT Token received:')
    tokens = response.json()
    print(f'Access Token (first 100 chars): {tokens["access"][:100]}...')
    print(f'Refresh Token (first 100 chars): {tokens["refresh"][:100]}...')
    print('\nFull Response:')
    print(json.dumps(tokens, indent=2))
else:
    print('Response:', response.json())
