from .logger import logger
from .api.routes.extractor import router as ExtractorRouter
from api.routes.search import router as SearchRouter
from fastapi import FastAPI

logger.info("Ejecutando...")

logger.info("Creando instancia de API...")

api = FastAPI()

logger.info("Inicializando endpoints de la API para los extractores...")

api.include_router(ExtractorRouter, prefix="/extractor", tags=["extractor"])

api.include_router(SearchRouter, prefix="/search", tags=["search"])
