from fastapi import HTTPException

from app.database.models import TechSpec
from app.schemas.tech_spec_schemas import TechSpecBase
from app.schemas.data_status_enum import DataStatus
from sqlalchemy.orm import Session


def get_tech_spec_by_id(db: Session, spec_id: int) -> TechSpec:
    db_spec = db.get(TechSpec, spec_id)
    if not db_spec:
        raise HTTPException(status_code=404, detail="Specification not found")
    return db_spec


def get_tech_spec_by_name(db: Session, spec_name: str):
    return db.query(TechSpec).filter(TechSpec.spec_name == spec_name).all()


def get_tech_spec(db: Session, tech_spec: TechSpecBase):
    return db.query(TechSpec) \
        .filter(TechSpec.spec_name == tech_spec.spec_name) \
        .filter(TechSpec.spec_value == tech_spec.spec_value) \
        .filter(TechSpec.spec_unit == tech_spec.spec_unit) \
        .first()


def get_all_tech_specs(db: Session):
    return db.query(TechSpec).order_by(TechSpec.spec_name).all()


def create_tech_spec(db: Session, tech_spec: TechSpecBase):
    new_spec = TechSpec(**tech_spec.dict(), status=DataStatus.active)
    db.add(new_spec)
    db.commit()
    db.refresh(new_spec)
    return new_spec


def update_tech_spec(db: Session, spec_id: int, tech_spec: TechSpecBase):
    db_spec = get_tech_spec_by_id(db, spec_id)
    db_spec.update(**tech_spec.dict())
    db.commit()
    return db_spec


def delete_tech_spec(db, spec_id):
    db_spec = get_tech_spec_by_id(db, spec_id)
    db_spec.status = DataStatus.inactive
    for product in db_spec.spec_products:
        product.status = DataStatus.inactive
    db.commit()
