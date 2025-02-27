from logging import Logger
from supabase import Client
from .extractor import Extractor
from .mappings.euskadi import (euskadi_monument_mapping, euskadi_monument_type_mapping, euskadi_province_mapping, euskadi_locality_mapping)

class EuskadiExtractor(Extractor):
    def __init__(self, db: Client, logger: Logger):
        super().__init__(db, logger)
        self.provinces_codes = (1, 20, 48)
        self.provinces_names = ['Araba/Álava', 'Bizkaia', 'Gipuzkoa']
    """
    Method that process a monument with its location to map the name of the properties with our local schema.
    """
    def _map_monument_to_local_schema(self, raw_monument: dict):
        monument_mapped = {}
        for key in euskadi_monument_mapping:
            value = raw_monument.setdefault(key, "")
            monument_mapped[euskadi_monument_mapping[key]] = value
        monument_mapped['tipo'] = self._set_monument_type(monument_mapped['nombre'])

        province_mapped = {}
        for key in euskadi_province_mapping:
            value = raw_monument[key]
            province_mapped[euskadi_province_mapping[key]] = value

        locality_mapped = {}
        for key in euskadi_locality_mapping:
            value = raw_monument[key]
            locality_mapped[euskadi_locality_mapping[key]] = value

        # SECTION - THIS SECTION IS TO CORRECT THE SPECIFICS ERROR IN THE DATA. It could be extracted to a different method.
        # NOTE - province id = "20 01" -> we only take the "20"
        province_mapped['id'] = province_mapped['id'].split()[0]
        locality_mapped['provincia_id'] = locality_mapped['provincia_id'].split()[0]

        return (monument_mapped, province_mapped, locality_mapped)

    """
    Method that assign a type for the monument by looking for keywords in the name.
    """
    def _set_monument_type(self, nombre: str):
        for monument_type, keywords in euskadi_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"
    
    def _log_error(self, raw_monument: dict, ex: Exception):
        message = f"Error en el monumento '{raw_monument.get('documentName')}', {ex}"
        self.logger.warning(message)
        return message