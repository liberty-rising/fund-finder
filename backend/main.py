from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine
from update_data import update_grants_tenders

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


@app.get("/businesses/", response_model=list[schemas.Business])
def read_businesses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    businesses = crud.get_businesses(db, skip=skip, limit=limit)
    return businesses


@app.delete("/businesses/{business_id}", response_model=schemas.Business)
def delete_business(business_id: int, db: Session = Depends(get_db)):
    db_business = crud.delete_business(db, business_id=business_id)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business


@app.post("/update-data/")
async def update_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_grants_tenders)
    return {"message": "Data update started in the background"}


@app.get("/grants-tenders/", response_model=List[schemas.EUFT])
def read_grants_tenders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grants_tenders = crud.get_grants_tenders(db, skip=skip, limit=limit)
    return [
        schemas.EUFT(
            **{k: v for k, v in grant_tender.__dict__.items() if v is not None}
        )
        for grant_tender in grants_tenders
    ]
