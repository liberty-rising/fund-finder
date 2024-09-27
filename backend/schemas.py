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


class OpportunityBase(BaseModel):
    title: str
    type: str
    description: str
    amount: float
    eligibility_criteria: str


class OpportunityCreate(OpportunityBase):
    pass


class Opportunity(OpportunityBase):
    id: int

    class Config:
        from_attributes = True


class EUFTBase(BaseModel):
    identifier: str
    title: str
    description: str
    status: str
    call_identifier: str
    topic_identifier: str
    publication_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None


class EUFTCreate(EUFTBase):
    pass


class EUFT(EUFTBase):
    id: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
