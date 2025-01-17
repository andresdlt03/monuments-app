from fastapi import FastAPI
import uvicorn
from logger import logger
from api.routes.extractor import router as extractorRouter
from fastapi.middleware.cors import CORSMiddleware

logger.info("Ejecutando...")

logger.info("Creando instancia de API...")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración API de carga

logger.info("Configurando API de carga...")

app.include_router(extractorRouter)

logger.info("API configurada")

logger.info("Proceso finalizado.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7999)