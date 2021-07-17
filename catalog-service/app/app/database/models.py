from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint, DateTime, text, UniqueConstraint
from sqlalchemy.orm import relationship


class BaseData(object):
    id = Column(Integer, primary_key=True, index=True)

    status = Column(String, CheckConstraint("status in ('Ativo', 'Inativo')"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Product(BaseData, Base):
    __tablename__ = 'product'

    provider_code = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)
    product_code = Column(String, unique=True, nullable=False)
    product_description = Column(String, nullable=False)
    product_model = Column(String)
    observation = Column(String)

    def update(self, id, provider_code, provider_name, product_code, product_description, product_model, observation,
               status):
        self.product_code = product_code
        self.provider_code = provider_code
        self.provider_name = provider_name
        self.product_code = product_code
        self.product_description = product_description
        self.product_model = product_model
        self.observation = observation
        self.status = status


class TechSpec(BaseData, Base):
    __tablename__ = 'tech_spec'

    spec_name = Column(String, index=True, nullable=False)
    spec_value = Column(String, nullable=False)
    spec_unit = Column(String)

    def update(self, id, spec_name, spec_value, spec_unit, status):
        self.spec_name = spec_name
        self.spec_value = spec_value
        self.spec_unit = spec_unit
        self.status = status


class ProductTechSpec(BaseData, Base):
    __tablename__ = 'product_tech_spec'

    product_id = Column(Integer, ForeignKey('product.id'))
    tech_spec_id = Column(Integer, ForeignKey('tech_spec.id'))

    UniqueConstraint(product_id, tech_spec_id, name='unique_product_spec')

    show = Column(Boolean)

    product = relationship('Product', backref='product_specs')
    tech_spec = relationship('TechSpec', backref='spec_products')

    def update(self, show: bool, status: str):
        self.show = show
        self.status = status


# class Vehicle(BaseData, Base):
#     __tablename__ = 'vehicle'
#
#     brand = Column(String, nullable=False)
#     name = Column(String, nullable=False)
#     model = Column(String, nullable=False)
#     engine_id = Column(Integer, ForeignKey('engine.id'))
#     axis_id = Column(Integer, ForeignKey('axis.id'))
#     transmission_id = Column(Integer, ForeignKey('transmission.id'))
#     axis_distance = Column(Integer)
#     production_start = Column(Integer)
#     production_end = Column(Integer)
