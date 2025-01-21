import html
import re
from logging import Logger
from bs4 import BeautifulSoup
from supabase import Client
from extractors.extractor import Extractor
from extractors.mappings.cle import (CLE_monument_mapping, CLE_monument_type_mapping)

class CLEExtractor(Extractor):
    def __init__(self, db: Client, logger: Logger):
        super().__init__(db, logger)
        self.provinces_codes = (5, 9, 24, 34, 37, 40, 42, 47, 49)
        self.provinces_names = ['Ávila', 'Burgos', 'León', 'Palencia', 'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora']
        
    """
    Metodo que procesa un documento con su localización para mapear el nombre de las propiedad con los de nuestra base de datos.
    """
    def _map_monument_to_local_schema(self, raw_monument: dict):

        # Comprobamos que el código postal tenga 5 dígitos
        if len(raw_monument['codigoPostal']) == 4: 
            raw_monument['codigoPostal'] = "0" + raw_monument['codigoPostal']
            self.messages.append_repairs(f"El código postal del monumento '{raw_monument.get('nombre')}' ha sido corregido a '{raw_monument['codigoPostal']}'")
        
        # Eliminamos las etiquetas HTML y los espacios en blanco de la descripción
        raw_monument['Descripcion'] = html.unescape(raw_monument['Descripcion'])
        soup = BeautifulSoup(raw_monument['Descripcion'], "html.parser")
        raw_monument['Descripcion'] = soup.get_text()

        monument_mapped = {}
        for key in CLE_monument_mapping:
            value = raw_monument.setdefault(key, "")
            monument_mapped[CLE_monument_mapping[key]] = value
        monument_mapped['tipo'] = self._set_monument_type(raw_monument['tipoMonumento'])
        try:
            monument_mapped['longitud'] = float(raw_monument['coordenadas']['longitud'])
            monument_mapped['latitud'] = float(raw_monument['coordenadas']['latitud'])
        except ValueError:
            raise ValueError("Las coordenadas no son válidas")

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
    def _set_monument_type(self, nombre: str):
        for monument_type, keywords in CLE_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"
    
    def _log_error(self, raw_monument: dict, ex: Exception):
        message = f"Error en el monumento '{raw_monument.get('nombre')}': {ex}"
        self.logger.warning(message)
        return message
