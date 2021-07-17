from typing import List, Optional
from pydantic import BaseModel
from app.schemas.tech_spec_schemas import TechSpec
from app.schemas.data_status_enum import DataStatus


class ProductBase(BaseModel):
    provider_code: str
    provider_name: str
    product_code: str
    product_description: str
    product_model: Optional[str] = None
    observation: Optional[str] = None


class Product(ProductBase):
    id: int
    status: DataStatus

    class Config:
        orm_mode = True


class ProductSpecs(BaseModel):
    id: int
    show: bool
    status: DataStatus
    # product: Product
    tech_spec: TechSpec

    class Config:
        orm_mode = True


class ProductWithSpecs(Product):
    product_specs: List[ProductSpecs] = []
