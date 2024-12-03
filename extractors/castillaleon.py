from postal_codes import provincias
from wrappers import Wrapper_CAT
import json

url = 'data-sources/Entrega1/monumentos.xml'

wrapper = Wrapper_CAT(url)

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
    "Yacimiento arqueologico": [
        "Yacimientos arqueológicos"
    ],
    "Iglesia-Ermita": [
        "Iglesias y Ermitas",
        "Catedrales",
        "Santuarios"
    ],
    "Monasterio-Convento": [
        "Monasterios"
    ],
    "Castillo-Fortaleza-Torre": [
        "Castillos",
        "Torres"
    ],
    "Edificio Singular": [
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
provinid = 0
localid = 0
province_gen = 'provincia'
locality_gen = 'localidad'


def extractorter(jsonkey : str,extractorkey : str,en_provincia : int = None) -> int:
    dataList = extractor.setdefault(extractorkey,[]) #Obtain the extractor value from the key from reference
    # if made if it is a province, if not its a locality
    nameList = monumentData[jsonkey].split(' ')[0] if jsonkey == province_gen else monumentData[jsonkey] #Get the name of the reference
    jsonn = list(map(lambda x: x['nombre'] == nameList,dataList)) #Make a boolean list to sort out if there the reference already exists
    if not any(jsonn):
        idd = len(dataList)
        dataList.append({'codigo' : idd,'nombre' : nameList})
        if extractorkey == 'localities':
            dataList[-1].update({'en_provincia' : en_provincia})
        print(f'Created {jsonkey} with id: {idd}')
    else:
        idd = dataList[jsonn.index(True)]['codigo'] #Get reference which already exists in the database
    return idd


def ensureinformation(data : dict) -> bool:
    longitud = ''.join(c for c in data['longitud'] if c.isdigit() or c == '.')
    latitud = ''.join(c for c in data['latitud'] if c.isdigit() or c == '.')
    if list(data.values()).count('') > 0:
        return False
    elif float(longitud) < -90 or float(latitud) < -90 or float(longitud) > 90 or float(latitud) > 90:
        return False
    for locality in extractor['localities']:
        if locality['codigo'] == data['en_localidad']:
            for province in extractor['provinces']:
                if province['codigo'] == locality['en_provincia']:
                    return len(data['codigo_postal']) == 5 and provincias[data['codigo_postal'][:2]] in province['nombre']


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
    typo = monumentData['tipoMonumento']
    for j in typeScheme:
        if typo in typeScheme[j]:
            aux.update({'tipo' : j})
            break
    
    m = extractor.setdefault('monuments',[])

    if ensureinformation(aux):
        m.append(aux)
        print('Created monument: ' + aux['nombre'])

# print(len(extractor['monuments']))

with open('castillaleon.json','w+',encoding='utf-8') as f:
    json.dump(extractor,f,indent=4,ensure_ascii=True)