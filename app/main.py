from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app import crud
from app.routers import activities, log, state


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts
    db = SessionLocal()
    try:
        crud.seed_activities(db)
        crud.seed_patterns(db)
        crud.ensure_default_user(db)
    finally:
        db.close()
    yield
    # Anything after yield runs on shutdown (nothing needed yet)


app = FastAPI(title="Google Quest API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(activities.router)
app.include_router(log.router)
app.include_router(state.router)
