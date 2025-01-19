from fastapi import FastAPI
import uvicorn
import json
import os

cwd = os.getcwd()

class WrapperMUR():
    
    def __init__(self,txt):
        self.txt = txt
	
    def get_data(self) -> dict:
        self.txt = self.txt.replace('''"address" : "",''','')
        self.txt = self.txt.replace('''"phone" : "",''','')
        return json.loads(self.txt)

api = FastAPI()

@api.get("/mur/")
async def get_data():
    with open(os.path.join(cwd,'edificios.json'), 'r',encoding='utf-8') as f:
        txt = f.read()
        wrapper = WrapperMUR(txt)
        return wrapper.get_data()

uvicorn.run(api, host='127.0.0.1', port=8003)