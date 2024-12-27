from . import (wrappers,postal_codes)
provincias = postal_codes.provincias

def get_euskadi() -> list:
    url = 'data-sources/Entrega1/edificios.json'

    data = wrappers.Wrapper_MUR(url).get_data();

    monumentsScheme = {
        'documentName' : 'nombre',
        'address' : 'direccion',
        'postalCode': 'codigo_postal',
        'lonwgs84' : 'longitud',
        'latwgs84' :'latitud',
        'documentDescription' : 'descripcion'
    }

    typeScheme = {
        "Yacimiento_arqueologico": [
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

    