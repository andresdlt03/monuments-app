from .logger import logger
from .api.routes.extractor import router as ExtractorRouter
from api.routes.search import router as SearchRouter
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

logger.info("Ejecutando...")

logger.info("Creando instancia de API...")

api = FastAPI()

logger.info("Inicializando endpoints de la API para los extractores...")

api.include_router(ExtractorRouter, prefix="/extractor", tags=["extractor"])

api.include_router(SearchRouter, prefix="/search", tags=["search"])

api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# route for the search form
@api.get("/busqueda", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("Cargando el formulario de busqueda")
    return templates.TemplateResponse("search.html", {"request": request})