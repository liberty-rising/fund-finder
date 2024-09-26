from pydantic import BaseModel

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
        orm_mode = True

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
        orm_mode = True