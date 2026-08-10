from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import setup_exception_handlers
from app.database.connection import init_db

from app.routes import auth_routes, admin_routes, health_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting up {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode...")
    await init_db()
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url=None
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach Centralized Exception Handlers
setup_exception_handlers(app)

# Register Routers
app.include_router(health_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(admin_routes.router, prefix="/api/admin", tags=["Admin Control Panel"])
