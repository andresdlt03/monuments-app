from base import Wrapper
import json

class WrapperMUR(Wrapper):
    def get_data(self) -> dict:
        return json.loads(self.txt)