from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.core.config import settings
from backend.core.db import engine, Base
from backend.core.logger import logger
from backend.routers import auth, users, profiles, astro
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Astrom backend...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully.")

        if not settings.DATA_DIR.exists():
            settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created data directory at {settings.DATA_DIR}")
        else:
            logger.info(f"📁 Data directory found: {settings.DATA_DIR}")

        yield  # app runs here

    finally:
        logger.info("🛑 Shutting down AI Astrom backend...")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI Astrom – Personalized Astrology Platform",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(astro.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}

# Diagnostic route print
print("\n🔍 ROUTE DEBUGGER — Listing registered paths:")
for r in app.router.routes:
    print(" •", r.path)
print("────────────────────────────────────────────\n")
