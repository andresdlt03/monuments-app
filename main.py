from fastapi import FastAPI
import uvicorn
from .logger import logger
from .api.routes.extractor import router as extractorRouter

logger.info("Ejecutando...")

logger.info("Creando instancia de API...")

app = FastAPI()

# Configuración API de carga

logger.info("Configurando API de carga...")

app.include_router(extractorRouter)

logger.info("API configurada")

logger.info("Proceso finalizado.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7999)