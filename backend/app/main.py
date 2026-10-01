import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import init_db, SessionLocal
from app.database.seed_data import seed_database
from app.rag.ingestion import ingest_travel_knowledge
from app.api.auth import router as auth_router
from app.api.destinations import router as destinations_router
from app.api.chat import router as chat_router
from app.api.trips import router as trips_router
from app.api.users import router as users_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle hooks.
    """
    logger.info("Initializing AI Travel Planner Agent Backend...")
    # 1. Initialize Tables
    init_db()

    # 2. Seed Database
    if SessionLocal:
        db = SessionLocal()
        try:
            seed_database(db)
        finally:
            db.close()

    # 3. Ingest ChromaDB Travel Knowledge
    try:
        ingest_travel_knowledge()
    except Exception as e:
        logger.warning(f"ChromaDB knowledge ingestion warning: {e}")

    logger.info("Backend initialization complete!")
    yield
    logger.info("Shutting down AI Travel Planner Agent Backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Agentic AI Travel Planning Assistant powered by LangGraph, Groq, ChromaDB, MySQL & FastAPI.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(destinations_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(trips_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
        "groq_model": settings.GROQ_MODEL,
        "api_key_configured": bool(settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("gsk_placeholder"))
    }
