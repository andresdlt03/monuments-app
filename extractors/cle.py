import re
from logging import Logger
from supabase import Client
from extractors.extractor import Extractor
from extractors.mappings.cle import (CLE_monument_mapping, CLE_monument_type_mapping)

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
        monument_mapped['longitud'] = raw_monument['coordenadas']['longitud']
        monument_mapped['latitud'] = raw_monument['coordenadas']['latitud']

        province_mapped = {}
        province_mapped['id'] = raw_monument['codigoPostal'][:2]
        province_mapped['nombre'] = raw_monument['poblacion']['provincia']

        locality_mapped = {}
        locality_mapped['nombre'] = raw_monument['poblacion']['localidad']
        locality_mapped['provincia_id'] = raw_monument['codigoPostal'][:2]
        locality_mapped['codigo_postal'] = raw_monument['codigoPostal']

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