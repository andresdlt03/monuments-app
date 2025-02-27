from fastapi import FastAPI
from bs4 import BeautifulSoup as b
import uvicorn

class WrapperCLE():

    def __init__(self,txt):
        self.txt = txt
		
    def get_data(self) -> dict:
        data = self.txt
        bs =  b(data, 'xml')
        json_parsed = []
        tags = bs.find_all('monumento')
        for monument in tags:
            monument_parsed = {}
            for tag_content in monument.contents:
                if tag_content != '\n':
                    if len(tag_content.contents) > 1:
                        monument_parsed.update({tag_content.name : self.update_dict(tag_content)})
                    else:
                        monument_parsed.update({tag_content.name : tag_content.text})
            json_parsed.append(monument_parsed)
        return json_parsed

    def update_dict(self,tag) -> dict:
        tag_dict = {}
        for subtag in tag.contents:
            if subtag != '\n':
                if len(subtag.contents) > 1:
                    tag_dict.update(self.update_dict(subtag))
                else:
                    tag_dict.update({subtag.name : subtag.text})
        return tag_dict

api = FastAPI()

@api.get("/cle/")
async def get_data():
    with open('monumentos (castilla y leon).xml', 'r',encoding='utf-8') as f:
        txt = f.read()
        wrapper = WrapperCLE(txt)
        return wrapper.get_data()

uvicorn.run(api, host='127.0.0.1', port=8001)
