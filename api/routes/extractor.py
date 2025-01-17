from fastapi import APIRouter
from api.services.extractor import MURExtractorService, CVExtractorService, CATExtractorService

router = APIRouter()

@router.post("/extractors/", tags=["extractor"])
async def launch_extractors(extractors: list[str]):
    for extractor in extractors:
        if extractor == 'mur':
            MURExtractorService()
        elif extractor == 'cv':
            CVExtractorService()
        elif extractor == 'cat':
            CATExtractorService()
    return {"message": "Extractors launched"}