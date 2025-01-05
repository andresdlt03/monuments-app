from base import Wrapper, TxtModel
from fastapi import FastAPI
import uvicorn
import json

class WrapperMUR(Wrapper):
    def get_data(self) -> dict:
        self.txt = self.txt.replace('''"address" : "",''','')
        self.txt = self.txt.replace('''"phone" : "",''','')

        return json.loads(self.txt)

app = FastAPI(debug=True,title="Euskadi Wrapper", description="Wrapper para la fuente de datos de Euskadi", version="1.0")

@app.post("/get_json")
async def get_json(txt : TxtModel) -> dict:
    euskadi_wrapper = WrapperMUR(txt.data)
    euskadi_json = euskadi_wrapper.get_data()
    return euskadi_json

uvicorn.run(app, host="127.0.0.1",port=8000)