from pydantic import BaseModel
from typing import Optional

class MURDocument(BaseModel):
    documentName: str
    documentDescription: Optional[str] = None
    templateType: str
    locality: Optional[str] = None
    qualityQ: Optional[str] = None
    qualityIconURL: Optional[str] = None
    qualityIconDescription: Optional[str] = None
    accesibility: Optional[str] = None
    accesibilityIconURL: Optional[str] = None
    accesibilityIconDescription: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    marks: Optional[str] = None
    physical: Optional[str] = None
    visual: Optional[str] = None
    auditive: Optional[str] = None
    intellectual: Optional[str] = None
    organic: Optional[str] = None
    qualityAssurance: Optional[str] = None
    tourismEmail: Optional[str] = None
    web: Optional[str] = None
    importance: Optional[str] = None
    room: Optional[str] = None
    productClub: Optional[str] = None
    visit: Optional[str] = None
    capacity: Optional[str] = None
    store: Optional[str] = None
    gastronomical: Optional[str] = None
    surfing: Optional[str] = None
    postalCode: Optional[str] = None
    cultureType: Optional[str] = None
    cultureSubtype: Optional[str] = None
    latitudelongitude: Optional[str] = None
    latwgs84: Optional[str] = None
    lonwgs84: Optional[str] = None
    placename: Optional[str] = None
    municipality: Optional[str] = None
    municipalitycode: Optional[str] = None
    postalcode: Optional[str] = None
    territory: Optional[str] = None
    territorycode: Optional[str] = None
    country: Optional[str] = None
    countrycode: Optional[str] = None
    friendlyUrl: Optional[str] = None
    physicalUrl: Optional[str] = None
    dataXML: Optional[str] = None
    metadataXML: Optional[str] = None
    zipFile: Optional[str] = None

class CVDocument(BaseModel):
    IGPCV: Optional[str] = None
    DENOMINACION: Optional[str] = None
    PROVINCIA: Optional[str] = None
    MUNICIPIO: Optional[str] = None
    UTMESTE: Optional[str] = None
    UTMNORTE: Optional[str] = None
    CODCLASIFICACION: Optional[str] = None
    CLASIFICACION: Optional[str] = None
    CODCATEGORIA: Optional[str] = None
    CATEGORIA: Optional[str] = None

class CATDocument(BaseModel):
    identificador: Optional[str] = None
    nombre: Optional[str] = None
    tipoMonumento: Optional[str] = None
    identificadosBienInteresCultural: Optional[str] = None
    calle: Optional[str] = None
    clasificacion: Optional[str] = None
    tipoConstruccion: Optional[str] = None
    codigoPostal: Optional[str] = None
    Descripcion: Optional[str] = None
    periodoHistorico: Optional[str] = None
    class Poblacion(BaseModel):
        provincia: Optional[str] = None
        municipio: Optional[str] = None
        localidad: Optional[str] = None

    poblacion: Optional[Poblacion] = None
    class Coordenadas(BaseModel):
        latitud: Optional[str] = None
        longitud: Optional[str] = None
    coordenadas: Optional[Poblacion] = None

