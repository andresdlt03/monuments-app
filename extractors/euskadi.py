import re
from extractors.extractor import Extractor
from extractors.mappings.euskadi import (euskadi_monument_mapping, euskadi_monument_type_mapping)

class EuskadiExtractor(Extractor):
    def map_to_schema(self, monuments: list[dict]):
        monuments_mapped: list[dict] = []
        for monument in monuments:
            monument_mapped = {}
            for key in euskadi_monument_mapping:
                value = monument[key]
                if(value):
                    monument_mapped[euskadi_monument_mapping[key]] = value
            monument_mapped['tipo'] = self._map_monument_type(monument_mapped['nombre'])
            monuments_mapped.append(monument_mapped)
        return monuments_mapped
    
    def _map_monument_type(self, nombre: str):
        for monument_type, keywords in euskadi_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"
    
    def is_valid_zip_code(zip_code: str):
        if not re.fullmatch(r'\d{5}', zip_code):
            return False
        
        province = int(zip_code[:2])
        
        return province in [1, 20, 48] # Codes of Alaba, Guipuzcoa and Bizkaia 