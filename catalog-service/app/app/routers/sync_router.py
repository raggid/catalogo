from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services import sync_service
from app.database.database import get_db
from app.dependencies import get_es_node

router = APIRouter(prefix='/sync', tags=['Syncronization'])


@router.post('/{product_id}')
async def syncronize_product(product_id: int, db: Session = Depends(get_db), es = Depends(get_es_node)):
    return sync_service.sync_product(db, es, product_id)
