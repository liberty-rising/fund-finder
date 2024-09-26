from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String, index=True)
    size = Column(String)
    annual_revenue = Column(Float)

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String, index=True)  # grant, tender, or loan
    description = Column(String)
    amount = Column(Float)
    eligibility_criteria = Column(String)