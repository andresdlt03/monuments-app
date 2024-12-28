from . import extractor

monument_type_mapping = {
    "Yacimiento_Arqueologico": [
        "Valle", "Recinto", "Coto", "Calero", "Murallas", "Santiago", "Archivo"
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

class EuskadiExtractor(extractor.Extractor):
    def mapToSchema(self, monuments: list[dict]):
        monuments_mapped: list[dict] = []
        for monument in monuments:
            new_monument_mapped = {}
            for key in euskadi_monuments_mapping:
                value = monument[key]
                if(value):
                    new_monument_mapped[euskadi_monuments_mapping[key]] = value
            monuments_mapped.append(new_monument_mapped)
        return monuments_mapped