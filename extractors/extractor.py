from abc import abstractmethod
from logging import Logger
from supabase import Client
class Extractor():

    def __init__(self, db: Client, logger: Logger):
        self.db = db
        self.logger = logger
        self.monuments = []
        self.provinces = []
        self.localities = []

    """
    Main method that will process the raw data received by the endpoint, calling all the
    internal methods of the extractor to validate and map the monuments to the internal schema.
    """
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

    def insert_new_province(self, new_province):
        self.provinces.append(new_province)
        self.db.table('provincia').insert(new_province).execute()

    def insert_new_locality(self, new_locality):
        self.localities.append(new_locality)
        self.db.table('localidad').insert(new_locality).execute()

    def insert_new_monument(self, new_monument):
        self.db.table('monumento').insert(new_monument).execute()

    """
    Function that will take each key-value of each data object in json and save only
    the values that have their key within the schema, changing the key to the one mapped.
    """
    @abstractmethod
    def map_monument_to_local_schema(self, json, schema: dict[str, str]):
        pass
