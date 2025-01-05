from abc import abstractmethod
from bs4 import BeautifulSoup as b
import csv
import json

class Wrapper():
    def __init__(self, url : str):
        self.url = url
        self.encoding = 'utf-8'

    @abstractmethod
    def get_data(self):
        pass

class WrapperEuskadi(Wrapper):
    def get_data(self) -> dict:
        with open(self.url,'r',encoding=self.encoding) as f:
            txt = f.read()

        txt = txt.replace('''"address" : "",''','')
        txt = txt.replace('''"phone" : "",''','')

        return json.loads(txt)
    
class WrapperCastilla(Wrapper):
    def get_data(self) -> dict:
        with open(self.url, 'r',encoding=self.encoding) as f:
            data = f.read()
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

class WrapperValenciana(Wrapper):
    def get_data(self) -> dict:
        with open(self.url, 'r',encoding=self.encoding) as f:
            reader = csv.DictReader(f,delimiter=';')
            rows = list(reader)
            self.rows = rows
            return rows
    
    def get_types(self) -> list:
        se = set()
        for row in self.rows:
            se.add(row['DENOMINACION'].split(' ')[0])
        return list(se)