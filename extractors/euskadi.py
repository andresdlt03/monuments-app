import json

with open('data-sources/edificios (euskadi).json','r',encoding='utf-8') as f:
    txt = f.read()

txt = txt.replace('''"address" : "",''','')
txt = txt.replace('''"phone" : "",''','')

data = json.loads(txt)

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

def extractorter(jsonkey : str,extractorkey : str,en_provincia : int = None):
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
    
    print('Created monument: ' + aux['nombre'])
    m = extractor.setdefault('monuments',[])
    m.append(aux)


with open('prove.json','w+',encoding='utf-8') as f:
    json.dump(extractor,f,indent=4)