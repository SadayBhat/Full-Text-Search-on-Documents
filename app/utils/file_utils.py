import hashlib
import os
import re
from fastapi import UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool
from shutil import copyfileobj
from app.core.config import settings
from app.core.logger.logging import get_logger
from app.core.constants.app_constant import AppConstants
from starlette import status

# Get logger
logger = get_logger()

async def save_uploaded_file(file: UploadFile) -> str:
    save_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        with open(save_path, "wb") as out_file:
            await run_in_threadpool(copyfileobj, file.file, out_file)
        logger.debug(f"File saved: {save_path}")
        return save_path
    except Exception as e:
        logger.error(f"Failed to save uploaded file {file.filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file."
        )

async def compute_file_hash(path: str) -> str:
    try:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(AppConstants.CHUNK_SIZE):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()
        logger.debug(f"File hash computed: {file_hash}")
        return file_hash
    except Exception as e:
        logger.error(f"Failed to compute file hash for {path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compute file hash."
        )

def clean_text_for_search(text: str) -> str:
    try:
        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r"\s+", " ", text)
        # Remove non-alphanumeric characters, but keep spaces
        cleaned_text = re.sub(r"[^\w\s]", "", cleaned_text)
        cleaned_text = cleaned_text.lower()
        return cleaned_text
    
    except Exception as e:
        logger.error(f"Text cleaning failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clean text for search indexing."
        )

def get_file_extension(filename: str) -> str:
    try:
        return os.path.splitext(filename)[1].lower()
    except Exception as e:
        logger.error(f"Failed to extract file extension from {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename provided."
        )
