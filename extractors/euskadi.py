from . import extractor

monument_type_mapping = {
    "Yacimiento_Arqueologico": [
        "Valle", "Recinto", "Coto", "Calero", "Murallas", "Archivo"
    ],
    "Iglesia_Ermita": [
        "Iglesia", "Ermita", "Catedral", "Basílica", "Parroquia", "Santuario"
    ],
    "Monasterio_Convento": [
        "Monasterio", "Convento", "Cofradia"
    ],
    "Castillo_Fortaleza_Torre": [
        "Castillo", "Fuerte", "Torre", "Torre-Palacio", "Casa-Torre"
    ],
    "Edificio_Singular": [
        "Canteras", "Ferrería", "Conjunto", "Ciudad", "Central", "Arco", "Muralla", 
        "Monumento-Homenaje", "Vivienda", "Pinturas", "Altos", "Casa", "Jauregi", "Viaducto", 
        "Teatro", "Antiguo", "Cruz", "Hórreo", "Balneario", "Bilbao", "Caserío", "Antigua", 
        "Grandes", "Muelle", "Marierrota", "Plaza", "Faro", "Quinta", "Jardín", "Bosque", 
        "Landetxo", "Túnel", "Funicular", "Órgano", "Basque", "Fábrica", "Ayuntamiento", 
        "Aduana", "Mercado", "Palacio", "Bikuña", "Chalet", "Universidad", "Edificio", 
        "Fuente", "Cargadero", "Auditorio", "Paseo", "Puente"
    ],
    "Otros": [
        "Peine", "Parque", "Núcleo", "Pequeño", "El", "San", "Molino", "Puerta", 
        "Villa", "Las", "Monumento", "Senda", "Puerto"
    ]
}

euskadi_monuments_mapping = {
    'documentName': 'nombre',
    'address': 'direccion',
    'postalCode': 'codigo_postal',
    'lonwgs84': 'longitud',
    'latwgs84': 'latitud',
    'documentDescription': 'descripcion'
}

# TODO - FALTA LA VALIDACIÓN DE LOS CAMPOS Y DESHECHAR LOS INCORRECTOS
class EuskadiExtractor(extractor.Extractor):
    def map_to_schema(self, monuments: list[dict]):
        monuments_mapped: list[dict] = []
        for monument in monuments:
            monument_mapped = {}
            for key in euskadi_monuments_mapping:
                value = monument[key]
                if(value):
                    monument_mapped[euskadi_monuments_mapping[key]] = value
            monument_mapped['tipo'] = self._map_monument_type(monument_mapped['nombre'])
            monuments_mapped.append(monument_mapped)
        return monuments_mapped
    
    def _map_monument_type(self, nombre: str):
        for monument_type, keywords in monument_type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in nombre.lower():
                    return monument_type
        return "Otros"