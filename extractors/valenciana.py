from . import (wrappers,postal_codes)
from geopy.geocoders import Nominatim
from pyproj import Proj, Transformer
from functools import partial

provincias = postal_codes.provincias

def get_valencia(pId : int = 0,lId : int = 0) -> list:
    url = 'data-sources/Entrega1/bienes_inmuebles_interes_cultural.csv'

    wrapper = wrappers.Wrapper_CV(url)

    data= wrapper.get_data()

    geolocator = Nominatim(user_agent="https://nominatim.org")

    reverse = partial(geolocator.reverse, language="es")

    utm_projection = Proj(proj="utm", zone=30, ellps="WGS84", south=False)

    wgs84_projection = Proj(proj="latlong", datum="WGS84")

    transformer = Transformer.from_proj(utm_projection, wgs84_projection)

    mScheme = {
        'DENOMINACION' : 'nombre',
        'CATEGORIA' : 'descripcion'
        }

    typeScheme = {
        "Yacimiento_arqueologico": [
            "Yacimiento", "Abrigos", "Covalta", "Cerro", "Restos", "Poblado", "Petroglifos", "Petroglifo", "Necrópolis"
        ],
        "Iglesia_Ermita": [
            "Iglesia", "Ermita", "Santuario", "Esglèsia", "Capilla", "Basílica", "Concatedral", "Colegiata", "Calvario"
        ],
        "Monasterio_Convento": [
            "Monasterio", "Convento", "Ex-Convento", "Exconvento", "Cartuja"
        ],
        "Castillo_Fortaleza_Torre": [
            "Castillo", "Fortaleza", "Torre", "Torres", "Torreón", "Torrecilla", "Castellet", "Castell", 
            "Castillo-Palacio", "Castillo-Alcazaba", "Fuerte", "Batería", "Fortín"
        ],
        "Edificio_Singular": [
            "Muralla", "Lienzo", "Tramo", "Arco", "Puente", "Mercado", "Ayuntamiento", "Ayuntamiento.", 
            "Edificio", "Palacio", "Palau", "Casco", "Casona", "Real", "Colegio", "Biblioteca", "Sindicato", 
            "Lonja", "Hospital", "Fábrica", "Escuelas", "Universidad", "Archivo", "Escudo", "Escudos", 
            "Atarazanas", "Capitanía", "Portal"
        ],
        "Otros": [
            "Cova", "Cisterna", "Campana", "Estación", "Pont", "Plaza", "Peiró", "Villa", "Casa", "L'Abric", 
            "Cruz", "Castillico", "Conjunto", "Cabezo", "La", "Colección", "Museo", "Recinto", "Canal", 
            "Templo", "Alt", "Alquería", "Elca,", "Cabeçó", "Bastida", "Colonia", "Alcázar", "Los", 
            "Palmeral", "Santa", "Covetes", "Barranco", "Puig", "Masia", "Masía", "Drama", "Solar", 
            "Desierto", "Pantano", "Ruta", "Zona", "Baños", "Barrio", "Grau", "Parque", "Orpesa", 
            "Molino", "Molinar", "Tossal", "Illeta", "Gloriosa", "Emblema", "El", "Lugar", "Finca", 
            "Séquia", "Jardín", "Mas", "Ciudad", "Villas", "Torrelló", "Dos", "Antigua", "Antiguo", "Teulada", 
            "Presa", "Alto"
        ]
    }

    extractor = {}
    PROVINID = pId
    LOCALID = lId
    provinid = pId
    localid = lId
    province_gen = 'PROVINCIA'
    locality_gen = 'MUNICIPIO'


    def get_information(norte, este):
        utm_x = int(norte)
        utm_y = int(este)
        try:
            longitude, latitude = transformer.transform(utm_x, utm_y)
            location = reverse(f'{latitude} , {longitude}')
        except:
            return {'longitud' : '', 'latitud' : '', 'direccion' : '', 'codigo_postal' : ''}
        address = list(map(lambda x : x.strip(), location.address.split(',')))
        p = list(filter(lambda x: x.isdigit(),address))
        codigo_postal = p[0] if len(p) > 0 else ''
        direccion = address[1]   
        return {'longitud' : str(longitude), 'latitud' : str(latitude), 'direccion' : direccion, 'codigo_postal' : codigo_postal}


    def extractorter(jsonkey : str,extractorkey : str,en_provincia : int = None) -> int:
        dataList = extractor.setdefault(extractorkey,{}) #Obtain the extractor value from the key from reference
        # if made if it is a province, if not its a locality
        nameList = monumentData[jsonkey].split(' ')[0] if jsonkey == province_gen else monumentData[jsonkey] #Get the name of the reference
        jsonn = [key for key, value in dataList.items() if value['nombre'] == nameList]
        #Make a boolean list to sort out if there the reference already exists list(filter(lambda x: dataList[x]['nombre'] == nameList,dataList))
        if not len(jsonn) > 0:
            idd = LOCALID + len(dataList) if extractorkey == 'localities' else PROVINID + len(dataList)
            dataList.update({idd : {'nombre' : nameList}})
            if extractorkey == 'localities':
                dataList[idd].update({'en_provincia' : en_provincia})
            print(f'Created {jsonkey} with id: {idd} and name: {nameList}')
        else:
            idd =  jsonn[0] #Get reference which already exists in the database
        return idd


    def ensureinformation(data : dict) -> bool:
        longitud = ''.join(c for c in data['longitud'] if c.isdigit() or c == '.' or c == '-')
        latitud = ''.join(c for c in data['latitud'] if c.isdigit() or c == '.' or c == '-')
        ensure = list(data.values()).count('') > 0 or float(longitud) < -90 or float(latitud) < -90 or float(longitud) > 90 or float(latitud) > 90 or int(data['codigo_postal'][:2]) < 1 or int(data['codigo_postal'][:2]) > 52
        if ensure:
            return False
        for locality in extractor['localities']:
            if locality == data['en_localidad']:
                for province in extractor['provinces']:
                    if province == extractor['localities'][locality]['en_provincia']:
                        return len(data['codigo_postal']) == 5 and provincias[data['codigo_postal'][:2]].lower() in extractor['provinces'][province]['nombre'].lower()


    data = list(filter(lambda x : list(x.values()).count('') == 0,data))
    for monumentData in data:
        #province transform
        if province_gen in monumentData and monumentData[province_gen] != '':
            provinid = extractorter(province_gen,'provinces')
        # locality transform
        if locality_gen in monumentData and monumentData[locality_gen] != '':
            localid = extractorter(locality_gen,'localities',provinid)
        #monument tranform
        aux = {}
        for j in mScheme:
            aux.update({mScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mScheme[j] : ""})

        aux.update(get_information(monumentData['UTMNORTE'],monumentData['UTMESTE']))               
        aux.update({'en_localidad' : localid})

        '''change on typo'''
        typo = monumentData['DENOMINACION'].split(' ')[0]
        for j in typeScheme:
            if typo in typeScheme[j]:
                aux.update({'tipo' : j})
                break

        if 'tipo' not in aux:
            aux.update({'tipo' : 'Otros'})
        
        m = extractor.setdefault('monuments',[])

        if ensureinformation(aux):
            m.append(aux)
            print('Created MONUMENT: ' + aux['nombre'])


    return [extractor,provinid,localid]