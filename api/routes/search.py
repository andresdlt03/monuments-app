from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from ..model.body import SearchMonument
from ..services.search import SearchMonumentService
from logger import logger

router = APIRouter()

@router.post("/search/", tags=["search"])
async def search_for_monuments(
    locality: str = Form(None), 
    zip_code: str = Form(None), 
    province: str = Form(None), 
    monument_type: str = Form(None)
):
    try:
        logger.info("Procesando datos del formulario")
        search_params = {
            "locality": locality,
            "zip_code" : zip_code,
            "province" : province,
            "monument_type" : monument_type
        } 
        results = SearchMonumentService(search_params)
        return JSONResponse(content={"message": "Búsqueda exitosa", "results": results})
    except Exception as e:
        logger.error(f"Error procesando los datos de busqueda: {e}")
        return {"error": "No se pudo buscar monumentos", "details": str(e)}