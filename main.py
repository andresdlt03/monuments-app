from logger import logger
from extractors.euskadi import EuskadiExtractor
from extractors.extractor import Extractor
from database import db
from fastapi import FastAPI
import uvicorn
from wrappers.base import TxtModel
import requests

EUSKADI_API_URL = 'http://127.0.0.1:8000'
CASTILLA_API_URL = 'http://127.0.0.1:8001'
VALENCIANA_API_URL = 'http://127.0.0.1:8002'

logger.info("Ejecutando...")

app = FastAPI(debug=True,title="Monuments API", description="API para la extracción de monumentos", version="1.0")

@app.post("/get_processed_data_euskadi")
def get_processed_data_euskadi(txt : TxtModel = None):
    logger.info("Convirtiendo a json los datos de EUSKADI...")

    if txt == None:
        euskadi_url = "./data-sources/edificios (euskadi).json"
        with open(euskadi_url, 'r', encoding='utf-8') as f: 
            euskadi_to_parse = f.read()
        euskadi_json = requests.post(f"{EUSKADI_API_URL}/get_json", json={'data' : euskadi_to_parse}).text
    else:
        euskadi_json = requests.post(f"{EUSKADI_API_URL}/get_json", json={'data': txt}).text

    logger.info("Inicializando extractor EUSKADI...")
    euskadi_extractor = EuskadiExtractor(db, logger)

    logger.info("Procesando monumentos EUSKADI...")
    euskadi_extractor.processs_data(euskadi_json)

uvicorn.run(app, host="127.0.0.1",port=8003)
