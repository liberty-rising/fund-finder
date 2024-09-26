from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/businesses/", response_model=schemas.Business)
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    return crud.create_business(db=db, business=business)

@app.get("/businesses/{business_id}", response_model=schemas.Business)
def read_business(business_id: int, db: Session = Depends(get_db)):
    db_business = crud.get_business(db, business_id=business_id)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business

@app.get("/opportunities/", response_model=list[schemas.Opportunity])
def read_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    opportunities = crud.get_opportunities(db, skip=skip, limit=limit)
    return opportunities

@app.post("/match/", response_model=list[schemas.Opportunity])
def match_opportunities(business_id: int, db: Session = Depends(get_db)):
    return crud.match_opportunities(db, business_id=business_id)