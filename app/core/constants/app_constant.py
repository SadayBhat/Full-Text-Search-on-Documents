class AppConstants:
    # Supported file types for upload and indexing
    SUPPORTED_FILE_TYPES = [".pdf", ".docx"]
    
    # Chunk size for file processing (1MB)
    CHUNK_SIZE = 1024 * 1024
    
    # PostgreSQL text search configuration
    SEARCH_CONFIG = "simple"
    
    # Default ZIP filename for search results
    DEFAULT_RESULTS_FILENAME = "search_results.zip"

    # Write mode for file processing
    ZIP_WRITE_MODE="w"
    
    # Database connection retry delay time
    DELAY_TIME = 5
    
    # Database connection retry attempts
    RETRY_ATTEMPTS = 3  
    
    # Index
    INDEX_COLUMN_NAME = "ix_search_vector_gin"
    INDEX="gin"
    
    TABLE_NAME = "search_index"    
    
    MEDIA_TYPE_FILE = "application/octet-stream"
    MEDIA_TYPE_ZIP = "application/zip"