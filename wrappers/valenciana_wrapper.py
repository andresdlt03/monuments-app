from base import Wrapper, TxtModel
from fastapi import FastAPI
import uvicorn
import csv
import io

class WrapperCV(Wrapper):
    def get_data(self) -> dict:
        csv_data = io.StringIO(self.txt)
        reader = csv.DictReader(csv_data,delimiter=';')
        rows = list(reader)
        self.rows = rows
        return rows
    
    def get_types(self) -> list:
        se = set()
        for row in self.rows:
            se.add(row['DENOMINACION'].split(' ')[0])
        return list(se)

app = FastAPI(debug=True,title="Valenciana Wrapper", description="Wrapper para la fuente de datos de Valenciana", version="1.0")

@app.post("/get_json")
async def get_json(txt : TxtModel):
    valenciana_wrapper = WrapperCV(txt.data)
    valenciana_json = valenciana_wrapper.get_data()
    return valenciana_json

uvicorn.run(app, host="127.0.0.1",port=8002)