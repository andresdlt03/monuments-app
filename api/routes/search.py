import html
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.search import get_monuments as get_monuments_service
from ..services.search import delete_monuments as delete_monuments_service
from logger import logger

router = APIRouter()

@router.get("/monuments/", tags=["monuments"])
async def get_monuments(
    locality: str | None = None, 
    zip_code: str | None = None, 
    province: str | None = None, 
    monument_type: str | None = None
):
    try:
        logger.info("Petición recibida: Procesando formulario...")
        search_params = {
            "locality": locality,
            "zip_code" : zip_code,
            "province" : province,
            "monument_type" : html.unescape(monument_type)
        } 
        results = get_monuments_service(search_params)
        return JSONResponse(content={"message": "Búsqueda exitosa", "results": results})
    except Exception as e:
        logger.error(f"Error procesando los datos de búsqueda: {e}")
        return {"error": "No se pudieron buscar monumentos", "details": str(e)}
    
@router.delete("/monuments/", tags=["monuments"])
async def delete_monuments():
    logger.info("Petición recibida: Eliminando monumento...")
    result = await delete_monuments_service()
    return result