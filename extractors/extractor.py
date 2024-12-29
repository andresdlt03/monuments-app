from abc import abstractmethod
from database import db
class Extractor():
    """
    Main method that will process the raw data received by the endpoint, calling all the
    internal methods of the extractor to validate and map the monuments to the internal schema.
    """
    @abstractmethod
    def process_data(json):
        pass
    """
    The mapToSchema function will take each key-value of each data object in json and save only
    the values that have their key within the schema, changing the key to the one mapped.
    """
    @abstractmethod
    def map_to_schema(self, json, schema: dict[str, str]):
        pass

    """
    Check if the provided zip code is valid.
    """
    @abstractmethod
    def is_valid_zip_code(self, zip_code: str) -> bool:
        pass

    """
    Method in charge of register and update the locations in database (provinces and municipalities)
    """
    def process_location():
        pass

    """
    The isValidData function will validate that a row of data is valid and has to be saved on database.
    """
    def is_valid_monument(self, row: str) -> bool:
        pass
