import requests

euskadi_url = "../data-sources/edificios (euskadi).json"

# INFORMATION
with open(euskadi_url, 'r', encoding='utf-8') as f: 
    euskadi_to_parse = f.read()

EUSKADI_API_URL = 'http://127.0.0.1:8000'
response = requests.post(EUSKADI_API_URL + '/get_json', json={'data' : euskadi_to_parse})
print(response.text)