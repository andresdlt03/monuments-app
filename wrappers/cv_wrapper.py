from fastapi import FastAPI
import uvicorn
from base import Wrapper
import csv
import io

class WrapperCV(Wrapper):
    def get_data(self) -> dict:
        csv_data = io.StringIO(self.txt)
        reader = csv.DictReader(csv_data,delimiter=';')
        rows = list(reader)
        self.rows = rows
        return rows
    
api = FastAPI()

@api.get("/cv/")
async def get_data():
    with open('./data-sources/bienes_inmuebles_interes_cultural (comunitat valenciana).csv', 'r') as f:
        txt = f.read()
        wrapper = WrapperCV(txt)
        return wrapper.get_data()

uvicorn.run(api, host='127.0.0.1', port=8001)