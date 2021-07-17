from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.product_schemas import ProductBase, Product, ProductWithSpecs
from app.services import product_service

router = APIRouter(prefix='/products', tags=['Product'])


@router.get('/', response_model=List[ProductWithSpecs])
async def get_all_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get('/{product_id}', response_model=ProductWithSpecs)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)


@router.post('/', response_model=Product)
async def create_product(product: ProductBase, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)


@router.put('/{product_id}', response_model=Product)
async def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    return product_service.update_product(db, product_id, product)


@router.delete('/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, product_id)
    return {}


@router.post('/{product_id}/add_spec/{spec_id}', response_model=ProductWithSpecs)
async def add_spec_to_product(product_id: int, spec_id: int, show: bool = True, db: Session = Depends(get_db)):
    return product_service.add_spec_to_product(db, product_id, spec_id, show)
