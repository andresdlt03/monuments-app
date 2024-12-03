from . import (wrappers,postal_codes)
import re

provincias = postal_codes.provincias

def get_castilla(pId : int = 0,lId : int = 0) -> list:
    url = 'data-sources/Entrega1/monumentos.xml'
    
    wrapper = wrappers.Wrapper_CAT(url)

    data = wrapper.get_data()

    mScheme = {
        'nombre' : 'nombre',
        'calle' : 'direccion',
        'codigoPostal': 'codigo_postal',
        'longitud' : 'longitud',
        'latitud' :'latitud',
        'Descripcion' : 'descripcion'
        }

    typeScheme = {
        "Yacimiento_arqueologico": [
            "Yacimientos arqueológicos"
        ],
        "Iglesia_Ermita": [
            "Iglesias y Ermitas",
            "Catedrales",
            "Santuarios"
        ],
        "Monasterio_Convento": [
            "Monasterios"
        ],
        "Castillo_Fortaleza_Torre": [
            "Castillos",
            "Torres"
        ],
        "Edificio_Singular": [
            "Murallas y Puertas",
            "Sinagogas",
            "Palacios",
            "Reales Sitios",
            "Casas Nobles",
            "Casas Consistoriales"
        ],
        "Otros": [
            "Plazas Mayores",
            "Esculturas",
            "Cruceros",
            "Jardín Histórico",
            "Hórreos",
            "Paraje pintoresco",
            "Otras localidades",
            "Sitio Histórico",
            "Fuentes",
            "Molinos",
            "Conjunto Etnológico"
        ]
    }

    extractor = {}
    PROVINID = pId
    LOCALID = lId
    provinid = pId
    localid = lId
    province_gen = 'provincia'
    locality_gen = 'localidad'

    vowel_map = {
        "a": "á",
        "e": "é",
        "i": "í",
        "o": "ó",
        "u": "ú",
        "A": "Á",
        "E": "É",
        "I": "Í",
        "O": "Ó",
        "U": "Ú"
    }
    
    def change_to_acute(match):
        captured_char = match.group(0)
        if captured_char[1] in vowel_map:
            return vowel_map[captured_char[1]]
        elif 'dash' in captured_char:
            return '/'
        elif 'nbsp' in captured_char:
            return ''
        return captured_char[1]


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
        aux.update({'en_localidad' : localid})

        '''change on typo'''
        aux['descripcion'] = re.sub(r'<[^>]*>', '', aux['descripcion'])
        aux['descripcion'] = re.sub(r'&([a-zA-Z](acute|tilde))+;',change_to_acute, aux['descripcion'])

        typo = monumentData['tipoMonumento']
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