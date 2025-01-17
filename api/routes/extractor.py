from fastapi import APIRouter
from api.services.extractor import MURExtractorService, CVExtractorService, CATExtractorService
from pydantic import BaseModel

router = APIRouter()

class Extractors(BaseModel):
    extractors: list[str]

@router.post("/extractors/", tags=["extractor"])
async def launch_extractors(extractors: Extractors):
    for extractor in extractors.extractors:
        if extractor == 'mur':
            MURExtractorService()
        elif extractor == 'cv':
            CVExtractorService()
        elif extractor == 'cat':
            CATExtractorService()
    return {"message": "Extractors launched"}