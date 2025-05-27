import os
from fastapi import FastAPI, Request,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.rds import Base, engine
from app.api.v1.endpoints.routes import router
from app.core.logger.logging import log_request, get_logger
from app.core.config import settings
from app.core.constants.response_constant import ResponseConstants
from app.core.constants.logger_constant import LoggerConstants

# Get logger
logger = get_logger()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(LoggerConstants.APP_STARTUP)
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            logger.info(LoggerConstants.DB_CONNECT_SUCCESS)
    except Exception as e:
        logger.error(LoggerConstants.DB_CONNECT_ERROR.format(error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=LoggerConstants.DB_CONNECT_ERROR.format(error=str(e))
        )
    yield
    logger.info(LoggerConstants.APP_SHUTDOWN)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A FastAPI application for full-text search of documents",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware - Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origins
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_request(request, call_next)

# Include router
app.include_router(router, prefix=settings.API_PREFIX,tags=["FTS-Document-Search"])
