class ExceptionConstants:
    
    # Upload related exceptions
    UPLOAD_FAILED = "Upload failed: {}"
    
    # Search related exceptions
    FILE_NOT_FOUND = "Matched file not found."
    NO_MATCHING_FILES = "No matching files found."
    SEARCH_FAILED = "Search failed: {}"
    
    # File type related exceptions
    UNSUPPORTED_FILE_TYPE = "Unsupported file type: {}. Supported types: PDF, DOCX"
    
    DOCUMENT_NOT_FOUND_WITH_HASH="No document found with hash: {file_hash}"
    
    DB_HASH_RETRIVAL_ERROR="Not able to retrieve document by hash: {error}"
    
    CREATE_UPDATE_FAILED = "Error creating or updating document: {error}"
    DOCUMENT_SEARCH_FAILED = "Error during document search: {error}"
    NO_MATCHING_DOCUMENTS = "No matching documents found."

    DB_CONNECTION_FAILED = "Database connection failed after {retries} attempts: {error}"
    DB_SESSION_FAILED = "Failed to connect to the database."
    DB_UNEXPECTED_ERROR = "Unexpected database error occurred: {error}"
    FILE_PROCESSING_FAILED = "Error processing file {filename}: {error}"
    TEXT_EXTRACTION_ERROR = "Error extracting text from {filename}: {error}"
    INTERNAL_SERVER_ERROR = "Internal Server Error: {error}"
    
    DOCUMENT_CREATE_UPDATE_ERROR="Error creating/updating document ({filename}): {error}"