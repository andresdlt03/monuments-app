from extractors.euskadi import EuskadiExtractor
from database import db
from logger import logger

def MURExtractorService(monument):
    euskadi_extractor = EuskadiExtractor(db, logger)
    euskadi_extractor.process_data(monument)
    return {"message": "MUR extracted"}

def CVExtractorService(monument):
    return {"message": "CV extracted"}

def CATExtractorService(monument):
    return {"message": "CAT extracted"}