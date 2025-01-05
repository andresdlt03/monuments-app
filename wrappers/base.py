from abc import abstractmethod
from pydantic import BaseModel

class Wrapper():
    def __init__(self, txt : str):
        self.txt = txt

    @abstractmethod
    def get_data(self):
        pass

class TxtModel(BaseModel):
    data: str