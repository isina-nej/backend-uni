# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.config import settings
from app.database import engine, Base, get_db
from app.routers import (
    universities, users, academic, financial, library,
    reports, notifications, system
)
from app.core.security import create_initial_admin
from app.core.cache import init_cache
from app.core.auth import get_current_user_optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting University Management System...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize cache
    await init_cache()

    # Create initial admin user if not exists
    await create_initial_admin()

    logger.info("University Management System started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down University Management System...")

# Create FastAPI application
app = FastAPI(
    title="University Management System API",
    description="Comprehensive API for managing university operations",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Get user info if available
    try:
        user = await get_current_user_optional(request)
        user_info = f"User: {user.id} ({user.email})" if user else "Anonymous"
    except:
        user_info = "Anonymous"

    logger.info(f"Request: {request.method} {request.url} - {user_info}")

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(".2f")

    return response

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "HTTPException"
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "type": "InternalServerError"
            }
        }
    )

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to University Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Include routers
app.include_router(
    universities.router,
    prefix="/api/v1/universities",
    tags=["Universities"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    academic.router,
    prefix="/api/v1/academic",
    tags=["Academic"]
)

app.include_router(
    financial.router,
    prefix="/api/v1/financial",
    tags=["Financial"]
)

app.include_router(
    library.router,
    prefix="/api/v1/library",
    tags=["Library"]
)

app.include_router(
    reports.router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)

app.include_router(
    notifications.router,
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)

app.include_router(
    system.router,
    prefix="/api/v1/system",
    tags=["System"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
