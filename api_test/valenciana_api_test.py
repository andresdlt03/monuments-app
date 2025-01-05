import requests

valenciana_url = "../data-sources/bienes_inmuebles_interes_cultural (comunitat valenciana).csv"

with open(valenciana_url, 'r', encoding='utf-8') as f: 
    valenciana_to_parse = f.read()

VALENCIANA_API_URL = 'http://127.0.0.1:8002'
response = requests.post(VALENCIANA_API_URL + '/get_json', json={'data' : valenciana_to_parse})
print(response.text)