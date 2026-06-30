from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/log", tags=["log"])


@router.post("/activity", response_model=schemas.LogEntryOut)
def log_activity(data: schemas.LogActivityIn, db: Session = Depends(get_db)):
    entry = crud.create_activity_log(db, user_id=1, data=data)
    if not entry:
        raise HTTPException(status_code=404, detail="Activity not found")
    return entry


@router.post("/pattern", response_model=schemas.LogEntryOut)
def log_pattern(data: schemas.LogPatternIn, db: Session = Depends(get_db)):
    entry = crud.create_pattern_log(db, user_id=1, data=data)
    if not entry:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return entry


@router.post("/daily-bonus", response_model=schemas.LogEntryOut)
def claim_daily_bonus(db: Session = Depends(get_db)):
    entry = crud.claim_daily_bonus(db, user_id=1)
    if not entry:
        raise HTTPException(status_code=400, detail="Daily bonus already claimed today")
    return entry


@router.delete("/{entry_id}")
def delete_log_entry(entry_id: int, db: Session = Depends(get_db)):
    success = crud.delete_log_entry(db, entry_id=entry_id, user_id=1)
    if not success:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return {"deleted": True}
