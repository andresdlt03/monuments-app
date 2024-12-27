from . import wrappers
from . import postal_codes
import json
from selenium import webdriver
from . import webdriverselenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

provincias = postal_codes.provincias

def get_valencia(pId : int = 0,lId : int = 0) -> list:
    url = 'data-sources/Entrega1/bienes_inmuebles_interes_cultural.csv'

    wrapper = wrappers.Wrapper_CV(url)

    data= wrapper.get_data()

    service = webdriverselenium.WebDriverService().get_service()

    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--window-size=1920x1080")  # Set window size for rendering
    options.add_argument("--no-sandbox")  # Required for some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Address shared memory issues
    driver = webdriver.Chrome(service=service,options=options)

    wait = WebDriverWait(driver, 10)

    def get_direction(UTMNORTE,UTMESTE):
        try:
            driver.get('https://icv.gva.es/auto/aplicaciones/geocodificador/')
            input_X = driver.find_element(By.ID, 'input_12')
            input_Y = driver.find_element(By.ID, 'input_13')
            input_X.send_keys(UTMNORTE)
            input_Y.send_keys(UTMESTE + Keys.RETURN)
            wait = WebDriverWait(driver, 10)
            divs = wait.until(lambda d: [div for div in d.find_elements(By.CSS_SELECTOR, '.direccion.ng-binding') if div.text != ''])
            a = divs[0].text.split('\n')[1].split(':')[1].strip()
            Municipio = driver.find_element(By.ID, 'select_3')
            Municipio.click()
            
            wait.until(EC.element_to_be_clickable((By.ID, "select_option_2"))).click()
            
            direction = driver.find_element(By.ID, 'input-5')
            direction.send_keys(a.split(',')[0])
            time.sleep(1)
            driver.execute_script('arguments[0].focus()',direction)
            first_li = wait.until(
                EC.presence_of_element_located((By.XPATH, "//ul[@id='ul-5']/li[1]//span"))
            )
            first_li.click()
            divs = wait.until(lambda d: [div for div in d.find_elements(By.CSS_SELECTOR, '.direccion.ng-binding') if div.text != ''])
            longitud, latitud = divs[0].text.split('\n')[2].split(':')[2].strip().split(' ')
        except Exception as e:
            a = ''
            longitud = ''
            latitud = ''
            raise e
        return {'direccion' : a,'longitud' : longitud, 'latitud' : latitud}
    
    def get_description(name):
        driver.get('https://www.google.com')
        
        # time.sleep(100)
        try:   
            cookie = driver.find_element(By.ID, 'L2AGLb')
            cookie.click()
        except Exception as e:
            pass
        try:
            search = driver.find_element(By.NAME, 'q')
            search.send_keys(name)
            search.send_keys(Keys.RETURN)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
            description = driver.find_element(By.CSS_SELECTOR, '.kno-rdesc span').text
        except:
            description = ''
        try:
            postalCode = driver.find_element(By.CSS_SELECTOR, '.gqkR3b.hP3ybd').text
            s = [c for c in postalCode.split(' ') if c.isdigit()]
        except:
            s = ''
        return {'descripcion' : description,'codigo_postal' : s[0] if len(s) > 0 else ''}

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


    # def get_information(norte, este):
    #     utm_x = int(norte)
    #     utm_y = int(este)
    #     try:
    #         longitude, latitude = transformer.transform(utm_x, utm_y)
    #         location = reverse(f'{latitude} , {longitude}')
    #     except:
    #         return {'longitud' : '', 'latitud' : '', 'direccion' : '', 'codigo_postal' : ''}
    #     address = list(map(lambda x : x.strip(), location.address.split(',')))
    #     p = list(filter(lambda x: x.isdigit(),address))
    #     codigo_postal = p[0] if len(p) > 0 else ''
    #     direccion = address[1]   
    #     return {'longitud' : str(longitude), 'latitud' : str(latitude), 'direccion' : direccion, 'codigo_postal' : codigo_postal}


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

        aux.update(get_direction(monumentData['UTMNORTE'],monumentData['UTMESTE'])) 
        aux.update(get_description(monumentData['DENOMINACION']))
        if aux['descripcion'] == '':
            aux.update({'descripcion' : monumentData['CATEGORIA']})
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

if __name__ == '__main__':
    dicc, _,_ = get_valencia()
    with open('valenciana_prove.json','w+') as f:
        json.dump(dicc,f,indent=4)