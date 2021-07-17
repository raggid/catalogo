from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.schemas.tech_spec_schemas import TechSpecBase, TechSpec
from app.services import tech_spec_service
from app.database.database import get_db

router = APIRouter(prefix='/techSpecs', tags=['TechSpecs'])


@router.get('/', response_model=List[TechSpec])
async def get_all_tech_specs(db: Session = Depends(get_db)):
    tech_specs = tech_spec_service.get_all_tech_specs(db)

    return tech_specs


@router.get('/{spec_id}', response_model=TechSpec)
async def get_tech_spec_by_id(spec_id: int, db: Session = Depends(get_db)):
    return tech_spec_service.get_tech_spec_by_id(db, spec_id)


@router.post('/', response_model=TechSpec)
async def create_tech_spec(tech_spec: TechSpecBase, db: Session = Depends(get_db)):
    db_spec = tech_spec_service.get_tech_spec(db, tech_spec)
    if db_spec:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Technical specification already exists")
    return tech_spec_service.create_tech_spec(db, tech_spec)


@router.put('/{spec_id}', response_model=TechSpec)
async def update_tech_spec(spec_id: int, tech_spec: TechSpec, db: Session = Depends(get_db)):
    return tech_spec_service.update_tech_spec(db, spec_id, tech_spec)


@router.delete('/{spec_id}')
async def delete_tech_spec(spec_id: int, db: Session = Depends(get_db)):
    return tech_spec_service.delete_tech_spec(db, spec_id)
