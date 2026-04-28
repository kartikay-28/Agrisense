"""
AgriSense FastAPI Backend
=========================
Run with:  uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from app.database import create_tables
from app.routes import auth, farms, predict
from app.jobs.scheduler import update_market_data, send_weekly_insights


# ── Scheduler setup ───────────────────────────────────────────────────────────

scheduler = BackgroundScheduler()


def setup_jobs():
    # Job 1: Update market data every day at midnight
    scheduler.add_job(
        update_market_data,
        trigger="cron",
        hour=0,
        minute=0,
        id="update_market_data",
        replace_existing=True,
    )
    # Job 2: Send weekly insights every Sunday at 8:00 AM
    scheduler.add_job(
        send_weekly_insights,
        trigger="cron",
        day_of_week="sun",
        hour=8,
        minute=0,
        id="send_weekly_insights",
        replace_existing=True,
    )
    scheduler.start()


# ── App lifecycle ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    setup_jobs()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="AgriSense API",
    version="1.0.0",
    description="ML-powered agricultural decision support platform",
    lifespan=lifespan,
)

# Allow Next.js frontend (localhost:3000) during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://agrisense.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routes ───────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(farms.router)
app.include_router(predict.router)


@app.get("/")
def health():
    return {"status": "ok", "service": "AgriSense API"}
