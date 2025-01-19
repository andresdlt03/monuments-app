from fastapi import FastAPI
import uvicorn
import csv
import io

class WrapperCV():

    def __init__(self,txt):
        self.txt = txt
		
    def get_data(self) -> dict:
        csv_data = io.StringIO(self.txt)
        reader = csv.DictReader(csv_data,delimiter=';')
        rows = list(reader)
        self.rows = rows
        return rows
    
api = FastAPI()

@api.get("/cv/")
async def get_data():
    with open('bienes_inmuebles_interes_cultural (comunitat valenciana).csv', 'r',encoding='utf-8') as f:
        txt = f.read()
        wrapper = WrapperCV(txt)
        return wrapper.get_data()

uvicorn.run(api, host='127.0.0.1', port=8002)