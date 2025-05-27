import os
import zipstream
from fastapi import HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.dao.search_dao import SearchService
from app.core.constants.exception_constant import ExceptionConstants
from app.core.constants.logger_constant import LoggerConstants
from app.core.constants.app_constant import AppConstants
from app.core.logger.logging import get_logger

logger = get_logger()

def search_and_return_files(query: str, db: Session):
    try:
        search_service = SearchService(db)
        results = search_service.search_documents(query)

        if not results:
            logger.info(LoggerConstants.FILE_MATCH_NO_QUERY.format(query=query))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ExceptionConstants.NO_MATCHING_FILES
            )

        logger.info(f"Search returned {len(results)} result(s): {results}")

        if len(results) == 1:
            filename, file_path, _ = results[0]
            file_path = os.path.normpath(file_path)

            if not os.path.isfile(file_path):
                logger.error(LoggerConstants.FILE_NOT_FOUND.format(file_path=file_path))
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ExceptionConstants.FILE_NOT_FOUND
                )

            logger.info(LoggerConstants.SINGLE_FILE_FOUND.format(file_path=file_path))
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type=AppConstants.MEDIA_TYPE_FILE
            )

        # Multiple files - create zip stream
        zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        files_added = 0

        for filename, file_path, _ in results:
            file_path = os.path.normpath(file_path)
            if os.path.isfile(file_path):
                try:
                    zip_file.write(file_path, arcname=filename)
                    files_added += 1
                except Exception as e:
                    logger.warning(f"Error adding file to zip: {file_path} | {e}")
            else:
                logger.warning(LoggerConstants.FILE_NOT_FOUND.format(file_path=file_path))

        if files_added == 0:
            logger.error("No valid files found to add to the ZIP archive.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ExceptionConstants.NO_MATCHING_FILES
            )

        logger.info(LoggerConstants.ZIP_FILE_RETURNING.format(count=files_added))
        return StreamingResponse(
            zip_file,
            media_type=AppConstants.MEDIA_TYPE_ZIP,
            headers={
                "Content-Disposition": f"attachment; filename={AppConstants.DEFAULT_RESULTS_FILENAME}"
            }
        )

    except HTTPException as http_exc:
        logger.warning(LoggerConstants.HTTP_ERROR_LOG.format(error=str(http_exc)))
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ExceptionConstants.INTERNAL_SERVER_ERROR.format(error=str(e))
        )
