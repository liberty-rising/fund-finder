from sqlalchemy.orm import Session
import models, schemas

def get_business(db: Session, business_id: int):
    return db.query(models.Business).filter(models.Business.id == business_id).first()

def create_business(db: Session, business: schemas.BusinessCreate):
    db_business = models.Business(**business.dict())
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
    return db.query(models.Opportunity).filter(
        models.Opportunity.eligibility_criteria.contains(business.industry)
    ).all()