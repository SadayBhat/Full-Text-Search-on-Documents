from fastapi import HTTPException, UploadFile,status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.file_utils import compute_file_hash, clean_text_for_search, get_file_extension
from app.utils.text_extraction import extract_text_from_file
from app.dao.search_dao import SearchService 
from app.core.constants.app_constant import AppConstants
from app.core.constants.logger_constant import LoggerConstants
from app.core.constants.exception_constant import ExceptionConstants
from app.core.logger.logging import get_logger

# Get logger
logger = get_logger()
    
async def process_uploaded_file(file: UploadFile, db: Session, save_path: str):
    try:
        logger.info(LoggerConstants.FILE_PROCESSING_START.format(filename=file.filename))

        # Compute hash from saved file
        file_hash = await compute_file_hash(save_path)

        # Extract text based on file extension
        file_extension = get_file_extension(file.filename)
        text = await extract_text_from_file(save_path, file_extension)

        # Clean text for search indexing
        clean_text = clean_text_for_search(text)

        # Use the DAO class to handle DB operations
        search_service = SearchService(db)
        search_service.create_or_update_document(file.filename, file_hash, save_path, clean_text)

        logger.info(LoggerConstants.FILE_PROCESSING_COMPLETE.format(filename=file.filename))
        return {"filename": file.filename, "hash": file_hash}

    except Exception as e:
        logger.error(LoggerConstants.FILE_PROCESSING_FAILED.format(filename=file.filename, error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ExceptionConstants.FILE_PROCESSING_FAILED.format(str(e))
        )


