from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BusinessBase(BaseModel):
    name: str
    industry: str
    size: str
    annual_revenue: float


class BusinessCreate(BusinessBase):
    pass


class Business(BusinessBase):
    id: int

    class Config:
        from_attributes = True


class EUFTBase(BaseModel):
    identifier: str
    title: str
    description: str
    keywords: Optional[str] = None
    fund_type: str
    links: str
    status: str
    call_identifier: str
    topic_identifier: str
    topic_conditions: str
    budget: str
    start_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None


class EUFTCreate(EUFTBase):
    pass


class EUFT(EUFTBase):
    id: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
