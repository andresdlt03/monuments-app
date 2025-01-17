import requests
from ...database import db
from ...logger import logger
from ...extractors.mur import EuskadiExtractor
from ...extractors.cv import CVExtractor
from ...extractors.cle import CLEExtractor

def MURExtractorService():
    try:
        logger.info("Pidiento los documentos a la API de MUR")
        r = requests.get('http://localhost:8003/mur/')
        raw_monuments = r.json()
        
        logger.info("Extrayendo los datos de MUR")
        euskadi_extractor = EuskadiExtractor(db, logger)
        euskadi_extractor.process_data(raw_monuments)
        return {"message": "MUR extracted"}
    except Exception as e:
        return {"message": f"Error: {e}"}

def CVExtractorService():
    try:
        logger.info("Pidiendo los documentos a la API de CV")
        r = requests.get('http://localhost:8002/cv/')
        raw_monuments = r.json()

        logger.info("Extrayendo los datos de CV")
        cv_extractor = CVExtractor(db, logger)
        cv_extractor.process_data(raw_monuments)
        return {"message": "CV extracted"}
    except Exception as e:
        return {"message": f"Error: {e}"}

def CATExtractorService():
    try:
        logger.info("Pidiendo los documentos a la API de CAT")
        r = requests.get('http://localhost:8001/cle/')
        raw_monuments = r.json()

        logger.info("Extrayendo los datos de CAT")
        cle_extractor = CLEExtractor(db, logger)
        cle_extractor.process_data(raw_monuments)
        return {"message": "CAT extracted"}
    except Exception as e:
        return {"message": f"Error: {e}"}