from abc import abstractmethod
from logging import Logger
from supabase import Client
import unicodedata
from geopy.geocoders import Nominatim
from extractors.message import Message

class Extractor():

    def __init__(self, db: Client, logger: Logger):
        self.db = db
        self.logger = logger
        self.monuments = []
        self.provinces = []
        self.localities = []
        self.provinces_codes = ()
        self.provinces_names = []
        self.messages = Message()

        self.processed_monuments = 0
        self.total_monuments = 0
        self.geolocator = Nominatim(user_agent="https://nominatim.org")

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
                error_message = self._log_error(raw_monument, ex)
                self.messages.append_errors(error_message)
                continue
            
            self._process_location(province, locality)
            registered = self._process_monument(monument, locality)
            if not registered:
                self.processed_monuments += 1

        messages_list = self.messages.return_list()
        self.logger.info(f"Se han procesado {self.processed_monuments} monumentos con éxito de un total de {self.total_monuments}")
        messages_list.append(f"Se han procesado {self.processed_monuments} monumentos con éxito de un total de {self.total_monuments}")

        self._reset_data()
        return messages_list

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

    """Method to verify if latitude and longitude are valid."""

    def _validate_latitude_longitude(self,latitude,longitude):
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            return latitude < -90 or latitude > 90 or longitude < -90 or longitude > 90
        except Exception:
            raise Exception(f'Faltan coordenadas')

    """Method to verify if the postal code is valid."""	
    def _validate_postal_code(self,postal_code):
        if postal_code == "":
            raise Exception(f'Falta código postal')
        return int(postal_code[:2]) not in self.provinces_codes
            
        
    """
    Metohod that will validate the good format of the monument data.
    """
    def _validate_monument(self, monument):
        if(self._validate_latitude_longitude(monument['latitud'],monument['longitud'])):
            raise Exception(f'Coordenadas no validas')
        if(monument['nombre'] == ''):
            raise Exception(f'Falta nombre')
        if(self._validate_postal_code(monument['codigo_postal'])):
            raise Exception(f'Codigo postal no valido')
        if(monument['descripcion'] == ''):
            raise Exception(f'Falta descripción')

    """
    Function to remove accents from province and locality to ensure that the comparation from the province given doesn't match with any other on the database.  
    """
    @staticmethod
    def remove_accents(input_str: str) -> str:
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    """Validate the external data from the database to be equal to the data in the database."""
    def _is_valid_province(self, external_province, db_province):
        return self.remove_accents(external_province) == self.remove_accents(db_province)
    
    """"Check that the province name is valid and its in the province_names list."""
    def _check_province_name(self, province):
        try:
            return not any(self._is_valid_province(province['nombre'], name) for name in self.provinces_names)
        except Exception:
            raise Exception(f"No tiene nombre de provincia (código de provincia: {province['id']})")
        
    """
    Method that will validate the location of the monument, checking if the province and locality
    are not empty.
    """
    def _validate_location(self, province, locality):
        if(self._check_province_name(province)):
            raise Exception(f'Provincia no válida')
        if(locality['nombre'] == ''):
            raise Exception('No tiene nombre de localidad')
    

    """Get equal province name from the correct provinces names."""
    def _get_province_name(self, province):
        original_province = next(name for name in self.provinces_names if self._is_valid_province(province['nombre'], name))
        if original_province != province['nombre']:
            self.messages.append_repairs(f"Se ha corregido el nombre de la provincia de {province['nombre']} a {original_province}")
        return original_province
    """
    Method that will process the location of the monument, checking if the province and locality
    are already registered in the database, and if not, will insert them.
    """
    def _process_location(self, province, locality):
        province_registered = False
        province['nombre'] = self._get_province_name(province)
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
    Method that will get the address from the latitude and longitude of the monument
    """
    @staticmethod
    def get_address_from_lat_lng(lat : str, lng : str) -> str:
        lat = float(lat)
        lng = float(lng)
        geolocator = Nominatim(user_agent="https://nominatim.org")
        location = geolocator.reverse((lat, lng), exactly_one=True)
        return location.address

    """
    Method that will process the monument, checking if the monument is already registered in the database,
    and if not, will insert it.
    """
    def _process_monument(self, monument, locality):
        monument_registered = False
        locality_id = (self.db.table('localidad').select('id').eq('nombre', locality['nombre']).execute()).data[0]['id']
        for m in self.monuments:
            if (m['nombre'] == monument['nombre'] and m['localidad_id'] == locality_id):
                self.logger.warning(f"Error en el monumento '{monument['nombre']}': ya está registrado en la base de datos")
                self.messages.append_errors(f"Error en el monumento '{monument['nombre']}': ya está registrado en la base de datos")
                monument_registered = True
        if(not monument_registered):
            monument['localidad_id'] = locality_id
            if monument['direccion'] == "":
                monument['direccion'] = self.get_address_from_lat_lng(monument['latitud'], monument['longitud'])
            self._insert_new_monument(monument)
        return monument_registered

    def _insert_new_province(self, new_province):
        self.provinces.append(new_province)
        self.db.table('provincia').insert(new_province).execute()

    def _insert_new_locality(self, new_locality):
        self.localities.append(new_locality)
        self.db.table('localidad').insert(new_locality).execute()

    def _insert_new_monument(self, new_monument):
        self.monuments.append(new_monument)
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
