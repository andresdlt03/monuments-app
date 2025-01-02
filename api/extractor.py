from fastapi import APIRouter

router = APIRouter()

@router.post("/mur", tags=["extractor"])
async def extract_mur():
    return {"message": "MUR extracted"}

@router.post("/cv", tags=["extractor"])
async def extract_cv():
    return {"message": "CV extracted"}

@router.post("/cat", tags=["extractor"])
async def extract_cat():
    return {"message": "CAT extracted"}