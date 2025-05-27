from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.constants.app_constant import AppConstants
from app.database.rds import get_db
from app.services.implementation.file_service import process_uploaded_file
from app.services.implementation.search_service import search_and_return_files
from app.core.constants.exception_constant import ExceptionConstants
from app.core.constants.response_constant import ResponseConstants
from app.core.constants.logger_constant import LoggerConstants
from app.utils.file_utils import get_file_extension, save_uploaded_file 
from app.core.logger.logging import get_logger

# Get logger
logger = get_logger()

router = APIRouter()

@router.post("/upload/", tags=["upload"])
async def upload_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        results = []
        for file in files:
            file_extension = get_file_extension(file.filename)
              
            if file_extension not in AppConstants.SUPPORTED_FILE_TYPES:
                logger.warning(LoggerConstants.UNSUPPORTED_FILE_TYPE.format(file_extension=file_extension))
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ExceptionConstants.UNSUPPORTED_FILE_TYPE.format(file_extension)
                )

            # Save file to disk
            save_path = await save_uploaded_file(file)

            # Process the file using the service layer
            result = await process_uploaded_file(file, db, save_path)  # Pass save_path to service function
            results.append(result)

        return {"message": ResponseConstants.UPLOAD_SUCCESS.format(len(files)), "files": results}
    
    except Exception as e:
        logger.error(LoggerConstants.FILE_UPLOAD_ERROR.format(error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ExceptionConstants.UPLOAD_FAILED.format(str(e))
        )


@router.get("/search/", tags=["search"])
def search(query: str = Query(..., description="Search term"), db: Session = Depends(get_db)):
    try:
        return search_and_return_files(query, db)
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(LoggerConstants.ERROR_DURING_FILE_SEARCH.format(error=str(e)))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ExceptionConstants.SEARCH_FAILED.format(str(e))
        )

