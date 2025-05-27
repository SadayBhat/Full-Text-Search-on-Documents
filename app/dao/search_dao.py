from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models.search_index import SearchIndex
from app.core.logger.logging import get_logger
from app.core.constants.logger_constant import LoggerConstants
from app.core.constants.app_constant import AppConstants
from app.core.constants.exception_constant import ExceptionConstants
from fastapi import HTTPException, status
from app.utils.file_utils import clean_text_for_search

# Get logger
logger = get_logger()

class SearchService:
    
    def __init__(self, db: Session):
        self.db = db

    def get_document_by_hash(self, file_hash: str):
        # Get a document by its hash
        try:
            document = self.db.query(SearchIndex).filter_by(file_hash=file_hash).first()
            if document:
                logger.debug(LoggerConstants.DOCUMENT_FOUND_WITH_HASH.format(file_hash=file_hash))
            else:
                logger.debug(LoggerConstants.DOCUMENT_NOT_FOUND_WITH_HASH.format(file_hash=file_hash))
            return document
        except Exception as e:
            logger.error(LoggerConstants.DB_HASH_RETRIVAL_ERROR.format(file_hash=file_hash, error=str(e)))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 detail=ExceptionConstants.DB_HASH_RETRIVAL_ERROR.format(error=str(e)))

    def create_or_update_document(self, filename: str, file_hash: str, file_path: str, clean_text: str):
        try:
            cleaned_filename = clean_text_for_search(filename)
            search_vector = func.to_tsvector(AppConstants.SEARCH_CONFIG, clean_text + ' ' + cleaned_filename)


            existing = self.get_document_by_hash(file_hash)
            
            #print(f"Indexing: {filename} -> {clean_text[:200]}...")
        
            if existing:
                logger.info(LoggerConstants.DOCUMENT_UPDATE.format(filename=filename))
                existing.file_path = file_path
                existing.search_vector = search_vector
            else:
                logger.info(LoggerConstants.DOCUMENT_CREATE.format(filename=filename))
                self.db.add(SearchIndex(
                    filename=filename,
                    file_hash=file_hash,
                    file_path=file_path,
                    search_vector=search_vector
            ))

            self.db.commit()
            logger.info(LoggerConstants.DOCUMENT_CREATE_UPDATE_SUCCESS.format(filename=filename))

        except Exception as e:
            self.db.rollback()
            logger.error(LoggerConstants.DOCUMENT_CREATE_UPDATE_ERROR.format(filename=filename, error=str(e)))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=ExceptionConstants.DOCUMENT_CREATE_UPDATE_ERROR.format(error=str(e)))


    def search_documents(self, query: str):
        try:
            cleaned_query = clean_text_for_search(query)
            logger.info(LoggerConstants.DOCUMENT_SEARCHING.format(query=query))

            #ts_query = func.websearch_to_tsquery (AppConstants.SEARCH_CONFIG, cleaned_query.replace(" ", " & "))
            ts_query = func.websearch_to_tsquery (AppConstants.SEARCH_CONFIG, cleaned_query)
            #ts_query = func.to_tsquery (AppConstants.SEARCH_CONFIG, cleaned_query.replace(" ", " & "))
            results = (
                self.db.query(
                    SearchIndex.filename,
                    SearchIndex.file_path,
                    func.ts_rank(SearchIndex.search_vector, ts_query).label("rank")
                )
                .filter(SearchIndex.search_vector.op('@@')(ts_query))
                .order_by(func.ts_rank(SearchIndex.search_vector, ts_query).desc())
                .all()
            )

            logger.info(LoggerConstants.DOCUMENT_SEARCH_RESULT_COUNT.format(count=len(results)))

            if not results:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ExceptionConstants.NO_MATCHING_DOCUMENTS
                )

            return results

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logger.error(LoggerConstants.DOCUMENT_SEARCH_ERROR.format(query=query, error=str(e)))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ExceptionConstants.DOCUMENT_SEARCH_FAILED.format(error=str(e))
            )