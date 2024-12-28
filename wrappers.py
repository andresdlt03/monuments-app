from abc import abstractmethod
import json

class Wrapper():
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_data(self):
        pass

class WrapperEuskadi(Wrapper):
    def get_data(self) -> dict:
        with open(self.url, 'r', encoding = 'utf-8') as f:
            txt = f.read()
        return json.loads(txt)