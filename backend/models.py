from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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


class EUFT(Base):
    __tablename__ = "eu_funding_tenders"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    call_identifier = Column(String)
    topic_identifier = Column(String)
    publication_date = Column(DateTime, nullable=True)
    deadline_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
