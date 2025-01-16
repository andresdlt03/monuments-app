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

        self.processed_monuments = 0
        self.total_monuments = 0

    """
    Main method that will process the raw data received by the endpoint, calling all the
    internal methods of the extractor to validate and map the monuments to the internal schema.
    """
    def process_data(self, raw_monuments: list[dict]):
        self._initialize_data()
        
        self.total_monuments = len(raw_monuments)

        for raw_monument in raw_monuments:
            try:
                (monument, province, locality) = self._map_monument_to_local_schema(raw_monument)
                self._validate_monument(monument)
                self._validate_location(province, locality)
            except Exception as ex:
                self._log_error(raw_monument, ex)
                continue

            self._process_location(province, locality)
            self._process_monument(monument, locality)

            self.processed_monuments += 1

        self.logger.info(f"Se han procesado {self.processed_monuments} monumentos con éxito de un total de {self.total_monuments}")
        
        self._reset_data()

    """
    Method that will initialize the extractor's data of the provinces, localities and monuments.
    """
    def _initialize_data(self):
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
        
    """
    Method that will reset the extractor's data of the provinces, localities and monuments.
    """
    def _reset_data(self):
        self.monuments = []
        self.provinces = []
        self.localities = []

    """
    Metohod that will validate the good format of the monument data.
    """
    def _validate_monument(self, monument):
        if(monument['latitud'] == '' or monument['longitud'] == ''):
            raise Exception(f'Faltan coordenadas')
        if(monument['nombre'] == ''):
            raise Exception(f'Falta nombre')
        if(monument['codigo_postal'] == ''):
            raise Exception(f'Falta código postal')
        if(monument['descripcion'] == ''):
            raise Exception(f'Falta descripción')

    """
    Method that will validate the location of the monument, checking if the province and locality
    are not empty.
    """
    def _validate_location(self, province, locality):
        if(province['nombre'] == ''):
            raise Exception(f'No tiene nombre de provincia (código de provincia: {province['id']})')
        if(locality['nombre'] == ''):
            raise Exception('No tiene nombre de localidad')

    """
    Method that will process the location of the monument, checking if the province and locality
    are already registered in the database, and if not, will insert them.
    """
    def _process_location(self, province, locality):
        province_registered = False
        for p in self.provinces:
            if (int(p['id']) == int(province['id'])):
                province_registered = True
        if(not province_registered):
            self._insert_new_province(province)
        locality_registered = False
        for l in self.localities:
            if (l['nombre'] == locality['nombre']):
                locality_registered = True
        if(not locality_registered):
            self._insert_new_locality(locality)

    """
    Method that will process the monument, checking if the monument is already registered in the database,
    and if not, will insert it.
    """
    def _process_monument(self, monument, locality):
        monument_registered = False
        locality_id = (self.db.table('localidad').select('id').eq('nombre', locality['nombre']).execute()).data[0]['id']
        for m in self.monuments:
            if (m['nombre'] == monument['nombre'] and m['localidad_id'] == locality_id):
                monument_registered = True
        if(not monument_registered):
            monument['localidad_id'] = locality_id
            self._insert_new_monument(monument)

    def _insert_new_province(self, new_province):
        self.provinces.append(new_province)
        self.db.table('provincia').insert(new_province).execute()

    def _insert_new_locality(self, new_locality):
        self.localities.append(new_locality)
        self.db.table('localidad').insert(new_locality).execute()

    def _insert_new_monument(self, new_monument):
        self.db.table('monumento').insert(new_monument).execute()

    """
    Function that will take each key-value of each data object in json and save only
    the values that have their key within the schema, changing the key to the one mapped.
    """
    @abstractmethod
    def _map_monument_to_local_schema(self, json, schema: dict[str, str]):
        pass

    @abstractmethod
    def _log_error(self, raw_monument: dict, ex: Exception):
        pass
