class LoggerConstants:
    
    # Request/response logging
    REQUEST_LOG = "Request: {request}"
    RESPONSE_LOG = "Response: {response}"
    PROCESS_TIME_LOG = "Process time: {time}ms"
    
    # Error logging
    ERROR_LOG = "Error: {error}"
    HTTP_ERROR_LOG = "HTTP Error: {error}"
    
    # Database logging
    DB_CONNECT_SUCCESS = "Successfully connected to the database"
    DB_CONNECT_ERROR = "Failed to connect to the database: {error}"
    
    # File processing logging
    FILE_PROCESSING_START = "Processing file: {filename}"
    FILE_PROCESSING_COMPLETE = "File processed: {filename}"
    TEXT_EXTRACTION_ERROR = "Error extracting text from {filename}: {error}"
    FILE_PROCESSING_FAILED = "Error processing file {filename}: {error}"
    FILE_NOT_FOUND = "File not found: {file_path}"
    FILE_MATCH_NO_QUERY = "No matching files found for query: {query}"
    ZIP_FILE_CREATED = "Created zip for {count} files"
    ZIP_FILE_RETURNING = "Returning zip with {count} files"
    SINGLE_FILE_FOUND = "Returning single file: {file_path}"
    
    # App lifecycle logging
    APP_STARTUP = "Application startup initiated."
    APP_SHUTDOWN = "Application shutdown completed."
    
    UNSUPPORTED_FILE_TYPE = "Unsupported file type: {file_extension}"
    FILE_UPLOAD_ERROR = "Error during file upload: {error}"
    ERROR_DURING_FILE_SEARCH="Error during search: {error}"
    
    DOCUMENT_FOUND_WITH_HASH="Found document with hash: {file_hash}"
    DOCUMENT_NOT_FOUND_WITH_HASH="No document found with hash: {file_hash}"
    DB_HASH_RETRIVAL_ERROR="Not able to retrieve document by hash:{file_hash} {error}"
    
    DOCUMENT_UPDATE = "Updating existing document: {filename}"
    DOCUMENT_CREATE = "Creating new document: {filename}"
    DOCUMENT_CREATE_UPDATE_ERROR = "Error creating/updating document ({filename}): {error}"

    # Search
    DOCUMENT_SEARCHING = "Searching for: {query}"
    DOCUMENT_SEARCH_RESULT_COUNT = "Found {count} matching documents"
    DOCUMENT_SEARCH_ERROR = "Error searching documents with query '{query}': {error}"
    DOCUMENT_CREATE_UPDATE_SUCCESS = "Successfully committed changes for document: {filename}"

    DB_CONNECT_ERROR = "Database connection error: {error}"
    DB_SESSION_ERROR = "Database session error: {error}"
    DB_CONNECT_RETRY_FAIL = "Failed to connect to the database after {retries} attempts."
    
    


