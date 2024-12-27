# from . import (wrappers,postal_codes)
import wrappers
import postal_codes
from methods import Extractor
import json

provincias = postal_codes.provincias

def get_euskadi(pId : int = 0,lId : int = 0) -> list:
    url = 'data-sources/Entrega1/edificios.json'

    EUS = wrappers.Wrapper_MUR(url)

    data = EUS.get_data()

    mappingScheme = {
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

    extractor = {}
    PROVINID = pId
    LOCALID = lId
    provinid = pId
    localid = lId
    '''Generilized variables'''
    province_gen = 'territory'
    locality_gen = 'locality'
    ''''''

    # def extractorter(jsonkey : str,extractorkey : str,en_provincia : int = None) -> int:
    #     dataList = extractor.setdefault(extractorkey,{}) #Obtain the extractor value from the key from reference
    #     # if made if it is a province, if not its a locality
    #     nameList = monumentData[jsonkey].split(' ')[0] if jsonkey == province_gen else monumentData[jsonkey] #Get the name of the reference
    #     jsonn = [key for key, value in dataList.items() if value['nombre'] == nameList]
    #     #Make a boolean list to sort out if there the reference already exists list(filter(lambda x: dataList[x]['nombre'] == nameList,dataList))
    #     if not len(jsonn) > 0:
    #         idd = LOCALID + len(dataList) if extractorkey == 'localities' else PROVINID + len(dataList)
    #         dataList.update({idd : {'nombre' : nameList}})
    #         if extractorkey == 'localities':
    #             dataList[idd].update({'en_provincia' : en_provincia})
    #         print(f'Created {jsonkey} with id: {idd} and name: {nameList}')
    #     else:
    #         idd =  jsonn[0] #Get reference which already exists in the database
    #     return idd


    # def ensureinformation(data : dict) -> bool:
    #     longitud = ''.join(c for c in data['longitud'] if c.isdigit() or c == '.' or c == '-')
    #     latitud = ''.join(c for c in data['latitud'] if c.isdigit() or c == '.' or c == '-')
    #     ensure = list(data.values()).count('') > 0 or float(longitud) < -90 or float(latitud) < -90 or float(longitud) > 90 or float(latitud) > 90 or int(data['codigo_postal'][:2]) < 1 or int(data['codigo_postal'][:2]) > 52
    #     if ensure:
    #         return False
    #     for locality in extractor['localities']:
    #         if locality == data['en_localidad']:
    #             for province in extractor['provinces']:
    #                 if province == extractor['localities'][locality]['en_provincia']:
    #                     return len(data['codigo_postal']) == 5 and provincias[data['codigo_postal'][:2]].lower() in extractor['provinces'][province]['nombre'].lower()


    extr = Extractor(province_gen,extractor,LOCALID,PROVINID)

    for monumentData in data:
        #province transform
        if province_gen in monumentData and monumentData[province_gen] != '':
            provinid = extr.get_province_locality(province_gen,monumentData)
        #locality transform
        if locality_gen in monumentData and monumentData[locality_gen] != '':
            localid = extr.get_province_locality(locality_gen,monumentData,provinid)
        #monument transform
        aux = {}
        for j in mappingScheme:
            aux.update({mappingScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mappingScheme[j] : ""})                   
        aux.update({'en_localidad' : localid})

        #tipoMonumento
        typo = monumentData['documentName'].split(' ')[0]
        for j in typeScheme:
            if typo in typeScheme[j]:
                aux.update({'tipo' : j})
                break
        
        if 'tipo' not in aux:
            aux.update({'tipo' : 'Otros'})

        m = extractor.setdefault('monuments',[])
        try:
            extr.ensureinformation(aux)
            extr.postal_code_verification(localid,aux['codigo_postal'])
            m.append(aux)
            print('Created MONUMENT: ' + aux['nombre'])
        except Exception as e:
            print(e)

    return [extractor,provinid,localid]

if __name__ == '__main__':
    with open('euskadi_prove.json','w+',encoding='utf-8') as f:
        json.dump(get_euskadi()[0],f,ensure_ascii=False,indent=4)