from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship

from app.core.database import Base


class Brand(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", backref="children", remote_side=id)


class Flavour(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", backref="flavours")


class Tobacco(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    strength = Column(Integer, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)

    brand = relationship("Brand", backref="tobaccos")


class Mapping(Base):
    id = Column(Integer, primary_key=True)
    tobacco_id = Column(Integer, ForeignKey("tobaccos.id"), nullable=False)
    flavour_id = Column(Integer, ForeignKey("flavours.id"), nullable=False)

    tobacco = relationship("Tobacco", backref="mappings")
    flavour = relationship("Flavour", backref="mappings")
