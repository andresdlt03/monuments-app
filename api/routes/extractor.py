from fastapi import APIRouter
from ..model.body import MURMonument, CVMonument, CATMonument
from ..services.extractor import MURExtractorService

router = APIRouter()

@router.post("/mur/", tags=["extractor"])
async def extract_mur(monument: MURMonument):
    MURExtractorService(monument)

@router.post("/cv/", tags=["extractor"])
async def extract_cv(monument: CVMonument):
    return {"message": "CV extracted"}

@router.post("/cat/", tags=["extractor"])
async def extract_cat(monument: CATMonument):
    return {"message": "CAT extracted"}