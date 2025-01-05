import requests

castilla_url =  "../data-sources/monumentos (castilla y leon).xml"

# INFORMATION
with open(castilla_url, 'r', encoding='utf-8') as f: 
    castilla_to_parse = f.read()

CASTILLA_API_URL = 'http://127.0.0.1:8001'
response = requests.post(CASTILLA_API_URL + '/get_json', json={'data' : castilla_to_parse})
print(response.text)