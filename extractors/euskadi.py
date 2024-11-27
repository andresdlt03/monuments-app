from postal_codes import provincias
from wrappers import Wrapper_MUR
import json
import os

cwd = os.getcwd()
print(cwd)

url = 'data-sources/edificios (euskadi).json'

EUS = Wrapper_MUR(url)

data = EUS.get_data()

mScheme = {
    'documentName' : 'nombre',
    'address' : 'direccion',
    'postalCode': 'codigo_postal',
    'lonwgs84' : 'longitud',
    'latwgs84' :'latitud',
    'documentDescription' : 'descripcion'
    }

typeScheme = {
    'Yacimiento arqueologico': [
        'Valle', 'Recinto', 'Coto', 'Calero', 'Murallas', 'Santiago', 'Archivo'
    ],
    
    'Iglesia-Ermita': [
        'Iglesia', 'Ermita', 'Catedral', 'Basílica', 'Parroquia', 'Santuario'
    ],
    
    'Monasterio-Convento': [
        'Monasterio', 'Convento', 'Cofradia'
    ],
    
    'Castillo-Fortaleza-Torre': [
        'Castillo', 'Fuerte', 'Torre', 'Torre-Palacio', 'Casa-Torre'
    ],
    
    'Edificio Singular': [
        'Canteras', 'Ferrería', 'Conjunto', 'Ciudad', 'Central', 'Arco', 'Muralla', 
        'Monumento-Homenaje', 'Vivienda', 'Pinturas', 'Altos', 'Casa', 'Jauregi', 'Viaducto', 
        'Teatro', 'Antiguo', 'Cruz', 'Hórreo', 'Balneario', 'Bilbao', 'Caserío', 'Antigua', 
        'Grandes', 'Muelle', 'Marierrota', 'Plaza', 'Faro', 'Quinta', 'Jardín', 'Bosque', 
        'Landetxo', 'Túnel', 'Funicular', 'Órgano', 'Basque', 'Fábrica', 'Ayuntamiento', 
        'Aduana', 'Mercado', 'Palacio', 'Bikuña', 'Chalet', 'Universidad', 'Edificio', 
        'Fuente', 'Cargadero', 'Auditorio', 'Paseo'
    ],
    
    'Otros': [
        'Peine', 'Parque', 'Núcleo', 'Pequeño', 'El', 'San', 'Puente', 'Molino', 'Puerta', 
        'Villa', 'Las', 'Monumento', 'Senda', 'Puerto'
    ]
}

extractor = {}
provinid = 0
localid = 0

def extractorter(jsonkey : str,extractorkey : str,en_provincia : int = None) -> int:
    dataList = extractor.setdefault(extractorkey,[]) #Obtain the extractor value from the key from reference
    nameList = monumentData[jsonkey].split(' ')[0] if jsonkey == 'territory' else monumentData[jsonkey] #Get the name of the reference
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
    if list(data.values()).count('') > 0:
        return False
    elif float(data['longitud']) < -90 or float(data['longitud']) > 90 or float(data['latitud']) < -90 or float(data['latitud']) > 90:
        return False
    for locality in extractor['localities']:
        if locality['codigo'] == data['en_localidad']:
            for province in extractor['provinces']:
                if province['codigo'] == locality['en_provincia']:
                    return len(data['codigo_postal']) == 5 and provincias[data['codigo_postal'][:2]] in province['nombre']


for monumentData in data:
    #province transform
    if 'territory' in monumentData and monumentData['territory'] != '':
        provinid = extractorter('territory','provinces')
    #locality transform
    if 'locality' in monumentData and monumentData['locality'] != '':
        localid = extractorter('locality','localities',provinid)
    #monument tranform
    aux = {}
    for j in mScheme:
        aux.update({mScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mScheme[j] : ""})                   
    aux.update({'en_localidad' : localid})

    typo = monumentData['documentName'].split(' ')[0]
    for j in typeScheme:
        if typo in typeScheme[j]:
            aux.update({'tipo' : j})
            break
    
    m = extractor.setdefault('monuments',[])

    if ensureinformation(aux):
        m.append(aux)
        print('Created monument: ' + aux['nombre'])

print(len(extractor['monuments']))

with open('euskadi.json','w+',encoding='utf-8') as f:
    json.dump(extractor,f,indent=4,ensure_ascii=True)