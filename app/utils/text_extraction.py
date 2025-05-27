from app.core.logger.logging import get_logger
from app.core.constants.logger_constant import LoggerConstants
from app.core.constants.exception_constant import ExceptionConstants
from typing import Callable, Awaitable
from fastapi import HTTPException,status


# Get logger
logger = get_logger()

async def extract_pdf_text(file_path: str) -> str:
    # Extract text from a PDF file
    try:
        import fitz
        with fitz.open(file_path) as pdf:
            text = "\n".join(page.get_text() for page in pdf if page.get_text().strip())
            logger.debug(f"Extracted {len(text)} characters from PDF: {file_path}")
            return text
    except Exception as e:
        logger.error(LoggerConstants.TEXT_EXTRACTION_ERROR.format(
            filename=file_path, error=str(e)))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error extracting text from PDF: {e}")

async def extract_docx_text(file_path: str) -> str:
    # Extract text from a DOCX file
    try:
        from docx import Document as DocxDocument
        doc = DocxDocument(file_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        logger.debug(f"Extracted {len(text)} characters from DOCX: {file_path}")
        return text
    except Exception as e:
        logger.error(LoggerConstants.TEXT_EXTRACTION_ERROR.format(
            filename=file_path, error=str(e)))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error extracting text from DOCX: {e}")


# Mapping of file extensions to their respective extraction functions
EXTRACTION_FUNCTIONS: dict[str, Callable[[str], Awaitable[str]]] = {
    ".pdf": extract_pdf_text,
    ".docx": extract_docx_text,
}

async def extract_text_from_file(file_path: str, file_extension: str) -> str:
    # Extract text from a file based on its extension using mapping
    try:
        extractor = EXTRACTION_FUNCTIONS.get(file_extension)
        if extractor:
            return await extractor(file_path)
    
        logger.warning(LoggerConstants.UNSUPPORTED_FILE_TYPE.format(file_extension = {file_extension}))
        return ""  # Unsupported file type
    except Exception as e:
        logger.error(LoggerConstants.FILE_PROCESSING_FAILED.format(filename=file_path, error=str(e)))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ExceptionConstants.TEXT_EXTRACTION_ERROR.format(str(e)))

