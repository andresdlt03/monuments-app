from logger import logger
import json
from extractors.euskadi import EuskadiExtractor

logger.info("Ejecutando...")

logger.info("Extrayendo información EUSKADI...")

url = "./data-sources/edificios (euskadi).json"

# TODO - Remove this two lines
euskadi_file = open(url, 'r', encoding='UTF-8')
euskadi_json: str = json.loads(euskadi_file.read())

euskadi_extractor = EuskadiExtractor()
euskadi_mapped = euskadi_extractor.map_to_schema(euskadi_json)