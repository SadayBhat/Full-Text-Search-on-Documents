from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logger.logging import get_logger
from app.core.constants.logger_constant import LoggerConstants
from app.core.constants.app_constant import AppConstants
from app.core.constants.exception_constant import ExceptionConstants
from fastapi import HTTPException, status, Depends
import time
from sqlalchemy.exc import SQLAlchemyError


# Get logger
logger = get_logger()

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        logger.error(LoggerConstants.DB_SESSION_ERROR.format(error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ExceptionConstants.DB_SESSION_FAILED
        )
    finally:
        db.close()


# Test database connection with retry logic
def test_db_connection(retries: int = AppConstants.RETRY_ATTEMPTS, delay:int = AppConstants.DELAY_TIME):
    attempt = 0
    while attempt < retries:
        try:
            with engine.connect() as conn:
                logger.info(LoggerConstants.DB_CONNECT_SUCCESS)
                return
        except Exception as e:
            attempt += 1
            logger.error(LoggerConstants.DB_CONNECT_ERROR.format(error=str(e)))
            if attempt >= retries:
                logger.error(LoggerConstants.DB_CONNECT_RETRY_FAIL.format(retries=retries))
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=ExceptionConstants.DB_CONNECTION_FAILED.format(retries=retries, error=str(e)))
            time.sleep(delay)

# Calling the function to test DB connection when the application starts
test_db_connection()

