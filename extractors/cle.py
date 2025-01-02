import re
from logging import Logger
from supabase import Client
from extractors.extractor import Extractor
from extractors.mappings.cle import (CLE_province_mapping, CLE_locality_mapping, CLE_monument_mapping, CLE_monument_type_mapping)

class CastillaLeonExtractor(Extractor):
    def __init__(self, db: Client, logger: Logger):
        super().__init__(db, logger)
        self.provinces_codes = (5, 9, 24, 32, 34, 37, 40, 47, 49)
        
    """
    Metodo que procesa un documento con su localización para mapear el nombre de las propiedad con los de nuestra base de datos.
    """
    def map_monument_to_local_schema(self, raw_monument: dict):
        monument_mapped = {}
        for key in CLE_monument_mapping:
            value = raw_monument[key]
            monument_mapped[CLE_monument_mapping[key]] = value
        monument_mapped['tipo'] = self.set_monument_type(monument_mapped['nombre'])

        province_mapped = {}
        for key in CLE_province_mapping:
            value = raw_monument[key]
            province_mapped[CLE_province_mapping[key]] = value

        locality_mapped = {}
        for key in CLE_locality_mapping:
            value = raw_monument[key]
            locality_mapped[CLE_locality_mapping[key]] = value

        # SECTION - THIS SECTION IS TO CORRECT THE SPECIFICS ERROR IN THE DATA. It could be extracted to a different method.
        # NOTE - province id = "20 01" -> we only take the "20"
        province_mapped['id'] = province_mapped['id'].split()[0]
        locality_mapped['provincia_id'] = locality_mapped['provincia_id'].split()[0]

        return (monument_mapped, province_mapped, locality_mapped)

    """
    Metodo que asigna el tipo de monumento por las palabras clave en el nombre
    """
    def set_monument_type(self, nombre: str):
        for monument_type, keywords in CLE_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"