from typing import Optional

from pydantic import BaseModel

from app.schemas.data_status_enum import DataStatus


class TechSpecBase(BaseModel):
    spec_name: str
    spec_value: str
    spec_unit: Optional[str] = None


class TechSpec(TechSpecBase):
    id: int
    status: DataStatus

    class Config:
        orm_mode = True
