from typing import List

from app.database import models
from app.schemas.product_schemas import ProductBase, Product, DataStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.services import tech_spec_service


def get_product_by_id(db: Session, product_id) -> models.Product:
    db_product = db.get(models.Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


def get_product_by_code(db: Session, product_code) -> models.Product:
    return db.query(models.Product).filter(models.Product.product_code == product_code).first()


def get_all_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).all()


def create_product(db: Session, product: ProductBase) -> models.Product:
    product_in_db = get_product_by_code(db, product.product_code)
    if product_in_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")
    db_product = models.Product(**product.dict(), status=DataStatus.active)
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except Exception as err:
        print(err.args[0])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_product


def update_product(db: Session, product_id: int, product: Product) -> models.Product:
    db_product = get_product_by_id(db, product_id)
    db_product.update(**product.dict())
    try:
        db.commit()
        db.refresh(db_product)
    except Exception as err:
        print(err.args[0])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    db_product.status = DataStatus.inactive
    for spec in db_product.product_spec:
        spec.status = DataStatus.inactive
    try:
        db.commit()
    except Exception as err:
        print(err.args[0])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')


def add_spec_to_product(db: Session, product_id, tech_spec_id, show) -> models.Product:
    db_product = get_product_by_id(db, product_id)
    db_spec = tech_spec_service.get_tech_spec_by_id(db, tech_spec_id)
    product_spec = models.ProductTechSpec(status = DataStatus.active, show = show)
    product_spec.tech_spec = db_spec
    db_product.product_specs.append(product_spec)
    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Spec already added to product')
    return db_product

