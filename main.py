from logger import logger
import json
from extractors.euskadi import EuskadiExtractor
from extractors.extractor import Extractor
from database import db

logger.info("Ejecutando...")

logger.info("Extrayendo información EUSKADI...")

url = "./data-sources/edificios (euskadi).json"

# TODO - Remove this two lines
euskadi_file = open(url, 'r', encoding='UTF-8')
euskadi_json = json.loads(euskadi_file.read())

euskadi_extractor = EuskadiExtractor(db, logger)
euskadi_extractor.process_data(euskadi_json)
