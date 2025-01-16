from fastapi import FastAPI
import uvicorn
from base import Wrapper
import json

class WrapperMUR(Wrapper):
    def get_data(self) -> dict:
        self.txt = self.txt.replace('''"address" : "",''','')
        self.txt = self.txt.replace('''"phone" : "",''','')
        return json.loads(self.txt)

api = FastAPI()

@api.get("/mur/")
async def get_data():
    with open('./data-sources/edificios (euskadi).json', 'r') as f:
        txt = f.read()
        wrapper = WrapperMUR(txt)
        return wrapper.get_data()

uvicorn.run(api, host='127.0.0.1', port=8002)