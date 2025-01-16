from fastapi import APIRouter
from ..model.body import EUSMonument, CVMonument, CLEMonument
from ..services.extractor import EUSExtractorService
from ..services.extractor import CVExtractorService
from ..services.extractor import CLEExtractorService

router = APIRouter()

@router.post("/mur/", tags=["extractor"])
async def extract_mur(monument: EUSMonument):
    EUSExtractorService(monument)
    return {"message": "EUS extracted"}

@router.post("/cv/", tags=["extractor"])
async def extract_cv(monument: CVMonument):
    CVExtractorService(monument)
    return {"message": "CV extracted"}

@router.post("/cat/", tags=["extractor"])
async def extract_cat(monument: CLEMonument):
    CLEExtractorService
    return {"message": "CAT extracted"}