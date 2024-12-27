from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_classes import Base, Provincia, Localidad, Monumento, TipoEnum
from extractors.euskadi import get_euskadi
from extractors.castillaleon import get_castilla
from extractors.valenciana import get_valencia

engine = create_engine('postgresql+psycopg2://postgres.bpfzccsjzpeacovylujj:4Vzao7Qqe4u4NG2E@aws-0-eu-west-3.pooler.supabase.com:6543/postgres')

Session = sessionmaker(bind=engine)
session = Session()

# print('EUSKADI LOAD')
# euskadi, pro,loc = get_euskadi()
# print('CASTILLA Y LEON LOAD')
# castillaleon,pro,loc = get_castilla()
print('VALENCIANA LOAD')
valenciana,_,_ = get_valencia()

provinces = valenciana['provinces']
localities = valenciana['localities']
monuments = valenciana['monuments']

Base.metadata.create_all(engine)

session.query(Monumento).delete()
session.query(Localidad).delete()
session.query(Provincia).delete()
session.commit()

for cod in provinces:
    prov = Provincia(codigo=cod,nombre=provinces[cod]['nombre'].upper())
    session.add(prov)
session.commit()

for cod in localities:
    loc = Localidad(codigo=cod,nombre=localities[cod]['nombre'],provincia_codigo=localities[cod]['en_provincia'])
    session.add(loc)
session.commit()

for monument in monuments:
    monu = Monumento(nombre=monument['nombre'],tipo=TipoEnum[monument['tipo']],direccion=monument['direccion'],codigo_postal=monument['codigo_postal'],longitud=monument['longitud'],latitud=monument['latitud'],descripcion=monument['descripcion'])
    loca = session.query(Localidad).filter(Localidad.codigo == monument['en_localidad']).first()
    monu.localidad = loca
    session.add(monu)

session.commit()

session.close()

