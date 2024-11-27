from abc import abstractmethod
from bs4 import BeautifulSoup as b
import json

class Wrapper():
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_data(self):
        pass

class Wrapper_CV(Wrapper):
    def get_data(self):
        with open(self.url, 'r') as file:
            self.data = file.read()

class Wrapper_CAT(Wrapper):
    def get_data(self):
        with open(self.url, 'r',encoding='utf-8') as f:
            data = f.read()
            return b(data, 'xml')

class Wrapper_MUR(Wrapper):
    def get_data(self) -> dict:
        with open(self.url,'r',encoding='utf-8') as f:
            txt = f.read()

        txt = txt.replace('''"address" : "",''','')
        txt = txt.replace('''"phone" : "",''','')

        return json.loads(txt)

