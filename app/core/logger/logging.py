import time
import sys
from fastapi import Request
from loguru import logger
from app.core.constants.logger_constant import LoggerConstants

# Configure loguru logger
logger.remove()  # Remove default handler to avoid conflict and duplication
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Configure loguru file logger 
logger.add(
    "logs/fts.log",  
    rotation="10 MB",  # Create new log file every 10 MB
    retention="1 week",  # Keep logs for 1 week
    compression="zip",  # Compress old logs to save space
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"  # Debug level logs will be written to file
)

async def log_request(request: Request, call_next):
    """Middleware to log requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.info(LoggerConstants.REQUEST_LOG.format(request=f"{request.method} {request.url}"))
    
    response = await call_next(request)
    
    # Calculate process time
    process_time = (time.time() - start_time) * 1000
    
    # Log response
    logger.info(LoggerConstants.RESPONSE_LOG.format(response=f"Status: {response.status_code}"))
    logger.info(LoggerConstants.PROCESS_TIME_LOG.format(time=round(process_time, 2)))
    
    return response

def get_logger():
    return logger
