from postal_codes import provincias
class Extractor:
    def __init__(self,province_gen,data_dict,localId,provinId):
        self.province_gen = province_gen
        self.data_dict = data_dict
        self.localID = localId
        self.provinID = provinId
    
    def get_province_locality(self, jsonkey : str, original_data,from_province : int = None) -> int:
        extractorkey = 'provinces' if from_province else 'localities'
        dataList =  self.data_dict.setdefault(extractorkey,{})
        nameList = original_data[jsonkey].split(' ')[0] if jsonkey == self.province_gen else original_data[jsonkey]
        jsonn = [key for key, value in dataList.items() if value['nombre'] == nameList]

        if not len(jsonn) > 0:
            idd = self.localID + len(dataList) if from_province else self.provinID + len(dataList)
            dataList.update({idd : {'nombre' : nameList}})
            if from_province:
                dataList[idd].update({'en_provincia' : from_province})
            print(f'Created {jsonkey} with id: {idd} and name: {nameList}')
        else:
            idd =  jsonn[0]
        return idd
    
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
    
    @property
    def get_extractor(self):
        return self.data_dict
    
    def ensureinformation(self,monument : dict) -> bool:
        longitud = ''.join(c for c in monument['longitud'] if c.isdigit() or c == '.' or c == '-')
        latitud = ''.join(c for c in monument['latitud'] if c.isdigit() or c == '.' or c == '-')
        if list(monument.values()).count('') > 0:
            raise Exception('Empty values in the monument')
        elif float(longitud) < -90 or float(latitud) < -90 or float(longitud) > 90 or float(latitud) > 90:
            raise Exception('Invalid coordinates')
        elif int(monument['codigo_postal'][:2]) < 1 or int(monument['codigo_postal'][:2]) > 52:
            raise Exception('Invalid postal code')

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

    def postal_code_verification(self,from_locality: int,postal_code : int):
        from_province = self.data_dict['localities'][from_locality]['en_provincia']
        if not len(postal_code) == 5 and provincias[postal_code[:2]].lower() in self.data_dict['provinces'][from_province]['nombre'].lower():
            raise Exception('Invalid postal code')
       
# #euskadi      
# for monumentData in data:
#     #province transform
#     if province_gen in monumentData and monumentData[province_gen] != '':
#         provinid = extractorter(province_gen,'provinces')
#     #locality transform
#     if locality_gen in monumentData and monumentData[locality_gen] != '':
#         localid = extractorter(locality_gen,'localities',provinid)
#     #monument tranform
#     aux = {}
#     for j in mScheme:
#         aux.update({mScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mScheme[j] : ""})                   
#     aux.update({'en_localidad' : localid})

#     #tipoMonumento
#     typo = monumentData['documentName'].split(' ')[0]
#     for j in typeScheme:
#         if typo in typeScheme[j]:
#             aux.update({'tipo' : j})
#             break
    
#     if 'tipo' not in aux:
#         aux.update({'tipo' : 'Otros'})

#     m = extractor.setdefault('monuments',[])

#     if ensureinformation(aux):
#         m.append(aux)
#         print('Created MONUMENT: ' + aux['nombre'])

# #return [extractor,provinid,localid]
# #Valenciana
# for monumentData in data:
#     #province transform
#     if province_gen in monumentData and monumentData[province_gen] != '':
#         provinid = extractorter(province_gen,'provinces')
#     # locality transform
#     if locality_gen in monumentData and monumentData[locality_gen] != '':
#         localid = extractorter(locality_gen,'localities',provinid)
#     #monument tranform
#     aux = {}
#     for j in mScheme:
#         aux.update({mScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mScheme[j] : ""})

#     aux.update(get_information(monumentData['UTMNORTE'],monumentData['UTMESTE']))               
#     aux.update({'en_localidad' : localid})

#     '''change on typo'''
#     typo = monumentData['DENOMINACION'].split(' ')[0]
#     for j in typeScheme:
#         if typo in typeScheme[j]:
#             aux.update({'tipo' : j})
#             break

#     if 'tipo' not in aux:
#         aux.update({'tipo' : 'Otros'})
    
#     m = extractor.setdefault('monuments',[])

#     if ensureinformation(aux):
#         m.append(aux)
#         print('Created MONUMENT: ' + aux['nombre'])


# # return [extractor,provinid,localid]
# #castilla leon
# for monumentData in data:
#     #province transform
#     if province_gen in monumentData and monumentData[province_gen] != '':
#         provinid = extractorter(province_gen,'provinces')
#     # locality transform
#     if locality_gen in monumentData and monumentData[locality_gen] != '':
#         localid = extractorter(locality_gen,'localities',provinid)
#     #monument tranform
#     aux = {}
#     for j in mScheme:
#         aux.update({mScheme[j] : monumentData[j]}) if j in monumentData else aux.update({mScheme[j] : ""})                   
#     aux.update({'en_localidad' : localid})

#     '''change on typo'''
#     aux['descripcion'] = re.sub(r'<[^>]*>', '', aux['descripcion'])
#     aux['descripcion'] = re.sub(r'&([a-zA-Z](acute|tilde))+;',change_to_acute, aux['descripcion'])

#     typo = monumentData['tipoMonumento']
#     for j in typeScheme:
#         if typo in typeScheme[j]:
#             aux.update({'tipo' : j})
#             break
    
#     if 'tipo' not in aux:
#         aux.update({'tipo' : 'Otros'})

#     m = extractor.setdefault('monuments',[])

#     if ensureinformation(aux):
#         m.append(aux)
#         print('Created MONUMENT: ' + aux['nombre'])

# return [extractor,provinid,localid]