from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# ── Inputs (what the frontend sends us) ──────────────────────────


class LogActivityIn(BaseModel):
    activity_id: str


class LogPatternIn(BaseModel):
    pattern_id: str
    problem_name: str


# ── Outputs (what we send back) ──────────────────────────────────


class ActivityOut(BaseModel):
    id: str
    label: str
    xp: int
    emoji: str
    category: str

    class Config:
        from_attributes = True


class PatternOut(BaseModel):
    id: str
    label: str
    emoji: str
    target: int

    class Config:
        from_attributes = True


class LogEntryOut(BaseModel):
    id: int
    date: date
    xp: int
    label: str
    emoji: str
    source: str
    activity_id: Optional[str] = None
    pattern_id: Optional[str] = None
    problem_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PatternProgress(BaseModel):
    pattern_id: str
    label: str
    emoji: str
    target: int
    count: int
    last_touched: Optional[date] = None
    records: list[str]


class StateOut(BaseModel):
    total_xp: int
    streak: int
    max_streak: int
    xp_by_date: dict[str, int]
    counts: dict[str, int]
    pattern_progress: list[PatternProgress]
    recent_log: list[LogEntryOut]
    daily_bonus_claimed: bool
