from logging import Logger
import re
from pyproj import Proj, Transformer
from supabase import Client
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from extractors.extractor import Extractor
from extractors.mappings.cv import (CV_monument_type_mapping, cv_locality_mapping, cv_monument_mapping, cv_province_mapping)

WEB_URL = 'https://www.coordenadas-gps.com/convertidor-de-coordenadas-gps'

utm_projection = Proj(proj="utm", zone=30, ellps="WGS84", south=False)
wgs84_projection = Proj(proj="latlong", datum="WGS84")

class CVExtractor(Extractor):
    def __init__(self, db: Client, logger: Logger, driver: webdriver.Chrome):
        super().__init__(db, logger)
        self.provinces_codes = (3, 12, 46)
        self.provinces_names = ['Castellón', 'Valencia', 'Alicante']
        
        self.transformer = Transformer.from_proj(utm_projection, wgs84_projection)
        self.driver = driver

        self.driver.implicitly_wait(10)
        self.driver.get(WEB_URL)
        # Consent the cookies
        consent_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='fc-button fc-cta-consent fc-primary-button']"))
        )
        consent_button.click()
        
    """
    Method that process a monument with its location to map the name of the properties with our local schema.
    """
    def _map_monument_to_local_schema(self, raw_monument: dict):
        utmNorte = raw_monument['UTMNORTE']
        utmEste = raw_monument['UTMESTE']
        if(utmNorte == '' or utmEste == ''):
            raise Exception('Coordenadas UTM vacías')
        # Transform the location fron UTM to WGS84
        longitude, latitude = self.transformer.transform(utmNorte, utmEste)
        try:
            (address, zip_code) = self._scrap_location_with_webdriver(longitude, latitude)
        except Exception as ex:
            raise Exception('Error en la localización WGS84')


        monument_mapped = {}
        for key in cv_monument_mapping:
            value = raw_monument[key]
            monument_mapped[cv_monument_mapping[key]] = value
        monument_mapped['tipo'] = self._set_monument_type(monument_mapped['nombre'])
        monument_mapped['direccion'] = address
        monument_mapped['codigo_postal'] = zip_code
        monument_mapped['latitud'] = latitude
        monument_mapped['longitud'] = longitude

        province_mapped = {}
        for key in cv_province_mapping:
            value = raw_monument[key].capitalize()
            province_mapped[cv_province_mapping[key]] = value
        province_mapped['id'] = zip_code[0:2]

        locality_mapped = {}
        for key in cv_locality_mapping:
            value = raw_monument[key].capitalize()
            locality_mapped[cv_locality_mapping[key]] = value
        locality_mapped['provincia_id'] = zip_code[0:2]
        locality_mapped['codigo_postal'] = zip_code

        return (monument_mapped, province_mapped, locality_mapped)

    def _scrap_location_with_webdriver(self, longitude: float, latitude: float):
        # Select fields of the form to insert the coordinates
        lat_input = self.driver.find_element(by=By.ID, value='latitude')
        long_input = self.driver.find_element(by=By.ID, value='longitude')
        # Select the button to submit the coordinates
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Obtener Dirección']")
        # Insert the coordinates in the form
        lat_input.clear()
        lat_input.send_keys(latitude)
        long_input.clear()
        long_input.send_keys(longitude)
        # Submit the form
        submit_button.click()
        # Get the input that contains the address
        address_text_box = self.driver.find_element(By.ID, 'address')
        # Wait until the address input has a value
        WebDriverWait(self.driver, 10).until(lambda driver: address_text_box.get_attribute('value') != '')
        address = address_text_box.get_attribute('value')
        # Process the output
        clean_address = re.match(r"^(.*?), \d{5}", address).group()
        zip_code = re.search(r"\b\d{5}\b", address).group()
        
        return (clean_address, zip_code)

    """
    Method that assign a type for the monument by looking for keywords in the name.
    """
    def _set_monument_type(self, nombre: str):
        for monument_type, keywords in CV_monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"
    
    def _log_error(self, raw_monument: dict, ex: Exception):
        message = f"Error en el monumento '{raw_monument.get('DENOMINACION')}': {ex}"
        self.logger.warning(message)
        return message