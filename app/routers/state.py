from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["state"])


@router.get("/state", response_model=schemas.StateOut)
def get_state(db: Session = Depends(get_db)):
    return crud.get_state(db, user_id=1)
