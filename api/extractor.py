from fastapi import APIRouter

router = APIRouter()

@router.post("/mur")
async def extract_mur():
    return {"message": "MUR extracted"}

@router.post("/cv")
async def extract_cv():
    return {"message": "CV extracted"}

@router.post("/cat")
async def extract_cat():
    return {"message": "CAT extracted"}