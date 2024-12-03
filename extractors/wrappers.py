from abc import abstractmethod
from bs4 import BeautifulSoup as b
import json
import csv

class Wrapper():
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_data(self):
        pass

class Wrapper_CV(Wrapper):
    def get_data(self):
        with open(self.url, 'r',encoding='utf-8') as file:
            reader = csv.DictReader(file,delimiter=';')
            rows = list(reader)
            self.rows = rows
            return rows
        # jsondata = []
    
    def get_clasification(self):
        se = set()
        for row in self.rows:
            se.add(row['DENOMINACION'].split(' ')[0])
        return list(se)

class Wrapper_CAT(Wrapper):
    def get_data(self):
        with open(self.url, 'r',encoding='utf-8') as f:
            data = f.read()
            bs =  b(data, 'xml')
        jsondata = []
        monumentsTags = bs.find_all('monumento')
        for monument in monumentsTags:
            monumentData = {}
            for tag in monument.contents:
                if tag != '\n':
                    if len(tag.contents) > 1:
                        monumentData.update(self.update_dict(tag))
                    else:
                        monumentData.update({tag.name : tag.text})
            jsondata.append(monumentData)
        return jsondata

    def update_dict(self,tag) -> dict:
        tag_dict = {}
        for subtag in tag.contents:
            if subtag != '\n':
                if len(subtag.contents) > 1:
                    tag_dict.update(self.update_dict(subtag))
                else:
                    tag_dict.update({subtag.name : subtag.text})
        return tag_dict            

class Wrapper_MUR(Wrapper):
    def get_data(self) -> dict:
        with open(self.url,'r',encoding='utf-8') as f:
            txt = f.read()

        txt = txt.replace('''"address" : "",''','')
        txt = txt.replace('''"phone" : "",''','')

        return json.loads(txt)