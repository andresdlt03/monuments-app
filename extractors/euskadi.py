import re
from logging import Logger
from supabase import Client
from extractors.extractor import Extractor
from extractors.mappings.euskadi import (euskadi_monument_mapping, euskadi_monument_type_mapping, euskadi_province_mapping, euskadi_locality_mapping)

class EuskadiExtractor(Extractor):
    def __init__(self, db: Client, logger: Logger):
        self.logger = logger
        self.db = db
        self.provinces_codes = (1, 20, 48)
        self.monuments = []
        self.provinces = []
        self.localities = []

    def process_data(self, raw_monuments: list[dict]):
        self.initialize_data()
        for raw_monument in raw_monuments:
            (monument, province, locality) = self.map_monument_to_local_schema(raw_monument)

            try:
                self.validate_monument(monument)
            except Exception as ex:
                self.logger.warning(f"Error en el monumento '{monument['nombre']}': {ex}")
                continue

            self.process_location(province, locality)
            self.process_monument(monument, locality)
        self.reset_data()
            
    # REVIEW - It could be generalised to Extractor class?
    def initialize_data(self):
        self.provinces = (
            self.db.table('provincia')
            .select('*')
            .filter('id', 'in', self.provinces_codes)
            .execute()).data
        self.localities = (
            self.db.table('localidad')
            .select('*')
            .filter('provincia_id', 'in', self.provinces_codes)
            .execute()).data
        
        localities_ids = tuple([d.get('id') for d in self.localities if d.get('id') is not None])
        self.monuments = (
            self.db.table('monumento')
            .select('*')
            .filter('localidad_id', 'in', localities_ids)
            .execute()).data
        
    def reset_data(self):
        self.monuments = []
        self.provinces = []
        self.localities = []

    def validate_monument(self, monument):
        if(monument['latitud'] == '' or monument['longitud'] == ''):
            raise Exception(f'Al monumento le faltan coordenadas')
        if(monument['nombre'] == ''):
            raise Exception(f'Al monumento le falta nombre')
        if(monument['codigo_postal'] == ''):
            raise Exception(f'Al monumento le falta código postal')
        # if(monument['direccion'] == ''):
        #     raise Exception(f'Al monumento {monument['nombre']} le falta dirección')
        if(monument['descripcion'] == ''):
            raise Exception(f'Al monumento le falta descripción')

    def validate_location(self, province, locality):
        if(province['nombre'] == ''):
            raise Exception(f'No tiene nombre de provincia (código de provincia: {province['id']})')
        if(locality['nombre'] == ''):
            raise Exception('No tiene nombre de localidad')

    def process_location(self, province, locality):
        province_registered = False
        for p in self.provinces:
            if (int(p['id']) == int(province['id'])):
                province_registered = True
        if(not province_registered):
            self.insert_new_province(province)
        locality_registered = False
        for l in self.localities:
            if (l['nombre'] == locality['nombre']):
                locality_registered = True
        if(not locality_registered):
            self.insert_new_locality(locality)

    def process_monument(self, monument, locality):
        monument_registered = False
        locality_id = (self.db.table('localidad').select('id').eq('nombre', locality['nombre']).execute()).data[0]['id']
        for m in self.monuments:
            if (m['nombre'] == monument['nombre'] and m['localidad_id'] == locality_id):
                monument_registered = True
        if(not monument_registered):
            monument['localidad_id'] = locality_id
            self.insert_new_monument(monument)

    # REVIEW - It could be generalised to Extractor class?
    def insert_new_province(self, new_province):
        self.provinces.append(new_province)
        self.db.table('provincia').insert(new_province).execute()

    # REVIEW - It could be generalised to Extractor class?
    def insert_new_locality(self, new_locality):
        self.localities.append(new_locality)
        self.db.table('localidad').insert(new_locality).execute()

    def insert_new_monument(self, new_monument):
        self.db.table('monumento').insert(new_monument).execute()

    """
    Method that process a monument with its location to map the name of the properties with our local schema.
    """
    def map_monument_to_local_schema(self, raw_monument: dict):
        monument_mapped = {}
        for key in euskadi_monument_mapping:
            value = raw_monument[key]
            monument_mapped[euskadi_monument_mapping[key]] = value
        monument_mapped['tipo'] = self.set_monument_type(monument_mapped['nombre'])

        province_mapped = {}
        for key in euskadi_province_mapping:
            value = raw_monument[key]
            province_mapped[euskadi_province_mapping[key]] = value

        locality_mapped = {}
        for key in euskadi_locality_mapping:
            value = raw_monument[key]
            locality_mapped[euskadi_locality_mapping[key]] = value

        # NOTE - province id = "20 01" -> we only take the "20"
        province_mapped['id'] = province_mapped['id'].split()[0]
        locality_mapped['provincia_id'] = locality_mapped['provincia_id'].split()[0]

        return (monument_mapped, province_mapped, locality_mapped)

    """
    Method that assign a type for the monument by looking for keywords in the name.
    """
    def set_monument_type(self, nombre: str):
        for monument_type, keywords in euskadi_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"