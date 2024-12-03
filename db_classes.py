from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


Base = declarative_base()

class TipoEnum(enum.Enum):
    Yacimiento_arqueologico = "Yacimiento arqueológico"
    Iglesia_Ermita = "Iglesia_Ermita"
    Monasterio_Convento = "Monasterio_Convento"
    Castillo_Fortaleza_Torre = "Castillo_Fortaleza_Torre"
    Edificio_Singular = "Edificio_Singular"
    Puente = "Puente"
    Otros = "Otros"

class Provincia(Base):
    __tablename__ = 'Provincia'
    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    localidades = relationship("Localidad", back_populates="provincia")

class Localidad(Base):
    __tablename__ = 'Localidad'
    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    provincia_codigo = Column(Integer, ForeignKey('Provincia.codigo'), nullable=False)
    provincia = relationship("Provincia", back_populates="localidades")
    monumentos = relationship("Monumento", back_populates="localidad")

class Monumento(Base):
    __tablename__ = 'Monumento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoEnum), nullable=False)
    direccion = Column(String(255), nullable=True)
    codigo_postal = Column(String(10), nullable=True)
    longitud = Column(Float, nullable=True)
    latitud = Column(Float, nullable=True)
    descripcion = Column(Text, nullable=True)

    localidad_codigo = Column(Integer, ForeignKey('Localidad.codigo'), nullable=False)
    localidad = relationship("Localidad", back_populates="monumentos")
