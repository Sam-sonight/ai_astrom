# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from backend.core.config import settings
from backend.core.logger import logger
from backend.core.db import Base, engine
from backend.routers import auth, users, profiles, astro


# ============================================================
# LIFESPAN HANDLER (FASTAPI ≥ 0.95) — NEVER NESTED, CLEAN
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Astrom backend...")

    # --------------------------
    # Ensure DATA DIRECTORY exists
    # --------------------------
    data_dir = Path(settings.DATA_DIR)
    if not data_dir.exists():
        logger.info(f"📁 Creating data directory at: {data_dir}")
        data_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------
    # Initialize database
    # --------------------------
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

    yield

    logger.info("🛑 Shutting down AI Astrom backend...")


# ============================================================
# APPLICATION SETUP
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    description="AI Astrom — Hyper-Precision Astrology Engine",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================
origins = ["*"]  # Expand for production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(astro.router)


# ============================================================
# ROOT ENDPOINT
# ============================================================
@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running"}


# ============================================================
# ROUTE DEBUGGER (OPTIONAL – Visible at startup)
# ============================================================
def print_routes():
    import inspect

    print("\n🔍 ROUTE DEBUGGER — Listing registered paths:")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f" • {route.path}")
    print("────────────────────────────────────────────\n")


print_routes()
