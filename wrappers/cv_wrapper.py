from base import Wrapper
import csv
import io

class WrapperCV(Wrapper):
    def get_data(self) -> dict:
        csv_data = io.StringIO(self.txt)
        reader = csv.DictReader(csv_data,delimiter=';')
        rows = list(reader)
        self.rows = rows
        return rows
