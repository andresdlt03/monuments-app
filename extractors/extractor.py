from abc import abstractmethod

class Extractor():
    """
    The mapToSchema function will take each key-value of each data object in json and save only
    the values that have their key within the schema, changing the key to the one mapped.
    """
    @abstractmethod
    def mapToSchema(json: str, schema: dict[str, str]):
        pass

    """
    The isValidData function will validate that a row of data is valid and has to be saved on database.
    """
    def isValidMonument(row: str) -> bool:
        pass