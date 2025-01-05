from logger import logger
import json
from extractors.euskadi import EuskadiExtractor
from wrappers import (WrapperEuskadi, WrapperValenciana, Wrapper_CAT)
from extractors.extractor import Extractor
from database import db

logger.info("Ejecutando...")

logger.info("Extrayendo información EUSKADI...")

# URLS
euskadi_url = "./data-sources/edificios (euskadi).json"
# castilla_url =  "./data-sources/monumentos (castilla y leon).xml"
# valenciana_url = "./data-sources/bienes_inmuebles_interes_cultural (comunitat valenciana).csv"

# WRAPPERS
euskadi_wrapper = WrapperEuskadi(euskadi_url)
# castilla_wrapper = WrapperEuskadi(castilla_url)
# valenciana_wrapper = WrapperValenciana(valenciana_url)

# JSONS
euskadi_json = euskadi_wrapper.get_data()
# castilla_json = castilla_wrapper.get_data()
# valenciana_json = valenciana_wrapper.get_data()

logger.info("Inicializando extractor EUSKADI...")
euskadi_extractor = EuskadiExtractor(db, logger)

logger.info("Procesando monumentos EUSKADI...")
euskadi_extractor.process_data(euskadi_json)

