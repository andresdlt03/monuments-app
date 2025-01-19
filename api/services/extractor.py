import requests
from database import db
from logger import logger
from extractors.mur import EuskadiExtractor
from extractors.cv import CVExtractor
from extractors.cle import CLEExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def MURExtractorService():
    try:
        logger.info("Pidiendo los documentos a la API de MUR")
        r = requests.get('http://localhost:8003/mur/')
        raw_monuments = r.json()
        
        logger.info("Extrayendo los datos de MUR")
        euskadi_extractor = EuskadiExtractor(db, logger)
        result = euskadi_extractor.process_data(raw_monuments)
        return result
    except Exception as e:
        return {"error": f"Error al extraer la información: {e}"}

def CVExtractorService():
    try:
        logger.info("Pidiendo los documentos a la API de CV")
        r = requests.get('http://localhost:8002/cv/')
        raw_monuments = r.json()

        logger.info("Extrayendo los datos de CV")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        cv_extractor = CVExtractor(db, logger, driver)
        result = cv_extractor.process_data(raw_monuments)
        return result
    except Exception as e:
        return {"error": f"Error al extraer la información: {e}"}

def CATExtractorService():
    try:
        logger.info("Pidiendo los documentos a la API de CAT")
        r = requests.get('http://localhost:8001/cle/')
        raw_monuments = r.json()

        logger.info("Extrayendo los datos de CAT")
        cle_extractor = CLEExtractor(db, logger)
        result = cle_extractor.process_data(raw_monuments)
        return result
    except Exception as e:
        return {"error": f"Error al extraer la información: {e}"}