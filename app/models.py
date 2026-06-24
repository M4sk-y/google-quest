from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Activity(Base):
    __tablename__ = "activities"
    id = Column(String, primary_key=True)
    label = Column(String, nullable=False)
    xp = Column(Integer, nullable=False)
    emoji = Column(String, nullable=False)
    category = Column(String, nullable=False)


class Pattern(Base):
    __tablename__ = "patterns"
    id = Column(String, primary_key=True)
    label = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    target = Column(Integer, nullable=False)


class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    xp = Column(Integer, nullable=False)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=True)
    pattern_id = Column(String, ForeignKey("patterns.id"), nullable=True)
    problem_name = Column(String, nullable=True)
    label = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    source = Column(String, nullable=False, default="manual")
    created_at = Column(DateTime, default=datetime.utcnow)
