from base import Wrapper, TxtModel
from bs4 import BeautifulSoup as b
from fastapi import FastAPI
import uvicorn

class WrapperCLE(Wrapper):
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
                        monument_parsed.update(self.update_dict(tag_content))
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

app = FastAPI(debug=True,title="Castilla Wrapper", description="Wrapper para la fuente de datos de Castilla", version="1.0")

@app.post("/get_json")
async def get_json(txt : TxtModel):
    castilla_wrapper = WrapperCLE(txt.data)
    castilla_json = castilla_wrapper.get_data()
    return castilla_json

uvicorn.run(app, host="127.0.0.1",port=8001)