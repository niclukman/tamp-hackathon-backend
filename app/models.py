from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from geoalchemy2 import Geometry
from app.db import Base

class Base(DeclarativeBase):
    pass

class Rack(Base):
    __tablename__ = "racks"
    
    id = Column("ogc_fid", Integer, primary_key=True)
    name = Column("description", String)
    type = Column(String)
    count = Column(Integer)
    sheltered = Column(Boolean)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
