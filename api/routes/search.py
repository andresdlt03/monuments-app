from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from ..services.search import get_monuments as get_monuments_service
from logger import logger

router = APIRouter()

@router.get("/monuments/", tags=["monuments"])
async def get_monuments(
    locality: str = Form(None), 
    zip_code: str = Form(None), 
    province: str = Form(None), 
    monument_type: str = Form(None)
):
    try:
        logger.info("Petición recibida: Procesando formulario...")
        search_params = {
            "locality": locality,
            "zip_code" : zip_code,
            "province" : province,
            "monument_type" : monument_type
        } 
        results = get_monuments_service(search_params)
        return JSONResponse(content={"message": "Búsqueda exitosa", "results": results})
    except Exception as e:
        logger.error(f"Error procesando los datos de busqueda: {e}")
        return {"error": "No se pudieron buscar monumentos", "details": str(e)}
    