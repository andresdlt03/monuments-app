from database import db
from logger import logger
from selenium import webdriver
from extractors.euskadi import EuskadiExtractor
from extractors.cv import CVExtractor
from extractors.cle import CastillaLeonExtractor

def EUSExtractorService(monument):
    euskadi_extractor = EuskadiExtractor(db, logger)
    euskadi_extractor.process_data(monument)
    return {"message": "MUR extracted"}

def CVExtractorService(monument):
    driver = webdriver.Chrome()
    cv_extractor = CVExtractor(db, logger, driver)
    cv_extractor.process_data(monument)
    return {"message": "CV extracted"}

def CLEExtractorService(monument):
    cle_extractor = CastillaLeonExtractor(db, logger)
    cle_extractor.process_data(monument)
    return {"message": "CAT extracted"}