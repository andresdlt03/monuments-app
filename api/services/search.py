from database import db
from logger import logger
from ..model.body import SearchMonument
from fastapi.responses import JSONResponse

def SearchMonumentService(search_params: dict):
    monuments = db.table('monumento').select("*").execute()
    localities = db.table("localidad").select('id', 'nombre').execute().data
    provinces = db.table('provincia').select('id', 'nombre').execute().data
    monuments_data = monuments.data

    print(search_params.get("locality"))
    print(search_params.get("provincia"))
    print(search_params.get("zip_code"))
    print(search_params.get("monument_type"))
    
    locality_dict = {locality['id']: locality['nombre'] for locality in localities}
    province_dict = {province['id']: province['nombre'] for province in provinces}

    if search_params.get("locality"):
        locality_name = search_params["locality"].lower()  
        monuments_data = [
            monument for monument in monuments_data
            if locality_name in locality_dict.get(monument["localidad_id"], "").lower()]
    
    if search_params.get("zip_code"):
        zip_code = str(search_params["zip_code"]).strip()
        monuments_data = [monument for monument in monuments_data if zip_code == monument["codigo_postal"]]
    
    if search_params.get("province"):
        province_name = search_params["province"].lower() 
        monuments_data = [
            monument for monument in monuments_data
            if province_name in province_dict.get(monument["provincia_id"], "").lower()]
    
    if search_params.get("monument_type"):
        monument_type = search_params["monument_type"].lower()
        monuments_data = [
            monument for monument in monuments_data
            if monument_type == monument["tipo"].lower()
        ]

    return monuments_data
