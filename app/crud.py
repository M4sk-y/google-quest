from sqlalchemy.orm import Session
from datetime import date, timedelta
from app import models
from app import schemas

# ── Seed helpers ──────────────────────────────────────────────────────────────
# Called once on startup to populate activities and patterns
# if the tables are empty. This way the app works out of the box
# without needing a separate data import step.


def seed_activities(db: Session):
    if db.query(models.Activity).count() > 0:
        return
    defaults = [
        models.Activity(
            id="lc_easy", label="LeetCode Easy", xp=10, emoji="🟢", category="Coding"
        ),
        models.Activity(
            id="lc_medium",
            label="LeetCode Medium",
            xp=25,
            emoji="🟡",
            category="Coding",
        ),
        models.Activity(
            id="lc_hard", label="LeetCode Hard", xp=60, emoji="🔴", category="Coding"
        ),
        models.Activity(
            id="commit", label="GitHub Commit", xp=5, emoji="💾", category="Building"
        ),
        models.Activity(
            id="project",
            label="1hr Project Work",
            xp=15,
            emoji="🔨",
            category="Building",
        ),
        models.Activity(
            id="pr",
            label="PR Merged (Open Source)",
            xp=200,
            emoji="🌟",
            category="Building",
        ),
        models.Activity(
            id="ddia", label="DDIA Section Read", xp=20, emoji="📖", category="Learning"
        ),
        models.Activity(
            id="sysdesign",
            label="System Design Practice",
            xp=30,
            emoji="🏗️",
            category="Learning",
        ),
        models.Activity(
            id="star",
            label="STAR Story Written",
            xp=25,
            emoji="📝",
            category="Learning",
        ),
        models.Activity(
            id="cf_contest",
            label="Codeforces Contest",
            xp=75,
            emoji="⚔️",
            category="Tournaments",
        ),
        models.Activity(
            id="lc_contest",
            label="LeetCode Weekly Contest",
            xp=75,
            emoji="🏆",
            category="Tournaments",
        ),
        models.Activity(
            id="mock_free",
            label="Mock Interview (Pramp)",
            xp=100,
            emoji="🎯",
            category="Interview",
        ),
        models.Activity(
            id="mock_paid",
            label="Mock Interview (Paid)",
            xp=200,
            emoji="🔱",
            category="Interview",
        ),
        models.Activity(
            id="freelance",
            label="Freelance Work (1hr)",
            xp=20,
            emoji="💼",
            category="Industry",
        ),
        models.Activity(
            id="client",
            label="New Client Secured",
            xp=500,
            emoji="🤝",
            category="Industry",
        ),
    ]
    db.add_all(defaults)
    db.commit()


def seed_patterns(db: Session):
    if db.query(models.Pattern).count() > 0:
        return
    defaults = [
        models.Pattern(id="arrays", label="Arrays & Hashing", emoji="📦", target=15),
        models.Pattern(id="twoptr", label="Two Pointers", emoji="👉", target=10),
        models.Pattern(id="sliding", label="Sliding Window", emoji="🪟", target=10),
        models.Pattern(id="binsearch", label="Binary Search", emoji="🔍", target=12),
        models.Pattern(id="trees", label="Trees", emoji="🌳", target=20),
        models.Pattern(id="graphs", label="Graphs (BFS/DFS)", emoji="🕸️", target=15),
        models.Pattern(id="dp", label="Dynamic Programming", emoji="🔢", target=20),
        models.Pattern(id="backtrack", label="Backtracking", emoji="↩️", target=12),
        models.Pattern(id="greedy", label="Greedy", emoji="💡", target=10),
        models.Pattern(id="heaps", label="Heaps / Priority Q", emoji="⛏️", target=10),
        models.Pattern(id="tries", label="Tries", emoji="🌲", target=8),
        models.Pattern(id="stack", label="Stack / Monotonic", emoji="📚", target=10),
        models.Pattern(id="unionfind", label="Union-Find", emoji="🔗", target=8),
        models.Pattern(id="sysdes", label="System Design", emoji="🏗️", target=8),
    ]
    db.add_all(defaults)
    db.commit()


def ensure_default_user(db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        user = models.User(id=1)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# ── Read ──────────────────────────────────────────────────────────────────────


def get_activities(db: Session) -> list[models.Activity]:
    return db.query(models.Activity).all()


def get_patterns(db: Session) -> list[models.Pattern]:
    return db.query(models.Pattern).all()


# ── Write ─────────────────────────────────────────────────────────────────────


def create_activity_log(
    db: Session, user_id: int, data: schemas.LogActivityIn
) -> models.LogEntry:
    activity = (
        db.query(models.Activity).filter(models.Activity.id == data.activity_id).first()
    )
    if not activity:
        return None

    entry = models.LogEntry(
        user_id=user_id,
        date=date.today(),
        xp=activity.xp,
        label=activity.label,
        emoji=activity.emoji,
        source="manual",
        activity_id=activity.id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def create_pattern_log(
    db: Session, user_id: int, data: schemas.LogPatternIn
) -> models.LogEntry:
    pattern = (
        db.query(models.Pattern).filter(models.Pattern.id == data.pattern_id).first()
    )
    if not pattern:
        return None

    entry = models.LogEntry(
        user_id=user_id,
        date=date.today(),
        xp=5,
        label=f"{pattern.label} — {data.problem_name}",
        emoji=pattern.emoji,
        source="manual",
        pattern_id=pattern.id,
        problem_name=data.problem_name,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def claim_daily_bonus(db: Session, user_id: int) -> models.LogEntry | None:
    today = date.today()
    already = (
        db.query(models.LogEntry)
        .filter(
            models.LogEntry.user_id == user_id,
            models.LogEntry.source == "daily_bonus",
            models.LogEntry.date == today,
        )
        .first()
    )
    if already:
        return None  # already claimed today

    entry = models.LogEntry(
        user_id=user_id,
        date=today,
        xp=50,
        label="Daily Bonus",
        emoji="🎁",
        source="daily_bonus",
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def delete_log_entry(db: Session, entry_id: int, user_id: int) -> bool:
    entry = (
        db.query(models.LogEntry)
        .filter(
            models.LogEntry.id == entry_id,
            models.LogEntry.user_id == user_id,
        )
        .first()
    )
    if not entry:
        return False
    db.delete(entry)
    db.commit()
    return True


# ── State computation (the big one) ───────────────────────────────────────────
# This is the "derive everything from the log" principle in action.
# Nothing here is stored — it's all computed fresh from log_entries.


def get_state(db: Session, user_id: int) -> schemas.StateOut:
    today = date.today()
    entries = (
        db.query(models.LogEntry)
        .filter(models.LogEntry.user_id == user_id)
        .order_by(models.LogEntry.date.desc())
        .all()
    )

    # Total XP
    total_xp = sum(e.xp for e in entries)

    # XP per date (for the 7-day chart)
    xp_by_date: dict[str, int] = {}
    for e in entries:
        key = e.date.isoformat()
        xp_by_date[key] = xp_by_date.get(key, 0) + e.xp

    # Activity counts
    counts: dict[str, int] = {}
    for e in entries:
        if e.activity_id:
            counts[e.activity_id] = counts.get(e.activity_id, 0) + 1

    # Streak — count consecutive active days ending today or yesterday
    active_days = sorted(set(e.date for e in entries), reverse=True)
    streak = 0
    expected = today
    for d in active_days:
        if d == expected or d == expected - timedelta(days=1):
            streak += 1
            expected = d - timedelta(days=1)
        elif d < expected - timedelta(days=1):
            break

    # Max streak (full replay, oldest to newest)
    max_streak = 0
    current = 0
    prev = None
    for d in sorted(set(e.date for e in entries)):
        if prev is None or d == prev + timedelta(days=1):
            current += 1
        else:
            current = 1
        max_streak = max(max_streak, current)
        prev = d

    # Pattern progress
    patterns = db.query(models.Pattern).all()
    pattern_progress = []
    for p in patterns:
        records = [e for e in entries if e.pattern_id == p.id]
        pattern_progress.append(
            schemas.PatternProgress(
                pattern_id=p.id,
                label=p.label,
                emoji=p.emoji,
                target=p.target,
                count=len(records),
                last_touched=records[0].date if records else None,
                records=[e.problem_name for e in records if e.problem_name],
            )
        )

    # Daily bonus
    daily_bonus_claimed = any(
        e.source == "daily_bonus" and e.date == today for e in entries
    )

    return schemas.StateOut(
        total_xp=total_xp,
        streak=streak,
        max_streak=max_streak,
        xp_by_date=xp_by_date,
        counts=counts,
        pattern_progress=pattern_progress,
        recent_log=entries[:50],
        daily_bonus_claimed=daily_bonus_claimed,
    )
