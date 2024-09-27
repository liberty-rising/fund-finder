from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


def get_business(db: Session, business_id: int):
    return db.query(models.Business).filter(models.Business.id == business_id).first()


def get_businesses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Business).offset(skip).limit(limit).all()


def create_business(db: Session, business: schemas.BusinessCreate):
    db_business = models.Business(**business.model_dump())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def get_opportunities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Opportunity).offset(skip).limit(limit).all()


def match_opportunities(db: Session, business_id: int):
    business = get_business(db, business_id)
    if not business:
        return []

    # Implement matching logic here
    # This is a simple example, you'll need to expand on this
    return (
        db.query(models.Opportunity)
        .filter(models.Opportunity.eligibility_criteria.contains(business.industry))
        .all()
    )


def create_or_update_grant_tender(db: Session, grant_tender: schemas.EUFTCreate):
    db_grant_tender = (
        db.query(models.EUFT)
        .filter(models.EUFT.identifier == grant_tender.identifier)
        .first()
    )
    if db_grant_tender:
        for key, value in grant_tender.model_dump().items():
            setattr(db_grant_tender, key, value)
        db_grant_tender.last_updated = datetime.utcnow()
    else:
        db_grant_tender = models.EUFT(
            **grant_tender.model_dump(), last_updated=datetime.utcnow()
        )
        db.add(db_grant_tender)
    db.commit()
    db.refresh(db_grant_tender)
    return db_grant_tender


def get_grants_tenders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EUFT).offset(skip).limit(limit).all()


def delete_business(db: Session, business_id: int):
    business = (
        db.query(models.Business).filter(models.Business.id == business_id).first()
    )
    if business:
        db.delete(business)
        db.commit()
    return business
