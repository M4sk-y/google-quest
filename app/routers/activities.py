from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["activities"])


@router.get("/activities", response_model=list[schemas.ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    return crud.get_activities(db)


@router.get("/patterns", response_model=list[schemas.PatternOut])
def list_patterns(db: Session = Depends(get_db)):
    return crud.get_patterns(db)
